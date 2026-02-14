import asyncio
import logging
import sys
import os

# Ensure local 'src' is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

try:
    from z3 import *
except ImportError:
    logging.error("Z3 solver not found.")

from src.vsa.agent import ReflectiveQuantAgent

async def run_portfolio_demo():
    """
    Showcase the 7-layer complexity of the VSA framework.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("\n" + "="*80)
    print("VSA PORTFOLIO DEMO: 7-LAYER COMPLEXITY RESEARCH CYCLE")
    print("="*80 + "\n")

    # Initialize the SOTA Agent (AFRRC Tier 1)
    agent = ReflectiveQuantAgent(domain="High-Frequency Alpha Discovery")

    # Define a formal trading hypothesis using Z3
    # E.g., Alpha (A) must exceed Transaction Cost (C) under Volatility (V)
    A = Real('alpha')
    C = Real('cost')
    V = Real('volatility')
    # Axiom: Alpha must be positive and at least 2x the cost of execution
    hypothesis_constraints = [A > 2 * C, C > 0, V > 0.02]

    # Sample market research data
    research_item = {
        "ticker": "AAPL-ARB",
        "predicted_alpha_bps": 15.5,
        "citation": "10.1515/quant-finance.2024.01"
    }

    print(f"[*] Starting verifiable research cycle for: {agent.domain}")
    result = await agent.execute_alpha_cycle(
        "Inter-market arbitrage opportunities in AAPL derivatives exceed execution friction.",
        hypothesis_constraints,
        research_item
    )

    if result["status"] == "success":
        print(f"\n[+] Alpha Hypothesis Verified!")
        print(f"    Ledger Block: {result['block_hash']}")
        print(f"    Report Path:  {result['report']}")
    else:
        print(f"\n[-] Hypothesis Rejected: {result['reason']}")

    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(run_portfolio_demo())
