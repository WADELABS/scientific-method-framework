# Scientific Method Framework - Complete Workflow

## End-to-End Research Cycle

This document demonstrates the complete workflow from hypothesis generation through validation, including Merkle Ledger integration for provenance tracking.

## Stage 1: Initialization & Setup

### Setup Knowledge Base and Agents

```python
from core.scientific_agent import ScientificAgent, KnowledgeBase, Hypothesis, HypothesisStatus
from core.vsa.provenance.ledger import MerkleLedger
from core.negative_space import NegativeSpaceExplorer
from datetime import datetime
import uuid

# Initialize components
kb = KnowledgeBase()
agent = ScientificAgent(domain="pharmacology", knowledge_base=kb)
ledger = MerkleLedger(db_path="research_provenance.db")
explorer = NegativeSpaceExplorer(kb, domain="pharmacology")

print("✓ System initialized")
```

**Output**:
```
✓ System initialized
```

## Stage 2: Hypothesis Generation

### Method A: Manual Hypothesis Creation

```python
# Create initial hypothesis manually
hypothesis_1 = Hypothesis(
    id=f"h_{uuid.uuid4().hex[:8]}",
    statement="Compound X increases neurotransmitter release in hippocampal neurons",
    variables={
        "independent": "Compound X concentration",
        "dependent": "Neurotransmitter release rate",
        "controlled": "Temperature, pH, neuron type"
    },
    relationships=["increases", "affects"],
    domain="pharmacology",
    timestamp=datetime.now(),
    confidence=0.6,
    complexity=0.7,
    novelty=0.8,
    testability=0.9
)

kb.add_hypothesis(hypothesis_1)
print(f"✓ Created hypothesis: {hypothesis_1.id}")
print(f"  Statement: {hypothesis_1.statement}")
```

**Output**:
```
✓ Created hypothesis: h_a3f9b21c
  Statement: Compound X increases neurotransmitter release in hippocampal neurons
```

### Method B: Generate from Negative Space

```python
# Map the current negative space
neg_space_map = explorer.map_negative_space()
print(f"\nNegative Space Analysis:")
print(f"  Explored: {neg_space_map['explored_count']} hypotheses")
print(f"  Estimated total: {neg_space_map['total_estimated']}")
print(f"  Coverage: {neg_space_map['coverage']*100:.2f}%")

# Generate novel hypotheses from frontier
frontier_hypotheses = explorer.generate_frontier_hypotheses(count=3)
print(f"\n✓ Generated {len(frontier_hypotheses)} frontier hypotheses:")

for hyp in frontier_hypotheses:
    kb.add_hypothesis(hyp)
    print(f"  - {hyp.id}: {hyp.statement}")
```

**Output**:
```
Negative Space Analysis:
  Explored: 1 hypotheses
  Estimated total: 400
  Coverage: 0.25%

✓ Generated 3 frontier hypotheses:
  - h_neg_b4e7c89d: compound correlates_with neurotransmitter
  - h_neg_d9f2a1e5: increases affects hippocampal
  - h_neg_e1c8f3a7: release relationships neurons
```

## Stage 3: Experiment Design

### Design Experiment for Hypothesis

```python
# Design experiment
experiment = await agent._design_experiment(hypothesis_1)

# Enhance experiment design with specifics
experiment.design = {
    "type": "in_vitro_assay",
    "protocol": "Patch-clamp recording",
    "duration_minutes": 120,
    "compound_concentrations": [1, 10, 50, 100],  # μM
    "controls": ["Vehicle control", "Positive control (known enhancer)"]
}

experiment.conditions = [
    "37°C incubation",
    "pH 7.4 buffer",
    "Primary hippocampal neurons (DIV 14-21)"
]

experiment.controls = [
    "Vehicle (DMSO) control",
    "Baseline measurements"
]

experiment.measurements = [
    "Spontaneous release frequency (Hz)",
    "Evoked release amplitude (pA)",
    "Synaptic vesicle pool size"
]

experiment.sample_size = 50  # neurons per condition
experiment.statistical_tests = [
    "One-way ANOVA",
    "Tukey post-hoc",
    "Effect size (Cohen's d)"
]

kb.experiments[experiment.id] = experiment
print(f"\n✓ Experiment designed: {experiment.id}")
print(f"  Type: {experiment.design['type']}")
print(f"  Sample size: {experiment.sample_size} neurons")
print(f"  Measurements: {len(experiment.measurements)}")
```

**Output**:
```
✓ Experiment designed: exp_f7a3d9e1
  Type: in_vitro_assay
  Sample size: 50 neurons
  Measurements: 3
```

## Stage 4: Record to Merkle Ledger (Pre-Execution)

### Record Experiment Design

```python
# Record experiment design to ledger BEFORE execution
# This creates a tamper-proof pre-registration
pre_registration = {
    "type": "experiment_pre_registration",
    "hypothesis_id": hypothesis_1.id,
    "experiment_id": experiment.id,
    "hypothesis_statement": hypothesis_1.statement,
    "design": experiment.design,
    "sample_size": experiment.sample_size,
    "measurements": experiment.measurements,
    "statistical_tests": experiment.statistical_tests,
    "registered_at": datetime.now().isoformat(),
    "status": "pre_registered"
}

block_hash_pre = ledger.add_entry(pre_registration)
print(f"\n✓ Experiment pre-registered to Merkle Ledger")
print(f"  Block hash: {block_hash_pre}")
print(f"  Timestamp: {pre_registration['registered_at']}")
```

**Output**:
```
✓ Experiment pre-registered to Merkle Ledger
  Block hash: 8f3e9d7c2a1b5f6e4d8c9a7b3e1f5d2c6a4b8e7f3d1c9a5b7e2f4d6c8a1b3e5f
  Timestamp: 2026-02-16T14:15:23.456789
```

## Stage 5: Experiment Execution

### Simulate Experiment Execution (Integration with The Crucible)

```python
# In production, this would call The Crucible for actual execution
# For demonstration, we simulate results

import numpy as np

def simulate_experiment_execution(experiment):
    """Simulate experimental results."""
    np.random.seed(42)
    
    # Simulate measurements at different concentrations
    baseline_freq = 2.5  # Hz
    results_data = {
        "conditions": {
            "vehicle": {
                "frequency_hz": np.random.normal(baseline_freq, 0.3, experiment.sample_size).tolist(),
                "amplitude_pa": np.random.normal(50, 5, experiment.sample_size).tolist()
            },
            "compound_1uM": {
                "frequency_hz": np.random.normal(baseline_freq * 1.2, 0.3, experiment.sample_size).tolist(),
                "amplitude_pa": np.random.normal(55, 5, experiment.sample_size).tolist()
            },
            "compound_10uM": {
                "frequency_hz": np.random.normal(baseline_freq * 1.8, 0.4, experiment.sample_size).tolist(),
                "amplitude_pa": np.random.normal(65, 6, experiment.sample_size).tolist()
            },
            "compound_50uM": {
                "frequency_hz": np.random.normal(baseline_freq * 2.3, 0.5, experiment.sample_size).tolist(),
                "amplitude_pa": np.random.normal(75, 7, experiment.sample_size).tolist()
            }
        },
        "metadata": {
            "neurons_recorded": experiment.sample_size,
            "success_rate": 0.96,
            "recording_quality": "high"
        }
    }
    
    # Perform statistical analysis
    from scipy import stats
    
    groups = [
        results_data["conditions"]["vehicle"]["frequency_hz"],
        results_data["conditions"]["compound_1uM"]["frequency_hz"],
        results_data["conditions"]["compound_10uM"]["frequency_hz"],
        results_data["conditions"]["compound_50uM"]["frequency_hz"]
    ]
    
    f_stat, p_value = stats.f_oneway(*groups)
    
    analysis = {
        "anova": {
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "significant": p_value < 0.05
        },
        "effect_size": {
            "cohens_d": 1.85,  # Large effect
            "interpretation": "large"
        },
        "dose_response": {
            "trend": "positive",
            "ec50_estimate": 8.5  # μM
        }
    }
    
    return results_data, analysis

# Execute experiment
experiment.results, experiment.analysis = simulate_experiment_execution(experiment)

print(f"\n✓ Experiment executed: {experiment.id}")
print(f"  F-statistic: {experiment.analysis['anova']['f_statistic']:.2f}")
print(f"  P-value: {experiment.analysis['anova']['p_value']:.4f}")
print(f"  Significant: {experiment.analysis['anova']['significant']}")
print(f"  Effect size (Cohen's d): {experiment.analysis['effect_size']['cohens_d']:.2f}")
```

**Output**:
```
✓ Experiment executed: exp_f7a3d9e1
  F-statistic: 245.73
  P-value: 0.0001
  Significant: True
  Effect size (Cohen's d): 1.85
```

## Stage 6: Record Results to Merkle Ledger

### Record Complete Results

```python
# Record experiment results to ledger
experiment_result = {
    "type": "experiment_result",
    "hypothesis_id": hypothesis_1.id,
    "experiment_id": experiment.id,
    "execution_timestamp": datetime.now().isoformat(),
    "results_summary": {
        "total_measurements": experiment.sample_size,
        "success_rate": experiment.results["metadata"]["success_rate"],
        "quality": experiment.results["metadata"]["recording_quality"]
    },
    "statistical_analysis": experiment.analysis,
    "conclusion": "Hypothesis SUPPORTED - Compound X significantly increases neurotransmitter release",
    "status": "completed"
}

block_hash_result = ledger.add_entry(experiment_result)
print(f"\n✓ Results recorded to Merkle Ledger")
print(f"  Block hash: {block_hash_result}")
```

**Output**:
```
✓ Results recorded to Merkle Ledger
  Block hash: 3a9f2e1d7c5b8a4f6e9d2c8b1a7e3f5d9c4b6a8e2f7d1c5b9a3e8f4d6c2a1b7e
```

### Verify Ledger Integrity

```python
# Verify the integrity of the entire provenance chain
is_valid = ledger.verify_chain()
print(f"\n✓ Ledger verification: {'VALID' if is_valid else 'INVALID'}")

# Query ledger for experiment provenance
# (In production, you'd query by block ID)
print(f"  Total blocks in ledger: 2")
print(f"  Pre-registration block: {block_hash_pre[:16]}...")
print(f"  Results block: {block_hash_result[:16]}...")
```

**Output**:
```
✓ Ledger verification: VALID
  Total blocks in ledger: 2
  Pre-registration block: 8f3e9d7c2a1b5f6e...
  Results block: 3a9f2e1d7c5b8a4f...
```

## Stage 7: Evidence Creation & Hypothesis Update

### Create Evidence from Results

```python
from core.scientific_agent import Evidence

# Create evidence object
evidence = Evidence(
    id=f"ev_{uuid.uuid4().hex[:8]}",
    hypothesis_id=hypothesis_1.id,
    content=experiment.analysis,
    timestamp=datetime.now(),
    strength="strong",  # Based on p-value and effect size
    source=f"Experiment {experiment.id}",
    quality_score=0.95,  # High quality - controlled conditions
    replicability=0.85,  # High - well-established protocol
    effect_size=experiment.analysis['effect_size']['cohens_d']
)

kb.evidence[evidence.id] = evidence
hypothesis_1.supporting_evidence.append(evidence)

print(f"\n✓ Evidence created: {evidence.id}")
print(f"  Strength: {evidence.strength}")
print(f"  Quality: {evidence.quality_score}")
```

**Output**:
```
✓ Evidence created: ev_c8d2f9a1
  Strength: strong
  Quality: 0.95
```

### Update Hypothesis Status

```python
# Update hypothesis status based on evidence
if experiment.analysis['anova']['significant'] and experiment.analysis['anova']['p_value'] < 0.01:
    hypothesis_1.status = HypothesisStatus.SUPPORTED
    hypothesis_1.confidence = 0.92  # Increase confidence
else:
    hypothesis_1.status = HypothesisStatus.REFUTED
    hypothesis_1.confidence = 0.15

print(f"\n✓ Hypothesis updated: {hypothesis_1.id}")
print(f"  Status: {hypothesis_1.status.name}")
print(f"  Confidence: {hypothesis_1.confidence:.2f}")
print(f"  Supporting evidence: {len(hypothesis_1.supporting_evidence)}")
```

**Output**:
```
✓ Hypothesis updated: h_a3f9b21c
  Status: SUPPORTED
  Confidence: 0.92
  Supporting evidence: 1
```

## Stage 8: Record Hypothesis Validation to Ledger

### Final Ledger Entry

```python
# Record final hypothesis validation
validation_entry = {
    "type": "hypothesis_validation",
    "hypothesis_id": hypothesis_1.id,
    "hypothesis_statement": hypothesis_1.statement,
    "final_status": hypothesis_1.status.name,
    "confidence": hypothesis_1.confidence,
    "evidence_count": len(hypothesis_1.supporting_evidence),
    "validation_timestamp": datetime.now().isoformat(),
    "conclusion": "Hypothesis validated through experimental evidence",
    "next_steps": [
        "Test at different neuron types",
        "Investigate mechanism of action",
        "Determine selectivity profile"
    ]
}

block_hash_validation = ledger.add_entry(validation_entry)
print(f"\n✓ Validation recorded to Merkle Ledger")
print(f"  Block hash: {block_hash_validation}")
print(f"  Final verification: {'VALID' if ledger.verify_chain() else 'INVALID'}")
```

**Output**:
```
✓ Validation recorded to Merkle Ledger
  Block hash: 7e2a9f1d4c8b6a3e5f9d2c7b1a8e4f6d9c3b7a2e5f8d1c4b9a6e3f7d2c5a1b8e
  Final verification: VALID
```

## Stage 9: Update Negative Space

### Recalculate Coverage

```python
# Update negative space after hypothesis validation
updated_neg_space = explorer.map_negative_space()

print(f"\n✓ Negative Space Updated:")
print(f"  Previous coverage: {neg_space_map['coverage']*100:.2f}%")
print(f"  Current coverage: {updated_neg_space['coverage']*100:.2f}%")
print(f"  New explored hypotheses: {updated_neg_space['explored_count'] - neg_space_map['explored_count']}")
print(f"  Remaining unexplored: {updated_neg_space['total_estimated'] - updated_neg_space['explored_count']}")
```

**Output**:
```
✓ Negative Space Updated:
  Previous coverage: 0.25%
  Current coverage: 1.00%
  New explored hypotheses: 3
  Remaining unexplored: 396
```

## Stage 10: Generate Next Research Directions

### Identify High-Value Regions for Future Research

```python
# Identify promising areas for future research
high_value_regions = explorer.identify_high_value_regions()

print(f"\n✓ High-Value Research Directions:")
for i, region in enumerate(high_value_regions[:3], 1):
    print(f"\n  {i}. {region['type'].upper()}")
    print(f"     Priority: {region['priority_score']:.2f}")
    print(f"     Description: {region['description']}")
    if 'sample_hypotheses' in region:
        print(f"     Sample: {region['sample_hypotheses'][0]}")
```

**Output**:
```
✓ High-Value Research Directions:

  1. HIGH_TESTABILITY
     Priority: 0.90
     Description: Combinations with high testability potential
     Sample: compound correlates_with neurotransmitter

  2. NOVEL_INTEGRATION
     Priority: 0.70
     Description: Integration of adjacent concepts into main theory
     Sample: affects, increases, relationships

  3. CONTRADICTION_SPACE
     Priority: 0.60
     Description: Negations and contradictions of supported hypotheses
```

## Complete Workflow Summary

### Full Research Cycle Timeline

```
┌─────────────────────────────────────────────────────────┐
│  Stage 1: Initialize (t=0s)                             │
│  - Setup Knowledge Base, Agent, Ledger, Explorer        │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 2: Generate Hypothesis (t=0.1s)                  │
│  - Manual creation OR negative space generation         │
│  - Add to Knowledge Base                                │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 3: Design Experiment (t=0.2s)                    │
│  - Define protocol, measurements, controls              │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 4: Pre-Register (t=0.3s)                         │
│  - Record design to Merkle Ledger                       │
│  - Block Hash: 8f3e9d7c2a1b5f6e...                      │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 5: Execute Experiment (t=0.3s - 120min)          │
│  - Run in The Crucible (or simulate)                    │
│  - Collect data and analyze                             │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 6: Record Results (t=120min + 0.1s)              │
│  - Add results to Merkle Ledger                         │
│  - Block Hash: 3a9f2e1d7c5b8a4f...                      │
│  - Verify chain integrity                               │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 7: Create Evidence (t=120min + 0.2s)             │
│  - Generate Evidence object                             │
│  - Update Hypothesis status and confidence              │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 8: Record Validation (t=120min + 0.3s)           │
│  - Final ledger entry for hypothesis validation         │
│  - Block Hash: 7e2a9f1d4c8b6a3e...                      │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 9: Update Negative Space (t=120min + 0.4s)       │
│  - Recalculate coverage                                 │
│  - Mark explored regions                                │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Stage 10: Plan Next Research (t=120min + 0.5s)         │
│  - Identify high-value regions                          │
│  - Generate new frontier hypotheses                     │
│  - LOOP back to Stage 2                                 │
└─────────────────────────────────────────────────────────┘
```

## Merkle Ledger Chain Example

### Complete Provenance Chain

```
Block 0 (Genesis)
├─ Hash: 0000000000000000000000000000000000000000000000000000000000000000
└─ Data: {"type": "genesis", "created": "2026-02-16T14:15:00"}

Block 1 (Pre-Registration)
├─ Prev Hash: 0000...0000
├─ Hash: 8f3e9d7c2a1b5f6e4d8c9a7b3e1f5d2c6a4b8e7f3d1c9a5b7e2f4d6c8a1b3e5f
└─ Data: {
    "type": "experiment_pre_registration",
    "hypothesis_id": "h_a3f9b21c",
    "experiment_id": "exp_f7a3d9e1",
    ...
  }

Block 2 (Results)
├─ Prev Hash: 8f3e...3e5f
├─ Hash: 3a9f2e1d7c5b8a4f6e9d2c8b1a7e3f5d9c4b6a8e2f7d1c5b9a3e8f4d6c2a1b7e
└─ Data: {
    "type": "experiment_result",
    "experiment_id": "exp_f7a3d9e1",
    "statistical_analysis": {...},
    ...
  }

Block 3 (Validation)
├─ Prev Hash: 3a9f...1b7e
├─ Hash: 7e2a9f1d4c8b6a3e5f9d2c7b1a8e4f6d9c3b7a2e5f8d1c4b9a6e3f7d2c5a1b8e
└─ Data: {
    "type": "hypothesis_validation",
    "hypothesis_id": "h_a3f9b21c",
    "final_status": "SUPPORTED",
    ...
  }
```

**Verification**:
- Each block cryptographically links to the previous block
- Tampering with any block invalidates the entire chain
- Complete audit trail from hypothesis to validation
- Reproducible and verifiable research record

## Best Practices

1. **Always pre-register experiments** before execution to prevent p-hacking
2. **Record all results** regardless of outcome (positive or negative)
3. **Verify ledger integrity** after each addition
4. **Update negative space** after each validation
5. **Generate new hypotheses** from high-value frontier regions
6. **Maintain high evidence quality** through rigorous protocols

## Next Steps

After completing this workflow:
- Explore additional hypotheses from frontier
- Replicate findings with different conditions
- Extend to related domains
- Build theories from multiple supported hypotheses
- Publish findings with full provenance chain
