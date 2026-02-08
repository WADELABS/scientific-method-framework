from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum, auto
from datetime import datetime
import uuid

class HypothesisStatus(Enum):
    PROPOSED = auto()
    TESTING = auto()
    SUPPORTED = auto()
    WELL_SUPPORTED = auto()
    REFUTED = auto()
    DISCARDED = auto()

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

class KnowledgeBase:
    def __init__(self):
        self.hypotheses: Dict[str, Hypothesis] = {}
        self.evidence: Dict[str, Evidence] = {}
        self.theories: Dict[str, Theory] = {}
        self.experiments: Dict[str, Experiment] = {}

    def add_hypothesis(self, hypothesis: Hypothesis):
        self.hypotheses[hypothesis.id] = hypothesis

    def add_theory(self, theory: Theory):
        self.theories[theory.id] = theory

class ScientificAgent:
    def __init__(self, domain: str, knowledge_base: KnowledgeBase):
        self.domain = domain
        self.knowledge_base = knowledge_base
        self.active_hypotheses: List[Hypothesis] = []
        self.active_experiments: List[Experiment] = []
        self.pending_experiments: List[Experiment] = []
        self.recent_evidence: List[Evidence] = []
        
        # Agent parameters
        self.novelty_preference: float = 0.5
        self.risk_tolerance: float = 0.5
        self.rigor_threshold: float = 0.7

    async def _design_experiment(self, hypothesis: Hypothesis) -> Experiment:
        """Design an experiment to test the hypothesis."""
        import logging
        logging.info(f"Designing experiment for hypothesis: {hypothesis.id}")
        return Experiment(
            id=f"exp_{uuid.uuid4()}",
            hypothesis_id=hypothesis.id,
            design={},
            conditions=[],
            controls=[],
            measurements=[],
            sample_size=100,
            randomization_procedure="standard",
            statistical_tests=[]
        )
    
    def _find_hypothesis(self, hypothesis_id: str) -> Optional[Hypothesis]:
        return self.knowledge_base.hypotheses.get(hypothesis_id)
    
    def _hypothesis_similarity(self, h1: Hypothesis, h2: Hypothesis) -> float:
        """Calculate semantic similarity between hypotheses."""
        # Simple Jaccard similarity of words
        words1 = set(h1.statement.lower().split())
        words2 = set(h2.statement.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)

    def _are_contradictory(self, h1: Hypothesis, h2: Hypothesis) -> bool:
        """Check if two hypotheses are contradictory."""
        # Basic negation check
        s1 = h1.statement.lower()
        s2 = h2.statement.lower()
        return (f"not {s1}" in s2) or (f"not {s2}" in s1) or ("no " in s1 and s1.replace("no ", "") in s2)
