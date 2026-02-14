import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Any, Dict, List, Optional
import matplotlib.cm as cm
from matplotlib.figure import Figure

from .scientific_agent import KnowledgeBase, Hypothesis, HypothesisStatus
from .agent import DeepScientificAgent
from .foundations import ScientificParadigm

class EnhancedScientificVisualizer:
    """
    Visualization tools for the Deep Scientific Agent.
    Visualizes:
    1. Knowledge Graph (Theories, Hypotheses, Evidence)
    2. Quantum States (Superposition, Entanglement)
    3. Hermeneutic Horizons (Fusion history)
    """
    
    def __init__(self, agent: DeepScientificAgent):
        self.agent = agent
    
    def visualize_knowledge_graph(self, save_path: Optional[str] = None):
        """Visualize the scientific knowledge graph."""
        G = nx.DiGraph()
        
        # Add nodes
        for h_id, h in self.agent.knowledge_base.hypotheses.items():
            G.add_node(h_id, type='hypothesis', status=h.status.name, 
                      confidence=h.confidence, label=h.statement[:30]+"...")
            
        for t_id, t in self.agent.knowledge_base.theories.items():
            G.add_node(t_id, type='theory', label=t.name)
            
            # Connect theory to hypotheses
            for h in t.hypotheses:
                G.add_edge(t_id, h.id, type='explains')
        
        # Add evidence nodes
        for e in self.agent.recent_evidence:
            e_node_id = f"ev_{e.id[:8]}"
            G.add_node(e_node_id, type='evidence', label=f"Ev:{e.id[:6]}")
            G.add_edge(e_node_id, e.hypothesis_id, type='supports')
            
        # Draw
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        
        # Draw different node types
        node_types = nx.get_node_attributes(G, 'type')
        
        # Hypotheses
        h_nodes = [n for n, t in node_types.items() if t == 'hypothesis']
        h_colors = [self._get_status_color(G.nodes[n].get('status')) for n in h_nodes]
        h_sizes = [G.nodes[n].get('confidence', 0.5) * 1000 for n in h_nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=h_nodes, node_color=h_colors, 
                             node_size=h_sizes, alpha=0.8, node_shape='o')
        
        # Theories
        t_nodes = [n for n, t in node_types.items() if t == 'theory']
        nx.draw_networkx_nodes(G, pos, nodelist=t_nodes, node_color='purple',
                             node_size=2000, alpha=0.6, node_shape='s')
        
        # Evidence
        e_nodes = [n for n, t in node_types.items() if t == 'evidence']
        nx.draw_networkx_nodes(G, pos, nodelist=e_nodes, node_color='gray',
                             node_size=300, alpha=0.5, node_shape='^')
        
        # Labels
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        # Edges
        nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='gray')
        
        plt.title(f"Scientific Knowledge Graph - {self.agent.domain}")
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    def visualize_quantum_states(self, save_path: Optional[str] = None):
        """Visualize quantum hypothesis states."""
        states = self.agent.quantum_reasoner.hypothesis_superpositions
        if not states:
            print("No quantum states to visualize")
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 1. Complex Amplitude Plane
        amplitudes = [s.amplitude for s in states.values()]
        labels = [s.hypothesis.id[:10] for s in states.values()]
        
        real_parts = [a.real for a in amplitudes]
        imag_parts = [a.imag for a in amplitudes]
        probs = [abs(a)**2 for a in amplitudes]
        
        scatter = ax1.scatter(real_parts, imag_parts, c=probs, cmap='viridis', s=200)
        plt.colorbar(scatter, ax=ax1, label='Probability')
        
        for i, txt in enumerate(labels):
            ax1.annotate(txt, (real_parts[i], imag_parts[i]))
            
        # Draw unit circle
        circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--')
        ax1.add_artist(circle)
        
        ax1.set_xlim(-1.1, 1.1)
        ax1.set_ylim(-1.1, 1.1)
        ax1.set_xlabel('Real Amplitude (Confidence)')
        ax1.set_ylabel('Imaginary Amplitude (Phase/Context)')
        ax1.set_title('Quantum Hypothesis States (Hilbert Space)')
        ax1.grid(True)
        
        # 2. Entanglement Network
        G = self.agent.quantum_reasoner.entanglement_network
        if len(G.nodes) > 0:
            pos = nx.spring_layout(G)
            nx.draw(G, pos, ax=ax2, with_labels=True, node_color='lightblue', 
                   node_size=500, font_size=8)
            ax2.set_title('Hypothesis Entanglement Network')
        else:
            ax2.text(0.5, 0.5, "No Entanglement", ha='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def _get_status_color(self, status):
        """Get color for hypothesis status."""
        colors = {
            'PROPOSED': 'yellow',
            'TESTING': 'orange',
            'SUPPORTED': 'lightgreen',
            'WELL_SUPPORTED': 'green',
            'REFUTED': 'red',
            'DISCARDED': 'gray'
        }
        return colors.get(str(status), 'blue')
