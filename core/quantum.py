from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
import networkx as nx
from .scientific_agent import Hypothesis

@dataclass
class CollapsedHypothesis:
    """Classical hypothesis state after quantum collapse."""
    hypothesis: Hypothesis
    observation_basis: str
    revealed_aspect: str
    probability: float
    collapse_time: datetime = field(default_factory=datetime.now)

@dataclass
class QuantumHypothesisState:
    """Quantum superposition of hypothesis states."""
    hypothesis: Hypothesis
    amplitude: complex  # Quantum amplitude
    phase: float
    entanglement_links: List[str]  # Links to other hypotheses
    
    def probability(self) -> float:
        """Born rule probability."""
        return abs(self.amplitude) ** 2
    
    def collapse(self, observation_basis: str) -> CollapsedHypothesis:
        """Collapse to classical state upon observation."""
        # Different observation bases reveal different aspects
        if observation_basis == "confirmation":
            revealed_aspect = "supported" if self.probability() > 0.7 else "ambiguous"
        elif observation_basis == "novelty":
            revealed_aspect = "novel" if self.hypothesis.novelty > 0.7 else "conventional"
        elif observation_basis == "practicality":
            revealed_aspect = "practical" if self.hypothesis.testability > 0.7 else "theoretical"
        else:
            revealed_aspect = "observed"
        
        return CollapsedHypothesis(
            hypothesis=self.hypothesis,
            observation_basis=observation_basis,
            revealed_aspect=revealed_aspect,
            probability=self.probability()
        )

class QuantumScientificReasoner:
    """
    Quantum-inspired scientific reasoning that maintains superposition
    of multiple interpretations simultaneously.
    """
    
    def __init__(self):
        self.hypothesis_superpositions: Dict[str, QuantumHypothesisState] = {}
        self.interference_patterns: Dict[str, List[float]] = {}  # Constructive/destructive interference
        self.entanglement_network: nx.Graph = nx.Graph()
        self.decoherence_history: List[Dict[str, Any]] = []
        
    def add_hypothesis_superposition(self, hypothesis: Hypothesis, 
                                    initial_amplitude: complex = 1+0j):
        """Add hypothesis in quantum superposition state."""
        state = QuantumHypothesisState(
            hypothesis=hypothesis,
            amplitude=initial_amplitude / np.sqrt(2),  # Normalize
            phase=np.random.uniform(0, 2*np.pi),
            entanglement_links=[]
        )
        self.hypothesis_superpositions[hypothesis.id] = state
        
        # Add to entanglement network
        self.entanglement_network.add_node(hypothesis.id, 
                                          confidence=hypothesis.confidence,
                                          novelty=hypothesis.novelty)
    
    def entangle_hypotheses(self, hypothesis_id1: str, hypothesis_id2: str,
                           entanglement_strength: float = 0.5):
        """Create quantum entanglement between hypotheses."""
        if (hypothesis_id1 in self.hypothesis_superpositions and 
            hypothesis_id2 in self.hypothesis_superpositions):
            
            # Create entangled state
            state1 = self.hypothesis_superpositions[hypothesis_id1]
            state2 = self.hypothesis_superpositions[hypothesis_id2]
            
            state1.entanglement_links.append(hypothesis_id2)
            state2.entanglement_links.append(hypothesis_id1)
            
            # Add edge to entanglement network
            self.entanglement_network.add_edge(hypothesis_id1, hypothesis_id2,
                                              strength=entanglement_strength,
                                              type="quantum_entanglement")
            
            # Update amplitudes to reflect entanglement
            self._update_entangled_amplitudes(state1, state2, entanglement_strength)
    
    def _update_entangled_amplitudes(self, state1: QuantumHypothesisState,
                                   state2: QuantumHypothesisState,
                                   strength: float):
        """Update amplitudes for entangled hypotheses."""
        # Simple entanglement model: amplitudes become correlated
        angle = np.arctan2(state2.amplitude.imag, state2.amplitude.real)
        new_amp1 = state1.amplitude * np.exp(1j * angle * strength)
        new_amp2 = state2.amplitude * np.exp(1j * np.pi/2 * strength)
        
        state1.amplitude = new_amp1
        state2.amplitude = new_amp2
    
    def apply_evidence(self, evidence: Any, 
                      decoherence_rate: float = 0.1):
        """Apply evidence as quantum measurement, causing partial decoherence."""
        hypothesis_id = evidence.hypothesis_id
        
        if hypothesis_id not in self.hypothesis_superpositions:
            return
        
        state = self.hypothesis_superpositions[hypothesis_id]
        
        # Evidence strength affects amplitude
        # Assuming evidence.strength is an Enum or similar with .value
        evidence_strength = 0.5 # Default fallback
        if hasattr(evidence.strength, 'value'):
             evidence_strength = evidence.strength.value / 3.0  # Normalize -3 to 1
        elif isinstance(evidence.strength, (int, float)):
             evidence_strength = float(evidence.strength)

        
        if evidence_strength > 0:
            # Confirming evidence: increase amplitude
            factor = 1 + (evidence_strength * 0.5)
            state.amplitude *= factor
        else:
            # Disconfirming evidence: decrease amplitude
            factor = 1 - (abs(evidence_strength) * 0.3)
            state.amplitude *= factor
        
        # Normalize
        self._normalize_superposition()
        
        # Record decoherence event
        self.decoherence_history.append({
            "timestamp": datetime.now(),
            "hypothesis_id": hypothesis_id,
            "evidence_id": evidence.id,
            "pre_amplitude": state.amplitude,
            "evidence_strength": evidence_strength,
            "decoherence_rate": decoherence_rate
        })
        
        # Propagate to entangled hypotheses
        for entangled_id in state.entanglement_links:
            if entangled_id in self.hypothesis_superpositions:
                entangled_state = self.hypothesis_superpositions[entangled_id]
                # Entangled hypotheses are affected, but less strongly
                entangled_state.amplitude *= (1 + evidence_strength * 0.2)
    
    def compute_interference(self, hypothesis_id1: str, hypothesis_id2: str) -> Dict[str, Any]:
        """Compute quantum interference between hypothesis states."""
        if (hypothesis_id1 not in self.hypothesis_superpositions or 
            hypothesis_id2 not in self.hypothesis_superpositions):
            return {}
        
        state1 = self.hypothesis_superpositions[hypothesis_id1]
        state2 = self.hypothesis_superpositions[hypothesis_id2]
        
        # Compute interference pattern
        phase_diff = np.angle(state1.amplitude) - np.angle(state2.amplitude)
        amplitude_sum = abs(state1.amplitude + state2.amplitude)
        amplitude_diff = abs(state1.amplitude - state2.amplitude)
        
        # Constructive vs destructive interference
        constructive = amplitude_sum ** 2
        destructive = amplitude_diff ** 2
        
        interference = {
            "phase_difference": phase_diff,
            "constructive_probability": constructive,
            "destructive_probability": destructive,
            "interference_visibility": (constructive - destructive) / (constructive + destructive) if (constructive + destructive) != 0 else 0,
            "entangled": hypothesis_id2 in state1.entanglement_links
        }
        
        # Store interference pattern
        key = f"{hypothesis_id1}_{hypothesis_id2}"
        if key not in self.interference_patterns:
            self.interference_patterns[key] = []
        self.interference_patterns[key].append(interference["interference_visibility"])
        
        return interference
    
    def generate_quantum_predictions(self, hypothesis_id: str, 
                                   n_predictions: int = 3) -> List[Dict[str, Any]]:
        """Generate quantum-inspired predictions from hypothesis superposition."""
        if hypothesis_id not in self.hypothesis_superpositions:
            return []
        
        state = self.hypothesis_superpositions[hypothesis_id]
        predictions = []
        
        # Generate predictions based on quantum state properties
        for i in range(n_predictions):
            # Amplitude affects prediction confidence
            confidence = min(0.95, state.probability() * 1.2)
            
            # Phase affects prediction type
            phase_angle = np.angle(state.amplitude)
            
            if 0 <= phase_angle < np.pi/2:
                pred_type = "direct_effect"
                novelty = 0.3
            elif np.pi/2 <= phase_angle < np.pi:
                pred_type = "moderating_effect"
                novelty = 0.6
            elif np.pi <= phase_angle < 3*np.pi/2:
                pred_type = "mediating_effect"
                novelty = 0.8
            else:
                pred_type = "emergent_effect"
                novelty = 0.9
            
            prediction = {
                "id": f"quantum_pred_{hypothesis_id}_{i}",
                "hypothesis_id": hypothesis_id,
                "type": pred_type,
                "confidence": confidence,
                "novelty": novelty,
                "amplitude": abs(state.amplitude),
                "phase": phase_angle,
                "generation_method": "quantum_superposition",
                "entanglement_effects": len(state.entanglement_links) > 0
            }
            
            predictions.append(prediction)
        
        return predictions
    
    def _normalize_superposition(self):
        """Normalize all amplitudes to preserve total probability."""
        total_prob = sum(state.probability() for state in self.hypothesis_superpositions.values())
        
        if total_prob > 0:
            normalization = 1.0 / np.sqrt(total_prob)
            for state in self.hypothesis_superpositions.values():
                state.amplitude *= normalization
