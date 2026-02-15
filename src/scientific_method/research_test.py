"""
src/scientific_method/research_test.py
Mock Research Agent for Phase 2 demonstration.
"""

from .research import ResearchAgent
from .credibility import CredibilitySubstrate

class MockResearchAgent(ResearchAgent):
    def __init__(self):
        super().__init__(CredibilitySubstrate())

    async def fetch_external_data(self, hypothesis: str) -> list:
        """Controlled mock data for testing."""
        return [
            "https://university.edu/papers/active-nitrogen-study.pdf", # Credible
            "https://arxiv.org/abs/2301.12345", # Credible
            "https://blog.hallucination.com/fake-facts" # Unverified
        ]
