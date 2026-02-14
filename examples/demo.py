import asyncio
import logging
from datetime import datetime
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.scientific_agent import KnowledgeBase, Hypothesis
from src.agent import DeepScientificAgent
from src.foundations import ScientificParadigm
from src.visualization import EnhancedScientificVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

async def main():
    print("=== Scientific Method Framework V2 Demo ===")
    
    # 1. Initialize
    kb = KnowledgeBase()
    
    # Add initial hypotheses
    h1 = Hypothesis(
        id="h_dark_matter",
        statement="Dark matter consists of weakly interacting massive particles (WIMPs)",
        variables={"mass": "high", "interaction": "weak"},
        relationships=["explains_rotation_curves"],
        domain="astrophysics",
        timestamp=datetime.now(),
        confidence=0.6,
        complexity=0.7,
        novelty=0.4,
        testability=0.5
    )
    
    h2 = Hypothesis(
        id="h_mond",
        statement="Modified Newtonian Dynamics (MOND) explains rotation curves without dark matter",
        variables={"gravity": "modified", "acceleration": "low"},
        relationships=["explains_rotation_curves_low_acc"],
        domain="astrophysics",
        timestamp=datetime.now(),
        confidence=0.4,
        complexity=0.6,
        novelty=0.8,
        testability=0.7
    )
    
    kb.add_hypothesis(h1)
    kb.add_hypothesis(h2)
    
    # Create Deep Scientific Agent
    agent = DeepScientificAgent(
        domain="Astrophysics", 
        knowledge_base=kb,
        primary_paradigm=ScientificParadigm.BAYESIAN
    )
    
    agent.active_hypotheses = [h1, h2]
    
    print(f"\nInitialized Agent in domain: {agent.domain}")
    print(f"Primary Paradigm: {list(agent.active_paradigms)[0].name}")
    print(f"Active Hypotheses: {len(agent.active_hypotheses)}")
    
    # 2. Run Research Cycle
    print("\n--- Starting Enhanced Research Cycle ---")
    await agent.enhanced_research_cycle(iterations=3)
    
    # 3. Display Results
    print("\n--- Research Results ---")
    
    # Quantum States
    print(f"\nQuantum Interpretations Generated: {len(agent.quantum_interpretations)}")
    if agent.quantum_reasoner.hypothesis_superpositions:
        print("Hypothesis Superpositions:")
        for hid, state in agent.quantum_reasoner.hypothesis_superpositions.items():
            print(f"  - {hid}: Prob={state.probability():.2f}")
    
    # Hermeneutic History
    print(f"\nHermeneutic Circles Conducted: {len(agent.hermeneutic_interpreter.hermeneutic_circles)}")
    print(f"Current Horizon Tradition: {agent.hermeneutic_interpreter.current_horizon.tradition.name}")
    
    # Paradigm Shifts
    if agent.paradigm_shifts:
        print(f"\nParadigm Shifts: {len(agent.paradigm_shifts)}")
        for shift in agent.paradigm_shifts:
            print(f"  - Shifted from {shift['from']} to {shift['to']} due to {shift['reason']}")
            
    # 4. Visualization
    # Note: Requires matplotlib, skipped if not available/headless
    try:
        viz = EnhancedScientificVisualizer(agent)
        # Uncomment to show/save
        # viz.visualize_quantum_states("quantum_states.png")
        # viz.visualize_knowledge_graph("knowledge_graph.png")
        print("\nVisualizers initialized (see code to enable saving plots)")
    except Exception as e:
        print(f"Visualization skipped: {e}")

if __name__ == "__main__":
    asyncio.run(main())
