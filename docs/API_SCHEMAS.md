# API Schemas and Data Contracts

This document provides comprehensive JSON Schema definitions for all core data structures in the Scientific Method Framework (SMF). These schemas define the API contracts for integrating with external systems and ensure data validation and consistency.

## Table of Contents

1. [Overview](#overview)
2. [Core Data Structures](#core-data-structures)
   - [Evidence](#evidence-schema)
   - [Hypothesis](#hypothesis-schema)
   - [Experiment](#experiment-schema)
   - [Theory](#theory-schema)
3. [Supporting Types](#supporting-types)
4. [Validation Rules](#validation-rules)
5. [Integration Schemas](#integration-schemas)
6. [Complete Examples](#complete-examples)

---

## Overview

The SMF uses strongly-typed data structures based on Python dataclasses. This document provides JSON Schema representations for external integrations, REST APIs, and data validation.

### Schema Conventions

- **Required fields**: Marked with `"required": true` in the schema
- **Timestamps**: ISO 8601 format (`YYYY-MM-DDTHH:mm:ss.sssZ`)
- **IDs**: UUID v4 format or custom string identifiers with prefix (e.g., `h_`, `exp_`, `ev_`)
- **Scores/Metrics**: Float values typically in range `[0.0, 1.0]`

---

## Core Data Structures

### Evidence Schema

Evidence represents observational data that supports or refutes a hypothesis.

#### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Evidence",
  "type": "object",
  "required": ["id", "hypothesis_id", "content", "timestamp", "strength", "source"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the evidence",
      "pattern": "^ev_[a-zA-Z0-9_-]+$",
      "examples": ["ev_12345", "ev_experiment_001"]
    },
    "hypothesis_id": {
      "type": "string",
      "description": "Reference to the hypothesis this evidence relates to",
      "pattern": "^h_[a-zA-Z0-9_-]+$"
    },
    "content": {
      "description": "The actual evidence data (flexible type)",
      "oneOf": [
        {"type": "object"},
        {"type": "array"},
        {"type": "string"},
        {"type": "number"},
        {"type": "boolean"}
      ]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the evidence was collected (ISO 8601)"
    },
    "strength": {
      "description": "Strength of evidence (can be enum or numeric value)",
      "oneOf": [
        {
          "type": "string",
          "enum": ["weak", "moderate", "strong", "very_strong"]
        },
        {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        }
      ]
    },
    "source": {
      "type": "string",
      "description": "Source of the evidence (e.g., experiment ID, observation, literature)"
    },
    "quality_score": {
      "type": "number",
      "description": "Quality/reliability of the evidence",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.5
    },
    "replicability": {
      "type": "number",
      "description": "How replicable this evidence is",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.5
    },
    "effect_size": {
      "type": ["number", "null"],
      "description": "Magnitude of the observed effect",
      "minimum": 0.0
    }
  },
  "additionalProperties": false
}
```

#### Python Type Definition

```python
@dataclass
class Evidence:
    id: str
    hypothesis_id: str
    content: Any
    timestamp: datetime
    strength: Any  # Can be an Enum or value
    source: str
    quality_score: float = 0.5
    replicability: float = 0.5
    effect_size: Optional[float] = None
```

---

### Hypothesis Schema

A hypothesis is a testable prediction about relationships between variables.

#### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Hypothesis",
  "type": "object",
  "required": [
    "id", "statement", "variables", "relationships", "domain",
    "timestamp", "confidence", "complexity", "novelty", "testability"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the hypothesis",
      "pattern": "^h_[a-zA-Z0-9_-]+$",
      "examples": ["h_timeout_fix", "h_performance_001"]
    },
    "statement": {
      "type": "string",
      "description": "Clear, testable statement of the hypothesis",
      "minLength": 10,
      "maxLength": 1000
    },
    "variables": {
      "type": "object",
      "description": "Variables involved in the hypothesis",
      "additionalProperties": {
        "type": "string"
      },
      "minProperties": 1
    },
    "relationships": {
      "type": "array",
      "description": "Relationships between variables",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "domain": {
      "type": "string",
      "description": "Scientific or problem domain",
      "examples": ["system_performance", "machine_learning", "biology"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the hypothesis was created"
    },
    "confidence": {
      "type": "number",
      "description": "Initial confidence in the hypothesis",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "complexity": {
      "type": "number",
      "description": "Complexity of the hypothesis",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "novelty": {
      "type": "number",
      "description": "How novel/original the hypothesis is",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "testability": {
      "type": "number",
      "description": "How testable the hypothesis is",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "status": {
      "type": "string",
      "description": "Current status of the hypothesis",
      "enum": [
        "PROPOSED",
        "TESTING",
        "SUPPORTED",
        "WELL_SUPPORTED",
        "REFUTED",
        "DISCARDED"
      ],
      "default": "PROPOSED"
    },
    "supporting_evidence": {
      "type": "array",
      "description": "Evidence that supports this hypothesis",
      "items": {
        "$ref": "#/definitions/Evidence"
      },
      "default": []
    },
    "disconfirming_evidence": {
      "type": "array",
      "description": "Evidence that contradicts this hypothesis",
      "items": {
        "$ref": "#/definitions/Evidence"
      },
      "default": []
    }
  },
  "additionalProperties": false
}
```

#### Python Type Definition

```python
class HypothesisStatus(Enum):
    PROPOSED = auto()
    TESTING = auto()
    SUPPORTED = auto()
    WELL_SUPPORTED = auto()
    REFUTED = auto()
    DISCARDED = auto()

@dataclass
class Hypothesis:
    id: str
    statement: str
    variables: Dict[str, str]
    relationships: List[str]
    domain: str
    timestamp: datetime
    confidence: float
    complexity: float
    novelty: float
    testability: float
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    supporting_evidence: List[Evidence] = field(default_factory=list)
    disconfirming_evidence: List[Evidence] = field(default_factory=list)
```

---

### Experiment Schema

An experiment is a controlled test designed to validate or refute a hypothesis.

#### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Experiment",
  "type": "object",
  "required": [
    "id", "hypothesis_id", "design", "conditions", "controls",
    "measurements", "sample_size", "randomization_procedure", "statistical_tests"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the experiment",
      "pattern": "^exp_[a-zA-Z0-9_-]+$",
      "examples": ["exp_timeout_test", "exp_12345"]
    },
    "hypothesis_id": {
      "type": "string",
      "description": "Reference to the hypothesis being tested",
      "pattern": "^h_[a-zA-Z0-9_-]+$"
    },
    "design": {
      "type": "object",
      "description": "Experimental design details",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["simulation", "ab_test", "randomized_control", "quasi_experimental", "observational"]
        },
        "parameters": {
          "type": "object",
          "additionalProperties": true
        }
      },
      "required": ["type"]
    },
    "conditions": {
      "type": "array",
      "description": "Experimental conditions to test",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "controls": {
      "type": "array",
      "description": "Control variables",
      "items": {
        "type": "string"
      }
    },
    "measurements": {
      "type": "array",
      "description": "Metrics to measure",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "sample_size": {
      "type": "integer",
      "description": "Number of samples/trials",
      "minimum": 1
    },
    "randomization_procedure": {
      "type": "string",
      "description": "How randomization is performed",
      "examples": ["random_assignment", "stratified", "block_randomization"]
    },
    "statistical_tests": {
      "type": "array",
      "description": "Statistical tests to apply",
      "items": {
        "type": "string"
      },
      "examples": [["t_test", "chi_square", "anova", "mann_whitney"]]
    },
    "results": {
      "description": "Experiment results (flexible schema)",
      "oneOf": [
        {"type": "object"},
        {"type": "null"}
      ]
    },
    "analysis": {
      "type": ["object", "null"],
      "description": "Statistical analysis of results",
      "properties": {
        "conclusion": {
          "type": "string",
          "enum": ["supported", "refuted", "inconclusive"]
        },
        "confidence": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "statistical_significance": {
          "type": "boolean"
        },
        "p_value": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        }
      }
    }
  },
  "additionalProperties": false
}
```

#### Python Type Definition

```python
@dataclass
class Experiment:
    id: str
    hypothesis_id: str
    design: Dict[str, Any]
    conditions: List[str]
    controls: List[str]
    measurements: List[str]
    sample_size: int
    randomization_procedure: str
    statistical_tests: List[str]
    results: Optional[Any] = None
    analysis: Optional[Dict[str, Any]] = None
```

---

### Theory Schema

A theory is a well-supported explanatory framework backed by multiple hypotheses and evidence.

#### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Theory",
  "type": "object",
  "required": [
    "id", "name", "core_principles", "explanatory_scope",
    "predictive_power", "parsimony", "coherence", "empirical_support",
    "hypotheses", "evidence"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the theory",
      "pattern": "^theory_[a-zA-Z0-9_-]+$"
    },
    "name": {
      "type": "string",
      "description": "Human-readable name of the theory",
      "minLength": 3,
      "maxLength": 200
    },
    "core_principles": {
      "type": "array",
      "description": "Fundamental principles of the theory",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "explanatory_scope": {
      "type": "array",
      "description": "Domains/phenomena explained by this theory",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "predictive_power": {
      "type": "number",
      "description": "How well the theory predicts outcomes",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "parsimony": {
      "type": "number",
      "description": "Simplicity of the theory (Occam's razor)",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "coherence": {
      "type": "number",
      "description": "Internal logical consistency",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "empirical_support": {
      "type": "number",
      "description": "Strength of empirical evidence",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "hypotheses": {
      "type": "array",
      "description": "Hypotheses that constitute this theory",
      "items": {
        "$ref": "#/definitions/Hypothesis"
      }
    },
    "evidence": {
      "type": "array",
      "description": "Evidence supporting this theory",
      "items": {
        "$ref": "#/definitions/Evidence"
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional metadata",
      "additionalProperties": true,
      "default": {}
    }
  },
  "additionalProperties": false
}
```

#### Python Type Definition

```python
@dataclass
class Theory:
    id: str
    name: str
    core_principles: List[str]
    explanatory_scope: List[str]
    predictive_power: float
    parsimony: float
    coherence: float
    empirical_support: float
    hypotheses: List[Hypothesis]
    evidence: List[Evidence]
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## Supporting Types

### HypothesisStatus Enum

```json
{
  "type": "string",
  "enum": [
    "PROPOSED",
    "TESTING",
    "SUPPORTED",
    "WELL_SUPPORTED",
    "REFUTED",
    "DISCARDED"
  ]
}
```

### EvidenceStrength

```json
{
  "oneOf": [
    {
      "type": "string",
      "enum": ["weak", "moderate", "strong", "very_strong"]
    },
    {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    }
  ]
}
```

---

## Validation Rules

### Field Constraints

1. **IDs**:
   - Hypothesis IDs must start with `h_`
   - Experiment IDs must start with `exp_`
   - Evidence IDs must start with `ev_`
   - Theory IDs must start with `theory_`

2. **Timestamps**:
   - Must be valid ISO 8601 format
   - Timezone-aware preferred
   - Example: `2024-01-15T14:30:00.000Z`

3. **Scores and Metrics**:
   - All scores must be in range `[0.0, 1.0]`
   - Includes: confidence, complexity, novelty, testability, quality_score, replicability

4. **Minimum Requirements**:
   - Hypothesis statement: 10-1000 characters
   - At least 1 variable in hypothesis
   - At least 1 relationship in hypothesis
   - At least 1 condition in experiment
   - At least 1 measurement in experiment
   - Sample size must be positive integer

### Business Rules

1. **Hypothesis Lifecycle**:
   ```
   PROPOSED → TESTING → (SUPPORTED | REFUTED | WELL_SUPPORTED)
                     ↓
                  DISCARDED
   ```

2. **Evidence Quality**:
   - `quality_score * replicability >= 0.25` for high-quality evidence
   - Effect size should be positive when present

3. **Theory Validity**:
   - Must have at least one hypothesis
   - Empirical support should correlate with hypothesis evidence
   - Predictive power ≥ 0.7 for strong theories

---

## Integration Schemas

### REST API Request/Response

#### Create Hypothesis Request

```json
{
  "statement": "Increasing cache size improves query performance",
  "variables": {
    "cache_size": "1GB",
    "query_latency": "reduced"
  },
  "relationships": ["cache_size_affects_latency"],
  "domain": "database_optimization",
  "confidence": 0.75,
  "complexity": 0.4,
  "novelty": 0.6,
  "testability": 0.9
}
```

#### Create Hypothesis Response

```json
{
  "id": "h_cache_optimization_001",
  "statement": "Increasing cache size improves query performance",
  "variables": {
    "cache_size": "1GB",
    "query_latency": "reduced"
  },
  "relationships": ["cache_size_affects_latency"],
  "domain": "database_optimization",
  "timestamp": "2024-01-15T14:30:00.000Z",
  "confidence": 0.75,
  "complexity": 0.4,
  "novelty": 0.6,
  "testability": 0.9,
  "status": "PROPOSED",
  "supporting_evidence": [],
  "disconfirming_evidence": []
}
```

#### Submit Evidence Request

```json
{
  "hypothesis_id": "h_cache_optimization_001",
  "content": {
    "avg_latency_before": 250,
    "avg_latency_after": 120,
    "sample_size": 1000,
    "p_value": 0.001
  },
  "strength": "strong",
  "source": "exp_cache_test_001",
  "quality_score": 0.9,
  "replicability": 0.85,
  "effect_size": 0.52
}
```

### Batch Operations Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BatchHypothesisCreation",
  "type": "object",
  "properties": {
    "hypotheses": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Hypothesis"
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "batch_id": {"type": "string"},
        "created_by": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"}
      }
    }
  }
}
```

---

## Complete Examples

### Example 1: Complete Hypothesis with Evidence

```json
{
  "id": "h_timeout_fix",
  "statement": "Increasing timeout to 300s will reduce transaction failures",
  "variables": {
    "timeout": "300s",
    "failure_rate": "low"
  },
  "relationships": ["timeout_affects_success"],
  "domain": "system_performance",
  "timestamp": "2024-01-15T10:00:00.000Z",
  "confidence": 0.7,
  "complexity": 0.3,
  "novelty": 0.5,
  "testability": 0.9,
  "status": "SUPPORTED",
  "supporting_evidence": [
    {
      "id": "ev_exp_timeout_001",
      "hypothesis_id": "h_timeout_fix",
      "content": {
        "success_rate": 0.92,
        "latency_ms": 145.3,
        "error_count": 2,
        "sample_size": 100,
        "statistical_significance": true
      },
      "timestamp": "2024-01-15T11:30:00.000Z",
      "strength": "strong",
      "source": "exp_timeout_001",
      "quality_score": 0.9,
      "replicability": 0.85,
      "effect_size": 0.42
    }
  ],
  "disconfirming_evidence": []
}
```

### Example 2: Complete Experiment with Results

```json
{
  "id": "exp_timeout_001",
  "hypothesis_id": "h_timeout_fix",
  "design": {
    "type": "ab_test",
    "parameters": {
      "timeout_values": [60, 120, 300],
      "duration": "1h",
      "traffic_split": "33/33/34"
    }
  },
  "conditions": ["baseline_60s", "moderate_120s", "extended_300s"],
  "controls": ["server_load", "network_conditions", "time_of_day"],
  "measurements": ["success_rate", "latency", "error_count"],
  "sample_size": 1000,
  "randomization_procedure": "stratified_random_assignment",
  "statistical_tests": ["anova", "tukey_hsd", "chi_square"],
  "results": {
    "baseline_60s": {
      "success_rate": 0.50,
      "avg_latency_ms": 280,
      "errors": 500
    },
    "moderate_120s": {
      "success_rate": 0.75,
      "avg_latency_ms": 210,
      "errors": 250
    },
    "extended_300s": {
      "success_rate": 0.92,
      "avg_latency_ms": 145,
      "errors": 80
    }
  },
  "analysis": {
    "conclusion": "supported",
    "confidence": 0.92,
    "statistical_significance": true,
    "p_value": 0.001,
    "effect_size": 0.42,
    "notes": "300s timeout shows significant improvement over baseline"
  }
}
```

### Example 3: Complete Theory

```json
{
  "id": "theory_timeout_performance",
  "name": "Timeout Configuration Theory",
  "core_principles": [
    "Adequate timeout values prevent premature termination",
    "Transaction success rate correlates with timeout duration",
    "Optimal timeout balances success rate and resource utilization"
  ],
  "explanatory_scope": [
    "system_performance",
    "transaction_processing",
    "network_reliability"
  ],
  "predictive_power": 0.85,
  "parsimony": 0.8,
  "coherence": 0.9,
  "empirical_support": 0.88,
  "hypotheses": [
    {
      "id": "h_timeout_fix",
      "statement": "Increasing timeout to 300s will reduce transaction failures",
      "status": "SUPPORTED"
    }
  ],
  "evidence": [
    {
      "id": "ev_exp_timeout_001",
      "hypothesis_id": "h_timeout_fix",
      "strength": "strong",
      "quality_score": 0.9
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-01-15T12:00:00.000Z",
    "authors": ["SMF Agent"],
    "domain_experts": ["system_architecture"]
  }
}
```

### Example 4: Knowledge Base Export

```json
{
  "knowledge_base": {
    "id": "kb_production_001",
    "created": "2024-01-15T09:00:00.000Z",
    "updated": "2024-01-15T12:00:00.000Z",
    "hypotheses": {
      "h_timeout_fix": { /* ... */ },
      "h_cache_optimization": { /* ... */ }
    },
    "experiments": {
      "exp_timeout_001": { /* ... */ },
      "exp_cache_001": { /* ... */ }
    },
    "evidence": {
      "ev_exp_timeout_001": { /* ... */ },
      "ev_exp_cache_001": { /* ... */ }
    },
    "theories": {
      "theory_timeout_performance": { /* ... */ }
    },
    "statistics": {
      "total_hypotheses": 2,
      "total_experiments": 2,
      "total_evidence": 2,
      "total_theories": 1,
      "hypothesis_status_counts": {
        "PROPOSED": 0,
        "TESTING": 1,
        "SUPPORTED": 1,
        "WELL_SUPPORTED": 0,
        "REFUTED": 0,
        "DISCARDED": 0
      }
    }
  }
}
```

---

## Validation Examples

### Using Python with dataclasses-json

```python
from dataclasses_json import dataclass_json
from core.scientific_agent import Hypothesis, Evidence, Experiment, Theory
import json

# Serialize to JSON
hypothesis = Hypothesis(
    id="h_test",
    statement="Test hypothesis",
    variables={"x": "value"},
    relationships=["x_affects_y"],
    domain="test",
    timestamp=datetime.now(),
    confidence=0.8,
    complexity=0.5,
    novelty=0.6,
    testability=0.9
)

# Convert to JSON
json_str = json.dumps(hypothesis, default=str)

# Validate against schema (using jsonschema library)
from jsonschema import validate, ValidationError

hypothesis_schema = { /* schema from above */ }

try:
    validate(instance=json.loads(json_str), schema=hypothesis_schema)
    print("✓ Valid hypothesis")
except ValidationError as e:
    print(f"✗ Invalid: {e.message}")
```

### Using JavaScript/TypeScript

```typescript
import Ajv from 'ajv';

const ajv = new Ajv();
const validate = ajv.compile(hypothesisSchema);

const hypothesis = {
  id: "h_test",
  statement: "Test hypothesis",
  // ... other fields
};

if (validate(hypothesis)) {
  console.log("✓ Valid hypothesis");
} else {
  console.log("✗ Invalid:", validate.errors);
}
```

---

## API Contract Versioning

The SMF uses semantic versioning for API contracts:

- **Major version**: Breaking changes to schema structure
- **Minor version**: Backward-compatible additions
- **Patch version**: Documentation or clarification updates

Current version: **1.0.0**

Include version in API requests:
```http
POST /api/v1/hypotheses
Content-Type: application/json
X-API-Version: 1.0.0
```

---

## Further Reading

- [Integration Guide](./INTEGRATION.md) - How to use these schemas in your projects
- [Scientific Agent Documentation](../core/scientific_agent.py) - Source code reference
- [Examples](../examples/) - Complete working examples

---

*Last updated: 2024*  
*Scientific Method Framework - WADELABS AI Safety Research*
