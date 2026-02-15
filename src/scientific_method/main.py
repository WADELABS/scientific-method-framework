"""
src/scientific_method/main.py
The Hypothesis Layer: AI as a PhD Candidate.
"""

import asyncio
from typing import List
from .research import ResearchAgent

class ScientificAgent:
    def __init__(self, researcher: ResearchAgent):
        self.researcher = researcher

    def generate_raw_claim(self, observation: str) -> str:
        """The AI's 'Intuition' - potential hallucination zone."""
        # In a real implementation, this would call the LLM
        return f"Hypothesis based on observation: {observation}"

    async def inquire(self, observation: str):
        """Standard scientific inquiry process."""
        print(f"\n🔬 Processing Observation: '{observation}'")
        
        # Phase 1: Hypothesis (The AI's 'Intuition')
        # We treat this as UNVERIFIED immediately.
        hypothesis = self.generate_raw_claim(observation)
        print(f"DEBUG: Hypothesis Generated: {hypothesis[:50]}...")

        # Phase 2: The 'Trial by Fire' (Active Research)
        # The AI is now forced to find REAL sources before proceeding.
        print("DEBUG: Initiating Active Research Phase...")
        verification = await self.researcher.test_hypothesis(hypothesis)
        
        # Phase 3: Synthesis (Only outputting what survived the test)
        conclusion = self.formulate_conclusion(verification, hypothesis)
        
        print("\n✅ FINAL VERIFIED CONCLUSION:")
        print(conclusion)
        return conclusion

    def formulate_conclusion(self, verification: dict, original_hypothesis: str) -> str:
        """Synthesize research into a final, verifiable conclusion."""
        if not verification.get("credible_sources"):
            return "RESULT: INCONCLUSIVE. No credible evidence found to support the hypothesis."
        
        sources = "\n".join([f"- {s}" for s in verification['credible_sources']])
        return f"RESULT: VERIFIED.\nConclusion: {original_hypothesis}\nSupported by:\n{sources}"

if __name__ == "__main__":
    from .research_test import MockResearchAgent # Placeholder for testing
    agent = ScientificAgent(MockResearchAgent())
    asyncio.run(agent.inquire("Atmospheric composition influences nitrogen levels."))
