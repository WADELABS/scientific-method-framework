"""
Simple Scientific Method Framework Example

Demonstrates the complete SMF cycle:
1. Hypothesis creation
2. Experiment design and execution (via stub Crucible)
3. Validation and theory update
"""

from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.scientific_agent import (
    KnowledgeBase, Hypothesis, Experiment, Evidence, Theory, 
    HypothesisStatus, ScientificAgent
)
from core.foundations import EpistemicVirtue
import random


def create_simple_experiment(hypothesis: Hypothesis) -> Experiment:
    """Create an experiment to test a hypothesis."""
    return Experiment(
        id=f"exp_{hypothesis.id}",
        hypothesis_id=hypothesis.id,
        design={"type": "simulation", "parameters": hypothesis.variables},
        conditions=["baseline", "modified"],
        controls=["temperature", "environment"],
        measurements=["success_rate", "latency", "error_count"],
        sample_size=100,
        randomization_procedure="random_assignment",
        statistical_tests=["t_test", "chi_square"]
    )


def run_stub_crucible(experiment: Experiment) -> dict:
    """
    Stub implementation of The Crucible experiment execution.
    Simulates running an experiment and returning results.
    """
    print(f"  🔬 Running experiment in The Crucible (sandboxed environment)...")
    print(f"     - Design: {experiment.design['type']}")
    print(f"     - Sample size: {experiment.sample_size}")
    print(f"     - Measurements: {', '.join(experiment.measurements)}")

    # Constants
    BASELINE_SUCCESS_RATE = 0.5

    # Simulate experiment execution with realistic results
    # In a real implementation, this would run actual code in a sandbox
    success_rate = random.uniform(0.75, 0.95)
    latency_ms = random.uniform(100, 300)
    error_count = random.randint(0, 5)

    results = {
        "success_rate": success_rate,
        "latency_ms": latency_ms,
        "error_count": error_count,
        "sample_size": experiment.sample_size,
        "statistical_significance": success_rate > 0.8,
        "baseline_success_rate": BASELINE_SUCCESS_RATE
    }

    print(f"     ✓ Experiment completed")
    print(f"       - Success rate: {success_rate:.2%}")
    print(f"       - Latency: {latency_ms:.1f}ms")
    print(f"       - Errors: {error_count}")

    return results


def main():
    print("=" * 70)
    print("Scientific Method Framework - Simple Example")
    print("=" * 70)
    print()
    
    # Step 1: Create Knowledge Base and Hypothesis
    print("Step 1: Hypothesis Generation")
    print("-" * 70)
    
    kb = KnowledgeBase()
    hypothesis = Hypothesis(
        id="h_timeout_fix",
        statement="Increasing timeout to 300s will reduce transaction failures",
        variables={"timeout": "300s", "failure_rate": "low"},
        relationships=["timeout_affects_success"],
        domain="system_performance",
        timestamp=datetime.now(),
        confidence=0.7,
        complexity=0.3,
        novelty=0.5,
        testability=0.9
    )
    kb.add_hypothesis(hypothesis)
    
    print(f"Hypothesis: {hypothesis.statement}")
    print(f"  - Domain: {hypothesis.domain}")
    print(f"  - Testability: {hypothesis.testability}")
    print(f"  - Confidence: {hypothesis.confidence}")
    print(f"  - Status: {hypothesis.status.name}")
    print()
    
    # Step 2: Create Scientific Agent
    print("Step 2: Initialize Scientific Agent")
    print("-" * 70)
    
    agent = ScientificAgent(domain="System Performance", knowledge_base=kb)
    agent.active_hypotheses.append(hypothesis)
    
    print(f"Agent initialized in domain: {agent.domain}")
    print(f"Active hypotheses: {len(agent.active_hypotheses)}")
    print()
    
    # Step 3: Design and Run Experiment
    print("Step 3: Experiment Execution")
    print("-" * 70)
    
    hypothesis.status = HypothesisStatus.TESTING
    experiment = create_simple_experiment(hypothesis)
    kb.experiments[experiment.id] = experiment
    
    print(f"Experiment designed: {experiment.id}")
    results = run_stub_crucible(experiment)
    
    # Record results
    experiment.results = results
    experiment.analysis = {
        "conclusion": "supported" if results["success_rate"] > 0.8 else "refuted",
        "confidence": results["success_rate"],
        "statistical_significance": results["statistical_significance"]
    }
    print()
    
    # Step 4: Validation and Theory Update
    print("Step 4: Validation and Theory Update")
    print("-" * 70)
    
    if results["success_rate"] > 0.8 and results["statistical_significance"]:
        hypothesis.status = HypothesisStatus.SUPPORTED
        print(f"✓ Hypothesis VALIDATED: {hypothesis.statement}")
        print(f"  Success rate ({results['success_rate']:.2%}) exceeds threshold (80%)")
        
        # Create evidence
        evidence = Evidence(
            id=f"ev_{experiment.id}",
            hypothesis_id=hypothesis.id,
            content=results,
            timestamp=datetime.now(),
            strength="strong",
            source=experiment.id,
            quality_score=0.9,
            replicability=0.85,
            effect_size=results["success_rate"] - results.get("baseline_success_rate", 0.5)
        )
        hypothesis.supporting_evidence.append(evidence)
        kb.evidence[evidence.id] = evidence
        
        # Update theory
        theory = Theory(
            id="theory_timeout_performance",
            name="Timeout Configuration Theory",
            core_principles=[
                "Adequate timeout values prevent premature termination",
                "Transaction success rate correlates with timeout duration"
            ],
            explanatory_scope=["system_performance", "transaction_processing"],
            predictive_power=0.85,
            parsimony=0.8,
            coherence=0.9,
            empirical_support=0.85,
            hypotheses=[hypothesis],
            evidence=[evidence]
        )
        kb.add_theory(theory)
        
        print(f"\n  Theory updated: '{theory.name}'")
        print(f"  - Predictive power: {theory.predictive_power}")
        print(f"  - Empirical support: {theory.empirical_support}")
        
    else:
        hypothesis.status = HypothesisStatus.REFUTED
        print(f"✗ Hypothesis REFUTED: {hypothesis.statement}")
        print(f"  Success rate ({results['success_rate']:.2%}) below threshold (80%)")
        print(f"  Further investigation needed to identify root cause")
    
    print()
    
    # Step 5: Summary
    print("Step 5: Summary")
    print("-" * 70)
    print(f"Knowledge Base Status:")
    print(f"  - Hypotheses: {len(kb.hypotheses)}")
    print(f"  - Experiments: {len(kb.experiments)}")
    print(f"  - Evidence: {len(kb.evidence)}")
    print(f"  - Theories: {len(kb.theories)}")
    print()
    print("SMF Cycle Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
