import re
import io
from typing import List, Dict, Any, Tuple
import pypdf
import docx

class DocumentParser:
    @staticmethod
    def parse_file(filename: str, content: bytes) -> str:
        """Extract text from TXT, DOCX, or PDF bytes."""
        lower_name = filename.lower()
        if lower_name.endswith('.txt'):
            return content.decode('utf-8', errors='replace')
        elif lower_name.endswith('.pdf'):
            reader = pypdf.PdfReader(io.BytesIO(content))
            pages_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            return "\n\n".join(pages_text)
        elif lower_name.endswith('.docx') or lower_name.endswith('.doc'):
            doc = docx.Document(io.BytesIO(content))
            return "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        else:
            return content.decode('utf-8', errors='replace')

    @staticmethod
    def segment_contract(text: str) -> List[Dict[str, Any]]:
        """
        Segments a legal contract into discrete, analyzable clauses/sections.
        Detects standard section numbering, article titles, and logical paragraph boundaries.
        """
        # Normalize carriage returns
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Split text into raw blocks
        blocks = re.split(r'\n{2,}', text)
        clauses = []
        clause_idx = 1
        current_section_title = "Preamble & Recitals"

        # Regex for section headers like: "1. Term", "1.1 Termination", "Section 5.", "ARTICLE IV - INDEMNITY"
        section_regex = re.compile(
            r'^(?:(?:SECTION|ARTICLE|CLAUSE)\s+[\dIVXLCDM]+[\.:\s\-]+|(?:\d+(?:\.\d+)*)[\.\s\-]+)([A-Z][A-Za-z0-9\s,\-\/\(\)]+)',
            re.IGNORECASE
        )

        for raw_block in blocks:
            clean_block = raw_block.strip()
            if not clean_block:
                continue

            # Check if this block is very short and acts like a standalone section header
            lines = clean_block.split('\n')
            first_line = lines[0].strip()
            
            header_match = section_regex.match(first_line)
            if header_match and len(first_line) < 100:
                current_section_title = first_line

            # If the block contains multiple enumerated sub-clauses, e.g. "(a) ... (b) ...", break or keep cohesive
            if len(clean_block) < 30 and not header_match:
                # likely a minor header or label
                current_section_title = clean_block
                continue

            # Sub-segment if the block is huge (>1200 chars) with numbered paragraphs
            if len(clean_block) > 1200:
                sub_parts = re.split(r'\n(?=(?:\d+\.\d+|\([a-z\d]+\))\s+)', clean_block)
                if len(sub_parts) > 1:
                    for sp in sub_parts:
                        sp_clean = sp.strip()
                        if len(sp_clean) > 20:
                            clauses.append({
                                "clause_index": clause_idx,
                                "section_title": current_section_title,
                                "text": sp_clean
                            })
                            clause_idx += 1
                    continue

            clauses.append({
                "clause_index": clause_idx,
                "section_title": current_section_title,
                "text": clean_block
            })
            clause_idx += 1

        # Fallback if no clauses segmented
        if not clauses and text.strip():
            clauses.append({
                "clause_index": 1,
                "section_title": "Full Agreement Text",
                "text": text.strip()
            })

        return clauses
