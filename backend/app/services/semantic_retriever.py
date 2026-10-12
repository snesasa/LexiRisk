import os
import json
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

from ..config import CACHE_DIR
from .cuad_taxonomy import CUAD_CATEGORIES

class SemanticRetriever:
    """
    Semantic retrieval and clause comparison engine.
    Stores and indexes standard precedent clauses for all 41 CUAD categories.
    Enables side-by-side comparison, conflicting clause identification, and semantic gap analysis.
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=8000, sublinear_tf=True)
        self.precedent_clauses: List[Dict[str, Any]] = []
        self.clause_matrix = None
        self._build_index()

    def _build_index(self):
        """Constructs benchmark index from CUAD taxonomy."""
        self.precedent_clauses = []
        texts = []

        for cat, meta in CUAD_CATEGORIES.items():
            entry = {
                "category": cat,
                "title": meta["title"],
                "description": meta["description"],
                "standard_text": meta["benchmark"],
                "base_risk": meta["base_risk"]
            }
            self.precedent_clauses.append(entry)
            texts.append(f"{meta['title']} {meta['description']} {meta['benchmark']}")

        self.clause_matrix = self.vectorizer.fit_transform(texts)

    def find_benchmark_for_clause(self, category: str) -> Optional[Dict[str, Any]]:
        """Retrieves the official market standard benchmark clause for a CUAD category."""
        meta = CUAD_CATEGORIES.get(category)
        if not meta:
            return None
        return {
            "category": category,
            "title": meta["title"],
            "benchmark_text": meta["benchmark"],
            "description": meta["description"],
            "base_risk": meta["base_risk"]
        }

    def compare_clauses(self, clause_a: str, clause_b: str) -> Dict[str, Any]:
        """
        Performs in-depth side-by-side comparison between two clauses.
        Returns semantic similarity, key divergent tokens, and drafting assessment.
        """
        vecs = self.vectorizer.transform([clause_a, clause_b])
        sim = float(cosine_similarity(vecs[0], vecs[1])[0][0])
        sim_percentage = round(sim * 100, 1)

        # Token analysis
        words_a = set(clause_a.lower().split())
        words_b = set(clause_b.lower().split())

        common_words = words_a.intersection(words_b)
        unique_a = list(words_a - words_b)[:10]
        unique_b = list(words_b - words_a)[:10]

        # Legal alignment diagnosis
        if sim_percentage >= 80:
            diagnosis = "Substantially Identical: Both clauses share core legal structure and terminology."
        elif sim_percentage >= 50:
            diagnosis = "Moderate Alignment: Clauses address similar subject matter but have differing obligations or qualifications."
        else:
            diagnosis = "Divergent Language: Clauses diverge significantly in scope, remedy mechanisms, or party obligations."

        return {
            "similarity_score": round(sim, 3),
            "similarity_percentage": sim_percentage,
            "diagnosis": diagnosis,
            "unique_terms_first": unique_a,
            "unique_terms_second": unique_b,
            "shared_term_count": len(common_words)
        }

    def compare_against_market_standard(self, clause_text: str, category: str) -> Dict[str, Any]:
        """Compares user's clause against the CUAD market standard benchmark."""
        benchmark = self.find_benchmark_for_clause(category)
        if not benchmark:
            return {
                "category": category,
                "benchmark_text": "No market standard precedent found.",
                "comparison": None
            }

        comp = self.compare_clauses(clause_text, benchmark["benchmark_text"])
        return {
            "category": category,
            "benchmark_title": benchmark["title"],
            "benchmark_text": benchmark["benchmark_text"],
            "benchmark_description": benchmark["description"],
            "comparison": comp
        }

    def retrieve_similar_clauses(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Finds closest matching CUAD categories and standard provisions."""
        query_vec = self.vectorizer.transform([query_text])
        sims = cosine_similarity(query_vec, self.clause_matrix)[0]
        top_indices = np.argsort(sims)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(sims[idx])
            prec = self.precedent_clauses[idx]
            results.append({
                "category": prec["category"],
                "title": prec["title"],
                "similarity": round(score, 3),
                "benchmark_text": prec["standard_text"]
            })
        return results

# Global singleton
_retriever_instance = None

def get_semantic_retriever() -> SemanticRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = SemanticRetriever()
    return _retriever_instance
