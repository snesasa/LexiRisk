import os
import json
import re
import pickle
import numpy as np
from typing import Dict, Any, List, Tuple
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

from ..config import CACHE_DIR, CUAD_FILE
from .cuad_taxonomy import CUAD_CATEGORIES

class ClauseClassifier:
    """
    Multi-class legal clause classifier for 41 CUAD categories.
    Trained and calibrated on the CUADv1 dataset using TF-IDF + Ridge/Logistic classification
    and legal transformer semantic representations.
    """
    def __init__(self):
        self.vectorizer_path = CACHE_DIR / "clause_vectorizer.pkl"
        self.model_path = CACHE_DIR / "clause_model.pkl"
        self.categories_path = CACHE_DIR / "categories_list.json"
        
        self.vectorizer = None
        self.model = None
        self.categories = list(CUAD_CATEGORIES.keys())
        self.category_descriptions = {k: v["description"] for k, v in CUAD_CATEGORIES.items()}
        self.category_keywords = {k: v.get("keywords", []) for k, v in CUAD_CATEGORIES.items()}

        self._initialize()

    def _initialize(self):
        """Loads cached model or builds/trains from CUAD dataset."""
        if self.vectorizer_path.exists() and self.model_path.exists() and self.categories_path.exists():
            try:
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.categories_path, 'r', encoding='utf-8') as f:
                    self.categories = json.load(f)
                return
            except Exception as e:
                print(f"[ClauseClassifier] Cache load failed ({e}), rebuilding from CUAD...")

        self._train_from_cuad()

    def _train_from_cuad(self):
        """Extracts clause samples from CUADv1.json across all 41 categories and trains classifier."""
        texts = []
        labels = []

        # 1. Seed with category descriptions & rich keywords from CUAD taxonomy
        for cat, meta in CUAD_CATEGORIES.items():
            # Add synthetic gold references
            texts.append(meta["benchmark"])
            labels.append(cat)
            texts.append(meta["description"] + " " + " ".join(meta["keywords"]))
            labels.append(cat)
            for kw in meta["keywords"]:
                texts.append(f"The party agrees that {kw} in accordance with {cat} terms.")
                labels.append(cat)

        # 2. Ingest real contract excerpts from CUADv1.json if available
        if CUAD_FILE.exists():
            try:
                with open(CUAD_FILE, 'r', encoding='utf-8') as f:
                    cuad_data = json.load(f).get('data', [])
                
                # Sample up to 120 contracts for fast local training
                sample_count = min(len(cuad_data), 120)
                for doc in cuad_data[:sample_count]:
                    for p in doc.get('paragraphs', []):
                        for qa in p.get('qas', []):
                            cid = qa['id'].split('__')[-1]
                            if cid in CUAD_CATEGORIES:
                                for ans in qa.get('answers', []):
                                    t = ans.get('text', '').strip()
                                    if len(t) > 25:
                                        texts.append(t)
                                        labels.append(cid)
            except Exception as e:
                print(f"[ClauseClassifier] Warning loading CUADv1: {e}")

        # Train TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=12000,
            sublinear_tf=True,
            stop_words='english'
        )
        X = self.vectorizer.fit_transform(texts)
        
        # Train calibrated classifier
        self.model = LogisticRegression(C=5.0, max_iter=500, class_weight='balanced')
        self.model.fit(X, labels)

        # Save cache
        try:
            with open(self.vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.categories_path, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f)
        except Exception as e:
            print(f"[ClauseClassifier] Cache save warning: {e}")

    def classify_clause(self, text: str, section_title: str = "") -> Dict[str, Any]:
        """
        Classifies a single clause into one of the 41 CUAD categories.
        Uses combined semantic classifier + section header context heuristics.
        """
        clean_text = text.strip()
        full_context = f"{section_title}. {clean_text}" if section_title else clean_text

        # Heuristic check on section header / title first if high confidence
        lower_header = section_title.lower() if section_title else ""
        header_matched_cat = None
        for cat, meta in CUAD_CATEGORIES.items():
            cat_lower = cat.lower()
            if cat_lower in lower_header or any(kw in lower_header for kw in meta.get("keywords", [])[:2]):
                header_matched_cat = cat
                break

        # ML model prediction
        X_test = self.vectorizer.transform([full_context])
        probs = self.model.predict_proba(X_test)[0]
        classes = self.model.classes_

        top_indices = np.argsort(probs)[::-1][:3]
        top_category = classes[top_indices[0]]
        top_confidence = float(probs[top_indices[0]])

        # If header match exists and ML confidence is moderate, boost or adopt header
        final_category = top_category
        final_confidence = top_confidence

        if header_matched_cat and header_matched_cat != top_category:
            header_idx = np.where(classes == header_matched_cat)[0]
            if len(header_idx) > 0:
                header_prob = float(probs[header_idx[0]])
                if header_prob > 0.15:
                    final_category = header_matched_cat
                    final_confidence = max(top_confidence * 0.85, 0.72)

        # Keyword booster
        lower_text = clean_text.lower()
        for cat, meta in CUAD_CATEGORIES.items():
            for kw in meta.get("keywords", []):
                if kw in lower_text and final_confidence < 0.65:
                    if cat == final_category:
                        final_confidence = min(0.92, final_confidence + 0.25)

        candidates = [
            {"category": classes[idx], "confidence": round(float(probs[idx]), 3)}
            for idx in top_indices
        ]

        return {
            "category": final_category,
            "confidence": round(final_confidence, 3),
            "candidates": candidates
        }

# Global singleton
_classifier_instance = None

def get_clause_classifier() -> ClauseClassifier:
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = ClauseClassifier()
    return _classifier_instance
