"""
Negative Space Explorer Module

Explores the space of untested hypotheses - the realm of possible hypotheses
that haven't yet been formulated, tested, or validated.
"""

from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import logging

from .scientific_agent import Hypothesis, KnowledgeBase


@dataclass
class NegativeSpaceRegion:
    """Represents a region in the negative space."""
    id: str
    domain: str
    description: str
    potential_hypotheses: int
    explored_count: int
    priority_score: float
    related_concepts: List[str] = field(default_factory=list)


class NegativeSpaceExplorer:
    """
    Explores the space of untested hypotheses.
    
    The Negative Space represents all possible hypotheses that haven't
    been formulated or tested yet. This class provides methods to:
    - Map the unexplored hypothesis space
    - Generate novel hypotheses from the frontier
    - Track exploration coverage
    - Identify high-value areas to investigate
    """
    
    def __init__(self, knowledge_base: KnowledgeBase, domain: str):
        """
        Initialize the Negative Space Explorer.
        
        Args:
            knowledge_base: The knowledge base containing explored hypotheses
            domain: The domain of investigation
        """
        self.knowledge_base = knowledge_base
        self.domain = domain
        self.explored_space: Set[str] = set()
        self.frontier: List[Dict[str, Any]] = []
        self._initialize_exploration()
        logging.info(f"NegativeSpaceExplorer initialized for domain: {domain}")
        
    def _initialize_exploration(self):
        """Initialize the exploration by analyzing existing hypotheses."""
        # Mark existing hypotheses as explored
        for hyp_id, hypothesis in self.knowledge_base.hypotheses.items():
            if hypothesis.domain == self.domain:
                self.explored_space.add(hypothesis.statement.lower())
                
    def map_negative_space(self) -> Dict[str, Any]:
        """
        Map the unexplored hypothesis space.
        
        Returns:
            Dictionary containing:
            - explored_count: Number of explored hypotheses
            - total_estimated: Estimated total hypothesis space
            - frontier_regions: List of frontier regions
            - coverage: Exploration coverage percentage
        """
        explored_count = len(self.explored_space)
        
        # Analyze knowledge base to find conceptual gaps
        concepts = self._extract_concepts()
        relationships = self._extract_relationships()
        
        # Estimate total space based on combinatorial analysis
        # Simple heuristic: concepts^2 * relationships
        total_estimated = max(len(concepts) ** 2 * len(relationships), 100)
        
        # Identify frontier regions
        frontier_regions = self._identify_frontier_regions(concepts, relationships)
        
        coverage = explored_count / total_estimated if total_estimated > 0 else 0.0
        
        neg_space_map = {
            "domain": self.domain,
            "explored_count": explored_count,
            "total_estimated": total_estimated,
            "frontier_regions": frontier_regions,
            "coverage": coverage,
            "concepts": list(concepts),
            "relationships": list(relationships),
            "timestamp": datetime.now().isoformat()
        }
        
        logging.info(f"Negative space mapped: {coverage*100:.2f}% coverage")
        return neg_space_map
        
    def _extract_concepts(self) -> Set[str]:
        """Extract key concepts from existing hypotheses."""
        concepts = set()
        for hypothesis in self.knowledge_base.hypotheses.values():
            if hypothesis.domain == self.domain:
                # Extract words from statement (simple word-based concept extraction)
                words = hypothesis.statement.lower().split()
                concepts.update(word for word in words if len(word) > 3)
                # Add variables as concepts
                concepts.update(hypothesis.variables.keys())
        return concepts
        
    def _extract_relationships(self) -> Set[str]:
        """Extract relationship types from existing hypotheses."""
        relationships = set()
        for hypothesis in self.knowledge_base.hypotheses.values():
            if hypothesis.domain == self.domain:
                relationships.update(hypothesis.relationships)
        # Add default relationship types if none exist
        if not relationships:
            relationships = {"causes", "correlates_with", "influences", "depends_on"}
        return relationships
        
    def _identify_frontier_regions(self, concepts: Set[str], relationships: Set[str]) -> List[Dict[str, Any]]:
        """Identify high-potential frontier regions."""
        frontier_regions = []
        
        # Region 1: Unexplored concept combinations
        unexplored_combinations = self._find_unexplored_combinations(concepts, relationships)
        if unexplored_combinations:
            frontier_regions.append({
                "type": "unexplored_combinations",
                "description": "Novel combinations of existing concepts",
                "potential_count": len(unexplored_combinations),
                "priority": 0.8
            })
            
        # Region 2: Adjacent concepts (concepts mentioned but not deeply explored)
        adjacent_concepts = self._find_adjacent_concepts(concepts)
        if adjacent_concepts:
            frontier_regions.append({
                "type": "adjacent_concepts",
                "description": "Related concepts at the periphery",
                "concepts": list(adjacent_concepts)[:10],
                "priority": 0.6
            })
            
        # Region 3: Inverse relationships
        frontier_regions.append({
            "type": "inverse_relationships",
            "description": "Inverse or negated versions of known relationships",
            "potential_count": len(relationships) * 2,
            "priority": 0.5
        })
        
        return frontier_regions
        
    def _find_unexplored_combinations(self, concepts: Set[str], relationships: Set[str]) -> List[Dict[str, str]]:
        """Find combinations of concepts and relationships not yet explored."""
        unexplored = []
        concepts_list = list(concepts)[:10]  # Limit for practicality
        
        for i, concept1 in enumerate(concepts_list):
            for concept2 in concepts_list[i+1:]:
                for relationship in relationships:
                    # Generate hypothesis statement
                    statement = f"{concept1} {relationship} {concept2}"
                    if statement.lower() not in self.explored_space:
                        unexplored.append({
                            "concept1": concept1,
                            "concept2": concept2,
                            "relationship": relationship,
                            "statement": statement
                        })
        return unexplored[:50]  # Return top 50
        
    def _find_adjacent_concepts(self, concepts: Set[str]) -> Set[str]:
        """Find concepts that are adjacent but not fully explored."""
        # In a real implementation, this could use word embeddings or domain ontologies
        # For now, simple approach: find concepts mentioned in relationships but not as primary
        adjacent = set()
        for hypothesis in self.knowledge_base.hypotheses.values():
            if hypothesis.domain == self.domain:
                # Check for concepts in relationships that aren't in main concepts
                for rel in hypothesis.relationships:
                    words = rel.split('_')
                    for word in words:
                        if word not in concepts and len(word) > 3:
                            adjacent.add(word)
        return adjacent
        
    def generate_frontier_hypotheses(self, count: int = 5) -> List[Hypothesis]:
        """
        Generate novel hypotheses at the frontier of knowledge.
        
        Args:
            count: Number of hypotheses to generate
            
        Returns:
            List of newly generated hypotheses
        """
        concepts = self._extract_concepts()
        relationships = self._extract_relationships()
        unexplored = self._find_unexplored_combinations(concepts, relationships)
        
        generated_hypotheses = []
        
        for i, combo in enumerate(unexplored[:count]):
            hypothesis_id = f"h_neg_{uuid.uuid4().hex[:8]}"
            
            hypothesis = Hypothesis(
                id=hypothesis_id,
                statement=combo["statement"],
                variables={
                    "var1": combo["concept1"],
                    "var2": combo["concept2"]
                },
                relationships=[combo["relationship"]],
                domain=self.domain,
                timestamp=datetime.now(),
                confidence=0.3,  # Low initial confidence for generated hypotheses
                complexity=0.5,
                novelty=0.9,  # High novelty as they're from negative space
                testability=0.7
            )
            
            generated_hypotheses.append(hypothesis)
            self.explored_space.add(combo["statement"].lower())
            
        logging.info(f"Generated {len(generated_hypotheses)} frontier hypotheses")
        return generated_hypotheses
        
    def calculate_exploration_coverage(self) -> float:
        """
        Calculate what percentage of possible space has been explored.
        
        Returns:
            Coverage as a float between 0.0 and 1.0
        """
        neg_space_map = self.map_negative_space()
        coverage = neg_space_map["coverage"]
        logging.info(f"Exploration coverage: {coverage*100:.2f}%")
        return coverage
        
    def identify_high_value_regions(self) -> List[Dict[str, Any]]:
        """
        Find promising unexplored areas based on various heuristics.
        
        Returns:
            List of high-value regions sorted by priority
        """
        concepts = self._extract_concepts()
        relationships = self._extract_relationships()
        
        high_value_regions = []
        
        # Region 1: High-testability unexplored areas
        unexplored = self._find_unexplored_combinations(concepts, relationships)
        if unexplored:
            high_value_regions.append({
                "id": f"hvr_{uuid.uuid4().hex[:8]}",
                "type": "high_testability",
                "description": "Combinations with high testability potential",
                "sample_hypotheses": [u["statement"] for u in unexplored[:3]],
                "estimated_hypotheses": len(unexplored),
                "priority_score": 0.9,
                "reasoning": "These combinations use well-understood concepts with clear relationships"
            })
            
        # Region 2: Novel concept integration
        adjacent_concepts = self._find_adjacent_concepts(concepts)
        if adjacent_concepts:
            high_value_regions.append({
                "id": f"hvr_{uuid.uuid4().hex[:8]}",
                "type": "novel_integration",
                "description": "Integration of adjacent concepts into main theory",
                "concepts": list(adjacent_concepts)[:5],
                "estimated_hypotheses": len(adjacent_concepts) * len(concepts),
                "priority_score": 0.7,
                "reasoning": "These concepts appear in relationships but aren't fully integrated"
            })
            
        # Region 3: Contradiction exploration
        high_value_regions.append({
            "id": f"hvr_{uuid.uuid4().hex[:8]}",
            "type": "contradiction_space",
            "description": "Negations and contradictions of supported hypotheses",
            "estimated_hypotheses": len([h for h in self.knowledge_base.hypotheses.values() 
                                        if h.domain == self.domain]),
            "priority_score": 0.6,
            "reasoning": "Testing contradictions can strengthen or refute current knowledge"
        })
        
        # Sort by priority score
        high_value_regions.sort(key=lambda x: x["priority_score"], reverse=True)
        
        logging.info(f"Identified {len(high_value_regions)} high-value regions")
        return high_value_regions
