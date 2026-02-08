from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Any

class ScientificParadigm(Enum):
    """Philosophical paradigms in science."""
    EMPIRICISM = auto()        # Knowledge from sensory experience
    RATIONALISM = auto()       # Knowledge from reason
    POSITIVISM = auto()        # Only verifiable statements meaningful
    FALSIFICATIONISM = auto()  # Popper: hypotheses must be falsifiable
    KUHNIAN = auto()           # Paradigm shifts, normal vs revolutionary science
    LAKATOSIAN = auto()        # Research programmes with hard core
    FEYERABEND = auto()        # Epistemological anarchism
    BAYESIAN = auto()          # Degrees of belief, probabilistic
    HERMENEUTIC = auto()       # Interpretation, understanding over explanation
    COMPLEXITY = auto()        # Complex systems, emergence

class EpistemicVirtue(Enum):
    """Intellectual virtues in scientific practice."""
    EMPIRICAL_ADEQUACY = auto()  # Fits the data
    EXPLANATORY_POWER = auto()   # Explains phenomena
    PREDICTIVE_ACCURACY = auto() # Makes correct predictions
    INTERNAL_CONSISTENCY = auto() # No contradictions
    EXTERNAL_CONSISTENCY = auto() # Consistent with other knowledge
    UNIFICATORY_POWER = auto()   # Unifies disparate phenomena
    FERTILITY = auto()           # Generates new research
    SIMPLICITY = auto()          # Parsimony, Occam's razor
    TESTABILITY = auto()         # Can be empirically tested
    NOVELTY = auto()             # New, non-obvious
    ROBUSTNESS = auto()          # Stable under variations
    TRANSPARENCY = auto()        # Clear, explicit assumptions
    COMPREHENSIBILITY = auto()   # Understandable to humans

@dataclass
class ParadigmLens:
    """How different paradigms interpret the same phenomena."""
    paradigm: ScientificParadigm
    interpretive_priorities: List[EpistemicVirtue]
    methodological_constraints: List[str]
    truth_criteria: List[str]
    blindnesses: List[str]  # What the paradigm cannot see
    
    def interpret_evidence(self, evidence: Any) -> Dict[str, Any]:
        """Interpret evidence through paradigm-specific lens."""
        interpretations = {}
        
        # Note: evidence expected to be Evidence object but imported as Any to avoid circular import
        # In implementation we assume it has strength, quality_score attributes
        
        if self.paradigm == ScientificParadigm.FALSIFICATIONISM:
            interpretations["focus"] = "falsifiability"
            # interpretations["value"] = evidence.strength.value < 0  
            interpretations["method"] = "attempted refutation"
            
        elif self.paradigm == ScientificParadigm.BAYESIAN:
            interpretations["focus"] = "belief updating"
            # interpretations["value"] = evidence.quality_score * evidence.strength.value
            interpretations["method"] = "Bayesian inference"
            
        elif self.paradigm == ScientificParadigm.HERMENEUTIC:
            interpretations["focus"] = "understanding"
            # interpretations["value"] = evidence.replicability * evidence.quality_score
            interpretations["method"] = "interpretive circle"
            
        elif self.paradigm == ScientificParadigm.COMPLEXITY:
            interpretations["focus"] = "emergent patterns"
            # interpretations["value"] = evidence.effect_size if evidence.effect_size else 0
            interpretations["method"] = "pattern recognition"
            
        return interpretations
