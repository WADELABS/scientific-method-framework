# Integration Guide

This guide shows you how to integrate the Scientific Method Framework (SMF) into your projects, whether you're building autonomous agents, validation pipelines, or research systems.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Integration Patterns](#integration-patterns)
5. [Using as a Library](#using-as-a-library)
6. [Common Use Cases](#common-use-cases)
7. [Best Practices](#best-practices)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)

---

## Installation

### From GitHub Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/scientific-method-framework.git
cd scientific-method-framework

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from core.scientific_agent import ScientificAgent; print('✓ SMF installed successfully')"
```

### Using pip (Direct from Git)

```bash
pip install git+https://github.com/yourusername/scientific-method-framework.git
```

### Development Installation

```bash
# Clone and install in editable mode
git clone https://github.com/yourusername/scientific-method-framework.git
cd scientific-method-framework
pip install -e .
```

### Dependencies

The SMF requires Python 3.9+ and the following packages:

```
numpy>=1.20.0
networkx>=2.6.0
pandas>=1.3.0
scipy>=1.7.0
dataclasses-json>=0.5.0
```

**Optional dependencies:**
- `pytest>=7.0.0` - For running tests
- `flake8>=6.0.0` - For code quality checks

---

## Quick Start

### 5-Minute Example

Create a file `my_first_smf.py`:

```python
from core.scientific_agent import (
    KnowledgeBase, Hypothesis, Experiment, Evidence,
    HypothesisStatus, ScientificAgent
)
from datetime import datetime

# Step 1: Initialize Knowledge Base
kb = KnowledgeBase()

# Step 2: Create a Hypothesis
hypothesis = Hypothesis(
    id="h_api_timeout",
    statement="Increasing API timeout from 30s to 60s reduces failure rate by 50%",
    variables={
        "timeout": "60s",
        "failure_rate": "reduced"
    },
    relationships=["timeout_affects_failure_rate"],
    domain="api_performance",
    timestamp=datetime.now(),
    confidence=0.75,
    complexity=0.3,
    novelty=0.5,
    testability=0.95
)
kb.add_hypothesis(hypothesis)

# Step 3: Create Scientific Agent
agent = ScientificAgent(domain="API Performance", knowledge_base=kb)

# Step 4: Design an Experiment
experiment = Experiment(
    id="exp_api_timeout_test",
    hypothesis_id=hypothesis.id,
    design={
        "type": "ab_test",
        "parameters": {"baseline": "30s", "treatment": "60s"}
    },
    conditions=["baseline_30s", "treatment_60s"],
    controls=["server_load", "time_of_day"],
    measurements=["failure_rate", "latency"],
    sample_size=1000,
    randomization_procedure="random_assignment",
    statistical_tests=["chi_square", "t_test"]
)
kb.experiments[experiment.id] = experiment

# Step 5: Simulate Experiment Results (replace with real execution)
experiment.results = {
    "baseline_failure_rate": 0.20,
    "treatment_failure_rate": 0.10,
    "p_value": 0.001,
    "confidence_interval": [0.08, 0.12]
}

# Step 6: Validate and Update
if experiment.results["treatment_failure_rate"] < experiment.results["baseline_failure_rate"] * 0.5:
    hypothesis.status = HypothesisStatus.SUPPORTED
    
    evidence = Evidence(
        id=f"ev_{experiment.id}",
        hypothesis_id=hypothesis.id,
        content=experiment.results,
        timestamp=datetime.now(),
        strength="strong",
        source=experiment.id,
        quality_score=0.9,
        replicability=0.85,
        effect_size=0.50
    )
    hypothesis.supporting_evidence.append(evidence)
    kb.evidence[evidence.id] = evidence
    
    print(f"✓ Hypothesis SUPPORTED: {hypothesis.statement}")
else:
    hypothesis.status = HypothesisStatus.REFUTED
    print(f"✗ Hypothesis REFUTED")

print(f"\nKnowledge Base Summary:")
print(f"  Hypotheses: {len(kb.hypotheses)}")
print(f"  Experiments: {len(kb.experiments)}")
print(f"  Evidence: {len(kb.evidence)}")
```

Run it:
```bash
python my_first_smf.py
```

Expected output:
```
✓ Hypothesis SUPPORTED: Increasing API timeout from 30s to 60s reduces failure rate by 50%

Knowledge Base Summary:
  Hypotheses: 1
  Experiments: 1
  Evidence: 1
```

---

## Core Concepts

### The Scientific Method Loop

The SMF implements a rigorous validation cycle:

```
┌─────────────────┐
│ 1. HYPOTHESIS   │  Create testable prediction
│    Generation   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. EXPERIMENT   │  Design controlled test
│    Design       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. EXECUTION    │  Run in The Crucible (sandbox)
│    (Crucible)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. VALIDATION   │  Compare results vs predictions
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. THEORY       │  Update knowledge base
│    Update       │
└─────────────────┘
```

### Key Components

1. **Hypothesis**: A testable prediction about system behavior
2. **Experiment**: A controlled test to validate the hypothesis
3. **Evidence**: Observational data supporting or refuting a hypothesis
4. **Theory**: A well-supported explanatory framework
5. **KnowledgeBase**: Central storage for all scientific artifacts
6. **ScientificAgent**: Orchestrates the research cycle

---

## Integration Patterns

### Pattern 1: Autonomous Agent Validation

Use SMF to validate AI agent actions before execution:

```python
from core.scientific_agent import *
from datetime import datetime

class ValidatedAgent:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.smf_agent = ScientificAgent(
            domain="Agent Actions",
            knowledge_base=self.kb
        )
    
    def propose_action(self, action_description: str, context: dict) -> Hypothesis:
        """Convert agent intent into testable hypothesis."""
        hypothesis = Hypothesis(
            id=f"h_{action_description.replace(' ', '_')}_{datetime.now().timestamp()}",
            statement=f"Action '{action_description}' will achieve desired outcome",
            variables=context,
            relationships=[f"{k}_affects_outcome" for k in context.keys()],
            domain="agent_actions",
            timestamp=datetime.now(),
            confidence=0.6,
            complexity=self._estimate_complexity(context),
            novelty=0.5,
            testability=0.8
        )
        self.kb.add_hypothesis(hypothesis)
        return hypothesis
    
    def validate_action(self, hypothesis: Hypothesis) -> bool:
        """Validate action in sandbox before real execution."""
        experiment = Experiment(
            id=f"exp_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={"type": "simulation", "sandbox": True},
            conditions=["baseline", "proposed_action"],
            controls=list(hypothesis.variables.keys()),
            measurements=["success", "safety", "efficiency"],
            sample_size=10,
            randomization_procedure="controlled",
            statistical_tests=["safety_check"]
        )
        
        # Run in sandbox (The Crucible)
        results = self._run_in_crucible(experiment)
        
        # Validate results
        if results["success"] and results["safety"] > 0.9:
            hypothesis.status = HypothesisStatus.SUPPORTED
            return True
        else:
            hypothesis.status = HypothesisStatus.REFUTED
            return False
    
    def _estimate_complexity(self, context: dict) -> float:
        """Estimate action complexity from context."""
        return min(1.0, len(context) * 0.1)
    
    def _run_in_crucible(self, experiment: Experiment) -> dict:
        """Execute experiment in sandboxed environment."""
        # Implement your sandbox execution here
        return {
            "success": True,
            "safety": 0.95,
            "efficiency": 0.85
        }


# Usage
agent = ValidatedAgent()
hypothesis = agent.propose_action(
    "deploy_new_model",
    context={"model_version": "v2.0", "traffic": "10%"}
)

if agent.validate_action(hypothesis):
    print("✓ Action validated - safe to execute")
    # Execute real action
else:
    print("✗ Action failed validation - do not execute")
```

### Pattern 2: A/B Testing Integration

Integrate SMF with A/B testing frameworks:

```python
from core.scientific_agent import *
from datetime import datetime

class ABTestIntegration:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.agent = ScientificAgent("AB Testing", kb)
    
    def create_test_hypothesis(
        self,
        feature_name: str,
        expected_improvement: float,
        metric: str
    ) -> Hypothesis:
        """Create hypothesis from A/B test parameters."""
        return Hypothesis(
            id=f"h_ab_{feature_name}",
            statement=f"Feature '{feature_name}' improves {metric} by {expected_improvement*100}%",
            variables={
                "feature": feature_name,
                "metric": metric,
                "expected_lift": str(expected_improvement)
            },
            relationships=[f"{feature_name}_affects_{metric}"],
            domain="product_features",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.4,
            novelty=0.7,
            testability=1.0
        )
    
    def run_ab_test(
        self,
        hypothesis: Hypothesis,
        duration_days: int,
        traffic_split: float = 0.5
    ) -> Experiment:
        """Execute A/B test as SMF experiment."""
        experiment = Experiment(
            id=f"exp_ab_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={
                "type": "ab_test",
                "duration_days": duration_days,
                "traffic_split": traffic_split
            },
            conditions=["control", "treatment"],
            controls=["user_segment", "time_of_day", "platform"],
            measurements=["conversion_rate", "engagement", "revenue"],
            sample_size=10000,
            randomization_procedure="stratified_random_assignment",
            statistical_tests=["chi_square", "bayesian_ab"]
        )
        
        self.kb.experiments[experiment.id] = experiment
        return experiment
    
    def analyze_results(self, experiment: Experiment, results: dict):
        """Analyze A/B test results and update hypothesis."""
        hypothesis = self.kb.hypotheses[experiment.hypothesis_id]
        
        # Statistical analysis
        control_rate = results["control_conversion_rate"]
        treatment_rate = results["treatment_conversion_rate"]
        p_value = results["p_value"]
        
        experiment.results = results
        experiment.analysis = {
            "conclusion": "supported" if treatment_rate > control_rate and p_value < 0.05 else "refuted",
            "confidence": treatment_rate,
            "statistical_significance": p_value < 0.05,
            "p_value": p_value,
            "lift": (treatment_rate - control_rate) / control_rate
        }
        
        if experiment.analysis["conclusion"] == "supported":
            hypothesis.status = HypothesisStatus.SUPPORTED
            
            evidence = Evidence(
                id=f"ev_{experiment.id}",
                hypothesis_id=hypothesis.id,
                content=results,
                timestamp=datetime.now(),
                strength="strong" if p_value < 0.01 else "moderate",
                source=experiment.id,
                quality_score=0.9,
                replicability=0.8,
                effect_size=experiment.analysis["lift"]
            )
            hypothesis.supporting_evidence.append(evidence)
            self.kb.evidence[evidence.id] = evidence
        else:
            hypothesis.status = HypothesisStatus.REFUTED
        
        return experiment.analysis


# Usage
kb = KnowledgeBase()
ab_integration = ABTestIntegration(kb)

# Create hypothesis
hypothesis = ab_integration.create_test_hypothesis(
    feature_name="new_checkout_flow",
    expected_improvement=0.15,
    metric="conversion_rate"
)
kb.add_hypothesis(hypothesis)

# Run test
experiment = ab_integration.run_ab_test(hypothesis, duration_days=14)

# Simulate results (replace with real data)
results = {
    "control_conversion_rate": 0.12,
    "treatment_conversion_rate": 0.14,
    "p_value": 0.003,
    "sample_size_control": 5000,
    "sample_size_treatment": 5000
}

# Analyze
analysis = ab_integration.analyze_results(experiment, results)
print(f"Test Result: {analysis['conclusion']}")
print(f"Lift: {analysis['lift']*100:.1f}%")
```

### Pattern 3: ML Model Validation

Validate machine learning models before deployment:

```python
from core.scientific_agent import *
from datetime import datetime

class MLModelValidator:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.agent = ScientificAgent("ML Validation", self.kb)
    
    def create_model_hypothesis(
        self,
        model_name: str,
        baseline_metric: float,
        expected_metric: float,
        metric_name: str = "accuracy"
    ) -> Hypothesis:
        """Create hypothesis for model improvement."""
        return Hypothesis(
            id=f"h_model_{model_name}",
            statement=f"Model '{model_name}' improves {metric_name} from {baseline_metric} to {expected_metric}",
            variables={
                "model": model_name,
                "baseline": str(baseline_metric),
                "target": str(expected_metric),
                "metric": metric_name
            },
            relationships=["model_improves_metric"],
            domain="machine_learning",
            timestamp=datetime.now(),
            confidence=0.7,
            complexity=0.6,
            novelty=0.8,
            testability=1.0
        )
    
    def validate_model(
        self,
        hypothesis: Hypothesis,
        model,
        test_data,
        validation_data
    ) -> bool:
        """Validate model through rigorous testing."""
        
        # Create experiment
        experiment = Experiment(
            id=f"exp_validate_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={
                "type": "randomized_control",
                "validation_strategy": "cross_validation",
                "folds": 5
            },
            conditions=["baseline_model", "new_model"],
            controls=["data_distribution", "random_seed"],
            measurements=["accuracy", "precision", "recall", "f1", "auc"],
            sample_size=len(test_data),
            randomization_procedure="stratified_k_fold",
            statistical_tests=["paired_t_test", "mcnemar_test"]
        )
        
        # Run validation
        results = self._run_validation(model, test_data, validation_data)
        experiment.results = results
        
        # Statistical significance check
        baseline = float(hypothesis.variables["baseline"])
        achieved = results["accuracy"]
        target = float(hypothesis.variables["target"])
        
        is_significant = results["p_value"] < 0.05
        meets_target = achieved >= target
        
        experiment.analysis = {
            "conclusion": "supported" if (meets_target and is_significant) else "refuted",
            "confidence": achieved,
            "statistical_significance": is_significant,
            "p_value": results["p_value"],
            "improvement": achieved - baseline
        }
        
        # Update hypothesis
        if experiment.analysis["conclusion"] == "supported":
            hypothesis.status = HypothesisStatus.SUPPORTED
            
            evidence = Evidence(
                id=f"ev_{experiment.id}",
                hypothesis_id=hypothesis.id,
                content=results,
                timestamp=datetime.now(),
                strength="strong",
                source=experiment.id,
                quality_score=0.95,
                replicability=0.9,
                effect_size=experiment.analysis["improvement"]
            )
            hypothesis.supporting_evidence.append(evidence)
            return True
        else:
            hypothesis.status = HypothesisStatus.REFUTED
            return False
    
    def _run_validation(self, model, test_data, validation_data) -> dict:
        """Run actual model validation (implement with your ML framework)."""
        # Placeholder - implement with sklearn, pytorch, tensorflow, etc.
        return {
            "accuracy": 0.92,
            "precision": 0.91,
            "recall": 0.93,
            "f1": 0.92,
            "auc": 0.94,
            "p_value": 0.002
        }


# Usage
validator = MLModelValidator()

hypothesis = validator.create_model_hypothesis(
    model_name="transformer_v2",
    baseline_metric=0.85,
    expected_metric=0.90,
    metric_name="accuracy"
)

# Validate model (replace with real model and data)
if validator.validate_model(hypothesis, model=None, test_data=[], validation_data=[]):
    print("✓ Model validated - safe to deploy")
else:
    print("✗ Model failed validation - do not deploy")
```

---

## Using as a Library

### Basic Import Structure

```python
# Core components
from core.scientific_agent import (
    KnowledgeBase,
    Hypothesis,
    HypothesisStatus,
    Experiment,
    Evidence,
    Theory,
    ScientificAgent
)

# Foundations
from core.foundations import (
    ScientificParadigm,
    EpistemicVirtue,
    ParadigmLens
)

# VSA (Verifiable Scientific Autonomy) - Optional
from core.vsa.logic.engine import FormalLogicEngine
from core.vsa.ledger.merkle import MerkleLedger
```

### Creating a Custom Integration

```python
from core.scientific_agent import *
from datetime import datetime
from typing import Optional, Callable

class CustomSMFIntegration:
    """Template for custom SMF integration."""
    
    def __init__(self, domain: str):
        self.kb = KnowledgeBase()
        self.agent = ScientificAgent(domain, self.kb)
        self.domain = domain
    
    def create_hypothesis_from_intent(
        self,
        intent: str,
        context: dict,
        confidence: float = 0.6
    ) -> Hypothesis:
        """Convert user intent to hypothesis."""
        hypothesis = Hypothesis(
            id=f"h_{len(self.kb.hypotheses)}",
            statement=intent,
            variables=context,
            relationships=self._extract_relationships(intent),
            domain=self.domain,
            timestamp=datetime.now(),
            confidence=confidence,
            complexity=self._estimate_complexity(context),
            novelty=0.5,
            testability=self._estimate_testability(intent)
        )
        self.kb.add_hypothesis(hypothesis)
        return hypothesis
    
    def validate_hypothesis(
        self,
        hypothesis: Hypothesis,
        validator_fn: Callable,
        **kwargs
    ) -> bool:
        """Generic validation with custom validator function."""
        experiment = Experiment(
            id=f"exp_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={"type": "custom", "validator": validator_fn.__name__},
            conditions=["test"],
            controls=list(hypothesis.variables.keys()),
            measurements=["outcome"],
            sample_size=kwargs.get("sample_size", 1),
            randomization_procedure="none",
            statistical_tests=[]
        )
        
        # Run custom validator
        results = validator_fn(hypothesis, **kwargs)
        experiment.results = results
        
        # Determine if supported
        is_supported = results.get("success", False)
        
        if is_supported:
            hypothesis.status = HypothesisStatus.SUPPORTED
            self._add_evidence(hypothesis, experiment, results)
        else:
            hypothesis.status = HypothesisStatus.REFUTED
        
        return is_supported
    
    def _extract_relationships(self, statement: str) -> list:
        """Extract variable relationships from statement."""
        # Simple keyword-based extraction
        keywords = ["affects", "influences", "causes", "improves", "reduces"]
        for keyword in keywords:
            if keyword in statement.lower():
                return [f"extracted_{keyword}_relationship"]
        return ["general_relationship"]
    
    def _estimate_complexity(self, context: dict) -> float:
        """Estimate hypothesis complexity."""
        return min(1.0, len(context) * 0.15)
    
    def _estimate_testability(self, statement: str) -> float:
        """Estimate how testable the hypothesis is."""
        testable_words = ["measure", "test", "validate", "compare", "observe"]
        score = sum(1 for word in testable_words if word in statement.lower())
        return min(1.0, 0.5 + score * 0.1)
    
    def _add_evidence(self, hypothesis: Hypothesis, experiment: Experiment, results: dict):
        """Add evidence to hypothesis."""
        evidence = Evidence(
            id=f"ev_{experiment.id}",
            hypothesis_id=hypothesis.id,
            content=results,
            timestamp=datetime.now(),
            strength="strong" if results.get("confidence", 0) > 0.8 else "moderate",
            source=experiment.id,
            quality_score=results.get("quality", 0.7),
            replicability=results.get("replicability", 0.7)
        )
        hypothesis.supporting_evidence.append(evidence)
        self.kb.evidence[evidence.id] = evidence


# Example usage
integration = CustomSMFIntegration("Custom Domain")

hypothesis = integration.create_hypothesis_from_intent(
    intent="Increasing cache size will improve response time",
    context={"cache_size": "2GB", "response_time": "reduced"}
)

def my_validator(hypothesis, **kwargs):
    # Your custom validation logic
    return {"success": True, "confidence": 0.9, "quality": 0.85}

if integration.validate_hypothesis(hypothesis, my_validator):
    print("✓ Hypothesis validated")
```

---

## Common Use Cases

### Use Case 1: Configuration Change Validation

```python
from core.scientific_agent import *
from datetime import datetime

def validate_config_change(
    config_name: str,
    old_value: any,
    new_value: any,
    expected_improvement: str
):
    """Validate a configuration change before deployment."""
    
    kb = KnowledgeBase()
    
    # Create hypothesis
    hypothesis = Hypothesis(
        id=f"h_config_{config_name}",
        statement=f"Changing {config_name} from {old_value} to {new_value} will {expected_improvement}",
        variables={
            "config": config_name,
            "old_value": str(old_value),
            "new_value": str(new_value)
        },
        relationships=["config_affects_performance"],
        domain="system_configuration",
        timestamp=datetime.now(),
        confidence=0.6,
        complexity=0.3,
        novelty=0.4,
        testability=0.9
    )
    kb.add_hypothesis(hypothesis)
    
    # Design canary deployment experiment
    experiment = Experiment(
        id=f"exp_{hypothesis.id}",
        hypothesis_id=hypothesis.id,
        design={
            "type": "canary",
            "rollout_percentage": 5,
            "duration_minutes": 30
        },
        conditions=["current_config", "new_config"],
        controls=["traffic_type", "region"],
        measurements=["error_rate", "latency_p99", "success_rate"],
        sample_size=1000,
        randomization_procedure="traffic_split",
        statistical_tests=["t_test"]
    )
    
    # Simulate canary deployment
    results = {
        "current_error_rate": 0.02,
        "new_error_rate": 0.01,
        "latency_improvement": 0.15,
        "p_value": 0.01
    }
    
    experiment.results = results
    
    # Validate
    if results["new_error_rate"] < results["current_error_rate"] and results["p_value"] < 0.05:
        hypothesis.status = HypothesisStatus.SUPPORTED
        print(f"✓ Config change validated: {config_name}")
        print(f"  Error rate improvement: {(1 - results['new_error_rate']/results['current_error_rate'])*100:.1f}%")
        return True
    else:
        hypothesis.status = HypothesisStatus.REFUTED
        print(f"✗ Config change rejected: {config_name}")
        return False


# Usage
validate_config_change(
    config_name="connection_pool_size",
    old_value=10,
    new_value=20,
    expected_improvement="reduce connection errors"
)
```

### Use Case 2: Feature Flag Evaluation

```python
from core.scientific_agent import *
from datetime import datetime

class FeatureFlagValidator:
    def __init__(self):
        self.kb = KnowledgeBase()
    
    def evaluate_feature(
        self,
        feature_name: str,
        success_criteria: dict
    ) -> bool:
        """Evaluate if a feature should be fully rolled out."""
        
        hypothesis = Hypothesis(
            id=f"h_feature_{feature_name}",
            statement=f"Feature '{feature_name}' meets success criteria: {success_criteria}",
            variables={
                "feature": feature_name,
                **success_criteria
            },
            relationships=["feature_improves_metrics"],
            domain="product_features",
            timestamp=datetime.now(),
            confidence=0.5,
            complexity=0.5,
            novelty=0.8,
            testability=1.0
        )
        self.kb.add_hypothesis(hypothesis)
        
        # Run progressive rollout experiment
        experiment = Experiment(
            id=f"exp_{hypothesis.id}",
            hypothesis_id=hypothesis.id,
            design={
                "type": "progressive_rollout",
                "stages": [1, 5, 25, 50, 100],
                "stage_duration_hours": 24
            },
            conditions=["feature_off", "feature_on"],
            controls=["user_cohort", "device_type"],
            measurements=list(success_criteria.keys()),
            sample_size=100000,
            randomization_procedure="consistent_hashing",
            statistical_tests=["sequential_testing"]
        )
        
        # Collect metrics (simulated)
        results = {
            "engagement": 1.15,  # 15% improvement
            "retention": 1.08,   # 8% improvement
            "error_rate": 0.98,  # 2% reduction
            "statistical_significance": True
        }
        
        experiment.results = results
        
        # Check all success criteria
        all_met = all(
            results.get(metric, 0) >= threshold
            for metric, threshold in success_criteria.items()
        )
        
        if all_met and results["statistical_significance"]:
            hypothesis.status = HypothesisStatus.SUPPORTED
            print(f"✓ Feature '{feature_name}' validated for full rollout")
            return True
        else:
            hypothesis.status = HypothesisStatus.REFUTED
            print(f"✗ Feature '{feature_name}' does not meet criteria")
            return False


# Usage
validator = FeatureFlagValidator()
validator.evaluate_feature(
    feature_name="new_recommendation_algorithm",
    success_criteria={
        "engagement": 1.10,  # 10% improvement required
        "retention": 1.05,   # 5% improvement required
        "error_rate": 1.0    # No increase in errors
    }
)
```

### Use Case 3: Infrastructure Change Testing

```python
from core.scientific_agent import *
from datetime import datetime

def test_infrastructure_change(
    change_description: str,
    metrics_to_monitor: list,
    acceptable_degradation: dict
):
    """Test infrastructure changes with automatic rollback on failure."""
    
    kb = KnowledgeBase()
    
    hypothesis = Hypothesis(
        id=f"h_infra_{datetime.now().timestamp()}",
        statement=f"Infrastructure change: {change_description}",
        variables={
            "change": change_description,
            **acceptable_degradation
        },
        relationships=["infrastructure_affects_performance"],
        domain="infrastructure",
        timestamp=datetime.now(),
        confidence=0.7,
        complexity=0.7,
        novelty=0.6,
        testability=0.85
    )
    kb.add_hypothesis(hypothesis)
    
    experiment = Experiment(
        id=f"exp_{hypothesis.id}",
        hypothesis_id=hypothesis.id,
        design={
            "type": "blue_green_deployment",
            "monitoring_period_minutes": 60,
            "auto_rollback": True
        },
        conditions=["current_infrastructure", "new_infrastructure"],
        controls=["region", "time_of_day"],
        measurements=metrics_to_monitor,
        sample_size=10000,
        randomization_procedure="traffic_mirroring",
        statistical_tests=["degradation_check"]
    )
    
    # Monitor metrics (simulated)
    results = {
        "latency_p99": 1.05,      # 5% increase (acceptable if threshold is 1.10)
        "error_rate": 0.99,       # 1% improvement
        "throughput": 1.02,       # 2% improvement
        "cpu_utilization": 0.95   # 5% reduction
    }
    
    experiment.results = results
    
    # Check if any metric exceeds acceptable degradation
    rollback_needed = any(
        results.get(metric, 0) > acceptable_degradation.get(metric, 1.0)
        for metric in metrics_to_monitor
    )
    
    if not rollback_needed:
        hypothesis.status = HypothesisStatus.SUPPORTED
        print(f"✓ Infrastructure change validated")
        for metric, value in results.items():
            change_pct = (value - 1.0) * 100
            print(f"  {metric}: {change_pct:+.1f}%")
        return True
    else:
        hypothesis.status = HypothesisStatus.REFUTED
        print(f"✗ Infrastructure change failed - rolling back")
        return False


# Usage
test_infrastructure_change(
    change_description="Migrate to ARM instances",
    metrics_to_monitor=["latency_p99", "error_rate", "throughput"],
    acceptable_degradation={
        "latency_p99": 1.10,   # Max 10% latency increase
        "error_rate": 1.02,    # Max 2% error rate increase
        "throughput": 0.95     # Min -5% throughput (95% of current)
    }
)
```

---

## Best Practices

### 1. Always Define Clear Hypotheses

**Good:**
```python
hypothesis = Hypothesis(
    statement="Increasing database connection pool from 10 to 20 reduces query timeout errors by >50%",
    variables={"pool_size": "20", "timeout_errors": "reduced"},
    testability=0.95
)
```

**Bad:**
```python
hypothesis = Hypothesis(
    statement="Make database better",  # Too vague
    variables={},  # No variables
    testability=0.3  # Not testable
)
```

### 2. Use Appropriate Sample Sizes

```python
# Statistical power calculation
def calculate_sample_size(baseline_rate, expected_improvement, alpha=0.05, power=0.8):
    """Calculate required sample size for statistical significance."""
    from scipy import stats
    # Simplified calculation - use proper statistical methods
    effect_size = expected_improvement / baseline_rate
    return int(1000 * effect_size)  # Placeholder

sample_size = calculate_sample_size(
    baseline_rate=0.10,
    expected_improvement=0.05
)

experiment = Experiment(
    sample_size=sample_size,
    # ... other fields
)
```

### 3. Implement Proper Controls

```python
experiment = Experiment(
    conditions=["baseline", "treatment_a", "treatment_b"],
    controls=[
        "user_segment",      # Control for user type
        "time_of_day",       # Control for temporal effects
        "platform",          # Control for platform differences
        "region"             # Control for geographic effects
    ],
    randomization_procedure="stratified_random_assignment",  # Proper randomization
    # ...
)
```

### 4. Track Evidence Quality

```python
evidence = Evidence(
    content=results,
    quality_score=0.9,      # High quality data
    replicability=0.85,     # Likely to replicate
    effect_size=0.42,       # Meaningful effect
    strength="strong"       # Strong evidence
)

# Only accept high-quality evidence for critical decisions
if evidence.quality_score * evidence.replicability >= 0.7:
    hypothesis.supporting_evidence.append(evidence)
```

### 5. Version Your Knowledge Base

```python
import json
from datetime import datetime

def export_knowledge_base(kb: KnowledgeBase, version: str) -> dict:
    """Export knowledge base with versioning."""
    return {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "hypotheses": {h.id: h for h in kb.hypotheses.values()},
        "experiments": {e.id: e for e in kb.experiments.values()},
        "evidence": {ev.id: ev for ev in kb.evidence.values()},
        "theories": {t.id: t for t in kb.theories.values()}
    }

# Save knowledge base
kb_export = export_knowledge_base(kb, version="1.0.0")
with open(f"kb_v{kb_export['version']}.json", "w") as f:
    json.dump(kb_export, f, default=str, indent=2)
```

### 6. Use The Crucible for Safe Testing

```python
class CrucibleSandbox:
    """Isolated execution environment for experiments."""
    
    def __init__(self, timeout_seconds=300):
        self.timeout = timeout_seconds
        self.isolation_level = "full"
    
    def execute_experiment(self, experiment: Experiment):
        """Execute experiment in isolated sandbox."""
        print(f"🔬 Executing in Crucible (timeout: {self.timeout}s)")
        
        # Sandbox execution
        try:
            # Your sandbox implementation here
            results = self._run_isolated(experiment)
            return results
        except Exception as e:
            print(f"⚠️  Experiment failed safely in sandbox: {e}")
            return {"error": str(e), "success": False}
    
    def _run_isolated(self, experiment):
        # Implement actual sandboxing (Docker, VM, etc.)
        return {"success": True}

# Usage
crucible = CrucibleSandbox(timeout_seconds=300)
results = crucible.execute_experiment(experiment)
```

---

## Advanced Features

### Using VSA (Verifiable Scientific Autonomy)

The VSA subsystem provides formal logic, citations, and provenance tracking:

```python
from core.vsa.logic.engine import FormalLogicEngine
from core.vsa.ledger.merkle import MerkleLedger

# Formal logic validation
logic_engine = FormalLogicEngine()
is_valid = logic_engine.validate_inference(
    premises=["All systems with timeout>60s have low error rates",
              "System X has timeout=300s"],
    conclusion="System X has low error rate"
)

# Cryptographic provenance
ledger = MerkleLedger()
ledger.add_entry({
    "type": "hypothesis_creation",
    "hypothesis_id": hypothesis.id,
    "timestamp": datetime.now().isoformat(),
    "creator": "agent_id_123"
})

# Verify integrity
root_hash = ledger.get_root_hash()
print(f"Provenance chain hash: {root_hash}")
```

### Multi-Paradigm Analysis

```python
from core.foundations import ScientificParadigm, ParadigmLens, EpistemicVirtue

# Analyze hypothesis from different paradigms
paradigms = [
    ParadigmLens(
        paradigm=ScientificParadigm.FALSIFICATIONISM,
        interpretive_priorities=[EpistemicVirtue.TESTABILITY],
        methodological_constraints=["must_be_falsifiable"],
        truth_criteria=["not_yet_falsified"],
        blindnesses=["confirmation_bias"]
    ),
    ParadigmLens(
        paradigm=ScientificParadigm.BAYESIAN,
        interpretive_priorities=[EpistemicVirtue.PREDICTIVE_ACCURACY],
        methodological_constraints=["probabilistic_inference"],
        truth_criteria=["high_posterior_probability"],
        blindnesses=["prior_sensitivity"]
    )
]

for lens in paradigms:
    interpretation = lens.interpret_evidence(evidence)
    print(f"{lens.paradigm.name}: {interpretation}")
```

---

## Troubleshooting

### Common Issues

**Issue: Hypothesis always marked as REFUTED**

```python
# Check testability score
if hypothesis.testability < 0.5:
    print("⚠️  Hypothesis has low testability - reformulate")

# Ensure proper validation logic
if experiment.results and experiment.results.get("p_value", 1.0) < 0.05:
    hypothesis.status = HypothesisStatus.SUPPORTED
```

**Issue: Experiments taking too long**

```python
# Use smaller sample sizes for rapid iteration
experiment.sample_size = 100  # Instead of 10000

# Implement early stopping
if preliminary_results["p_value"] < 0.001:
    # Strong signal - can stop early
    experiment.results = preliminary_results
```

**Issue: Knowledge Base growing too large**

```python
# Implement cleanup policy
def cleanup_old_hypotheses(kb: KnowledgeBase, days=30):
    """Remove old refuted/discarded hypotheses."""
    cutoff = datetime.now() - timedelta(days=days)
    
    to_remove = [
        h_id for h_id, h in kb.hypotheses.items()
        if h.status in [HypothesisStatus.REFUTED, HypothesisStatus.DISCARDED]
        and h.timestamp < cutoff
    ]
    
    for h_id in to_remove:
        del kb.hypotheses[h_id]
    
    print(f"Removed {len(to_remove)} old hypotheses")
```

---

## Next Steps

1. **Read the API Documentation**: See [API_SCHEMAS.md](./API_SCHEMAS.md) for detailed schema definitions
2. **Explore Examples**: Check the [examples/](../examples/) directory for complete working examples
3. **Run Tests**: Execute `pytest tests/` to understand expected behavior
4. **Customize**: Build your own integration following the patterns above

---

## Support and Resources

- **GitHub Issues**: Report bugs or request features
- **Examples Directory**: `examples/` contains working demonstrations
- **Test Suite**: `tests/` shows expected behavior
- **Core Documentation**: In-code documentation in `core/` modules

---

*Last updated: 2024*  
*Scientific Method Framework - WADELABS AI Safety Research*
