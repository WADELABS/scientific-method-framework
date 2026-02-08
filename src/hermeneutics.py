from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from .foundations import ScientificParadigm

@dataclass
class InterpretiveHorizon:
    """Gadamerian horizon for scientific understanding."""
    pre_understandings: List[str]  # Prejudices (Vorurteile)
    historical_consciousness: Dict[str, Any]  # Wirkungsgeschichte
    tradition: ScientificParadigm
    fusion_history: List[Dict[str, Any]]  # Horizon fusions
    effective_history: Dict[str, Any]  # How history affects current understanding
    
    def fuse_with(self, other: 'InterpretiveHorizon') -> 'InterpretiveHorizon':
        """Fuse horizons (Horizontverschmelzung)."""
        new_pre_understandings = list(set(self.pre_understandings + other.pre_understandings))
        
        # Historical consciousness fusion
        new_historical = {
            "merged_from": [self.historical_consciousness.get("origin", "unknown"),
                           other.historical_consciousness.get("origin", "unknown")],
            "fusion_time": datetime.now(),
            "integrated_traditions": [self.tradition, other.tradition]
        }
        
        # Record fusion
        fusion_record = {
            "horizon1": self.tradition.name,
            "horizon2": other.tradition.name,
            "time": datetime.now(),
            "pre_understanding_synthesis": f"{len(new_pre_understandings)} integrated prejudgements"
        }
        
        new_fusion_history = self.fusion_history + other.fusion_history + [fusion_record]
        
        # Create new effective history
        new_effective = {
            "created_from_fusion": True,
            "parent_horizons": [id(self), id(other)],
            "fusion_count": len(new_fusion_history),
            "tradition_complexity": len(set([self.tradition, other.tradition]))
        }
        
        # Choose dominant tradition (for now, weighted by historical influence)
        dominant_tradition = self.tradition if len(self.fusion_history) > len(other.fusion_history) else other.tradition
        
        return InterpretiveHorizon(
            pre_understandings=new_pre_understandings,
            historical_consciousness=new_historical,
            tradition=dominant_tradition,
            fusion_history=new_fusion_history,
            effective_history=new_effective
        )
    
    def interpret_data(self, data: pd.DataFrame, 
                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret data through this horizon."""
        interpretation = {
            "horizon": self.tradition.name,
            "pre_understandings_applied": self.pre_understandings[:3],
            "historical_effects": self.effective_history,
            "interpretive_moves": []
        }
        
        # Different traditions interpret data differently
        if self.tradition == ScientificParadigm.FALSIFICATIONISM:
            interpretation["focus"] = "refutation_attempts"
            interpretation["method"] = "search_for_counterexamples"
            interpretation["value_criteria"] = ["falsifiability", "riskiness"]
            
        elif self.tradition == ScientificParadigm.HERMENEUTIC:
            interpretation["focus"] = "understanding_meaning"
            interpretation["method"] = "hermeneutic_circle"
            interpretation["value_criteria"] = ["coherence", "meaningfulness", "context_sensitivity"]
            
        elif self.tradition == ScientificParadigm.BAYESIAN:
            interpretation["focus"] = "belief_updating"
            interpretation["method"] = "probabilistic_inference"
            interpretation["value_criteria"] = ["likelihood_ratio", "prior_plausibility"]
            
        elif self.tradition == ScientificParadigm.COMPLEXITY:
            interpretation["focus"] = "emergent_patterns"
            interpretation["method"] = "pattern_recognition"
            interpretation["value_criteria"] = ["nonlinearity", "scale_invariance", "emergence"]
        # Default or fallback
        else:
             interpretation["focus"] = "general_analysis"
             interpretation["method"] = "standard_review"
             interpretation["value_criteria"] = ["accuracy"]
        
        return interpretation

class HermeneuticScientificInterpreter:
    """
    Applies hermeneutic principles to scientific interpretation.
    Focuses on understanding rather than just explanation.
    """
    
    def __init__(self, initial_horizon: InterpretiveHorizon):
        self.current_horizon = initial_horizon
        self.hermeneutic_circles: List[Dict[str, Any]] = []
        self.aporia_log: List[Dict[str, Any]] = []  # Record of interpretive difficulties
        self.fusion_events: List[Dict[str, Any]] = []
        
    async def conduct_hermeneutic_circle(self, 
                                        hypothesis: Any, # Typed as Any to avoid circular import, expects Hypothesis
                                        data: pd.DataFrame,
                                        existing_interpretations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Conduct hermeneutic circle: part-whole understanding.
        Move between hypothesis (whole) and data (parts).
        """
        circle_start = datetime.now()
        
        # 1. Pre-understanding: What we already think
        pre_understanding = {
            "hypothesis": hypothesis.statement,
            "existing_confidence": hypothesis.confidence,
            "horizon_biases": self.current_horizon.pre_understandings
        }
        
        # 2. First encounter with data
        initial_interpretation = self.current_horizon.interpret_data(data, {})
        
        # 3. Check for contradictions with pre-understanding
        contradictions = self._find_contradictions(pre_understanding, initial_interpretation)
        
        # 4. Adjust understanding based on contradictions
        adjusted_understanding = await self._adjust_understanding(
            pre_understanding, initial_interpretation, contradictions)
        
        # 5. Return to hypothesis with new understanding
        # Note: In a real implementation this would invoke logic to modify the hypothesis object
        # For now we simulate the revision check
        revised_hypothesis_statement = self._adjust_statement(hypothesis.statement, adjusted_understanding["adjusted_beliefs"])
        
        # 6. Second encounter with data (with revised understanding)
        secondary_interpretation = self.current_horizon.interpret_data(data, adjusted_understanding)
        
        # 7. Check for coherence
        coherence_score = self._compute_coherence(adjusted_understanding, secondary_interpretation)
        
        # 8. Record hermeneutic circle
        circle_record = {
            "start_time": circle_start,
            "end_time": datetime.now(),
            "hypothesis_id": hypothesis.id,
            "pre_understanding": pre_understanding,
            "initial_interpretation": initial_interpretation,
            "contradictions_found": contradictions,
            "adjusted_understanding": adjusted_understanding,
            "revised_hypothesis": revised_hypothesis_statement if revised_hypothesis_statement != hypothesis.statement else "unchanged",
            "secondary_interpretation": secondary_interpretation,
            "coherence_score": coherence_score,
            "circle_complete": coherence_score > 0.7
        }
        
        self.hermeneutic_circles.append(circle_record)
        
        return circle_record
    
    async def engage_with_other_horizon(self, other_interpreter: 'HermeneuticScientificInterpreter',
                                      topic: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Engage in dialogue with another interpretive horizon."""
        # Each interpreter shares their understanding
        my_interpretation = self.current_horizon.interpret_data(data, {})
        their_interpretation = other_interpreter.current_horizon.interpret_data(data, {})
        
        # Identify differences
        differences = self._compare_interpretations(my_interpretation, their_interpretation)
        
        # Attempt horizon fusion
        if self._are_fusible(self.current_horizon, other_interpreter.current_horizon):
            fused_horizon = self.current_horizon.fuse_with(other_interpreter.current_horizon)
            
            fusion_event = {
                "time": datetime.now(),
                "horizon1": self.current_horizon.tradition.name,
                "horizon2": other_interpreter.current_horizon.tradition.name,
                "fused_horizon": fused_horizon.tradition.name,
                "differences_resolved": len(differences.get("major_differences", [])),
                "fusion_success": True
            }
            
            self.fusion_events.append(fusion_event)
            self.current_horizon = fused_horizon
            
            # Create new interpretation with fused horizon
            fused_interpretation = fused_horizon.interpret_data(data, {})
            
            return {
                "dialogue_outcome": "horizon_fusion",
                "fusion_event": fusion_event,
                "fused_interpretation": fused_interpretation
            }
        
        else:
            # Record aporia (unresolvable difference)
            aporia = {
                "time": datetime.now(),
                "topic": topic,
                "horizon1": self.current_horizon.tradition.name,
                "horizon2": other_interpreter.current_horizon.tradition.name,
                "irreconcilable_differences": differences.get("major_differences", []),
                "resolution": "aporia_recorded"
            }
            
            self.aporia_log.append(aporia)
            
            return {
                "dialogue_outcome": "aporia",
                "aporia": aporia,
                "suggestion": "seek third horizon or methodological innovation"
            }
    
    def _find_contradictions(self, pre_understanding: Dict[str, Any],
                            interpretation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find contradictions between pre-understanding and interpretation."""
        contradictions = []
        
        # Check if interpretation challenges pre-understanding assumptions
        if "focus" in interpretation and "horizon_biases" in pre_understanding:
            horizon_focus = interpretation["focus"]
            biases = pre_understanding["horizon_biases"]
            
            for bias in biases:
                if "only" in bias or "always" in bias:
                    # Absolute statements often contradicted by data
                    if horizon_focus == "counterexamples":
                        contradictions.append({
                            "type": "absolute_statement_challenged",
                            "bias": bias,
                            "challenge": f"Data suggests exceptions to '{bias}'"
                        })
        
        return contradictions
    
    async def _adjust_understanding(self, pre_understanding: Dict[str, Any],
                                  interpretation: Dict[str, Any],
                                  contradictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Adjust understanding based on contradictions."""
        adjusted = {
            "original_pre_understanding": pre_understanding,
            "initial_interpretation": interpretation,
            "contradictions_addressed": [],
            "adjusted_beliefs": []
        }
        
        for contradiction in contradictions:
            if contradiction["type"] == "absolute_statement_challenged":
                # Qualify the absolute statement
                bias = contradiction["bias"]
                qualified_bias = bias.replace("always", "often").replace("only", "primarily")
                
                adjusted["contradictions_addressed"].append(contradiction)
                adjusted["adjusted_beliefs"].append({
                    "from": bias,
                    "to": qualified_bias,
                    "reason": "data_shows_exceptions"
                })
        
        return adjusted
    
    def _adjust_statement(self, statement: str, 
                         adjustments: List[Dict[str, Any]]) -> str:
        """Adjust hypothesis statement based on belief adjustments."""
        revised = statement
        
        for adjustment in adjustments:
            old_belief = adjustment["from"]
            new_belief = adjustment["to"]
            
            if old_belief in revised:
                revised = revised.replace(old_belief, new_belief)
        
        return revised
    
    def _compute_coherence(self, understanding1: Dict[str, Any],
                          understanding2: Dict[str, Any]) -> float:
        """Compute coherence between two understandings."""
        # Check consistency of foci
        focus1 = understanding1.get("focus", "")
        focus2 = understanding2.get("focus", "")
        
        if focus1 == focus2:
            focus_coherence = 1.0
        elif focus1 in focus2 or focus2 in focus1:
            focus_coherence = 0.7
        else:
            focus_coherence = 0.3
        
        # Check consistency of methods
        method1 = understanding1.get("method", "")
        method2 = understanding2.get("method", "")
        
        if method1 == method2:
            method_coherence = 1.0
        else:
            method_coherence = 0.5
        
        # Check for contradictions in value criteria
        values1 = set(understanding1.get("value_criteria", []))
        values2 = set(understanding2.get("value_criteria", []))
        
        if values1 == values2:
            value_coherence = 1.0
        elif not values1.isdisjoint(values2):
            value_coherence = len(values1.intersection(values2)) / len(values1.union(values2))
        else:
            value_coherence = 0.0
        
        return (focus_coherence + method_coherence + value_coherence) / 3
    
    def _compare_interpretations(self, interpretation1: Dict[str, Any],
                                interpretation2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two interpretations."""
        differences = {
            "focus_difference": interpretation1.get("focus") != interpretation2.get("focus"),
            "method_difference": interpretation1.get("method") != interpretation2.get("method"),
            "value_differences": [],
            "major_differences": []
        }
        
        # Compare value criteria
        values1 = set(interpretation1.get("value_criteria", []))
        values2 = set(interpretation2.get("value_criteria", []))
        
        unique_to_1 = values1 - values2
        unique_to_2 = values2 - values1
        
        differences["value_differences"] = {
            "unique_to_1": list(unique_to_1),
            "unique_to_2": list(unique_to_2),
            "common": list(values1.intersection(values2))
        }
        
        # Identify major differences
        if differences["focus_difference"]:
            differences["major_differences"].append(
                f"Different foci: {interpretation1.get('focus')} vs {interpretation2.get('focus')}"
            )
        
        if unique_to_1 or unique_to_2:
            differences["major_differences"].append(
                f"Different value criteria: {unique_to_1} vs {unique_to_2}"
            )
        
        return differences
    
    def _are_fusible(self, horizon1: InterpretiveHorizon,
                    horizon2: InterpretiveHorizon) -> bool:
        """Determine if two horizons are fusible."""
        # Some paradigms are more compatible than others
        compatibility_matrix = {
            ScientificParadigm.BAYESIAN: {ScientificParadigm.EMPIRICISM, ScientificParadigm.FALSIFICATIONISM},
            ScientificParadigm.HERMENEUTIC: {ScientificParadigm.COMPLEXITY, ScientificParadigm.KUHNIAN},
            ScientificParadigm.COMPLEXITY: {ScientificParadigm.HERMENEUTIC, ScientificParadigm.FEYERABEND},
            ScientificParadigm.FALSIFICATIONISM: {ScientificParadigm.BAYESIAN, ScientificParadigm.POSITIVISM}
        }
        
        compatible_with_1 = compatibility_matrix.get(horizon1.tradition, set())
        compatible_with_2 = compatibility_matrix.get(horizon2.tradition, set())
        
        return (horizon2.tradition in compatible_with_1 or 
                horizon1.tradition in compatible_with_2)
