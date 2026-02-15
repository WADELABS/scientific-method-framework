"""
src/scientific_method/credibility.py
The Credibility Engine: Solves the 'Fake Source' problem.
"""

import re

class SourceRegistry:
    def __init__(self):
        # Trusted roots for academic and institutional data sovereignty
        self.trusted_roots = [".edu", ".gov", "arxiv.org", "jstor.org", "nature.com", "science.org"]
        
    def evaluate(self, source_url: str) -> str:
        """
        Evaluate if a source comes from a verified, credible database.
        Returns 'CREDIBLE' or 'UNVERIFIED_SOURCE'.
        """
        # Phase 1: Pattern Matching against Trusted Roots
        is_trusted = any(pattern in source_url.lower() for pattern in self.trusted_roots)
        
        if is_trusted:
            # Phase 2: Heuristic Validation (e.g. basic URL structure check)
            # In Phase 3, this would include DNS validation and SSL cert verification
            if re.match(r'^https?://', source_url):
                return "CREDIBLE"
                
        # If it's not in the registry, it's flagged as 'Anecdotal' or 'Potential Hallucination'
        return "UNVERIFIED_SOURCE"

class CredibilitySubstrate:
    """Manages the hierarchy of evidence."""
    def __init__(self):
        self.registry = SourceRegistry()

    def filter_sources(self, sources: list) -> list:
        """Return only sources that meet the baseline credibility threshold."""
        return [s for s in sources if self.registry.evaluate(s) == "CREDIBLE"]
