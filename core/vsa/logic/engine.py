from typing import List, Any
import logging


class FormalLogicEngine:
    """
    Layer 2: Formal Logical Consistency.
    Provides basic logical validation without external dependencies.
    """
    
    def __init__(self):
        self.axioms = []
        self.statements = []
        logging.info("Formal Logic Engine initialized.")

    def add_axiom(self, name: str, formula: str):
        """Add a physical or domain-specific axiom."""
        self.axioms.append({"name": name, "formula": formula})
        logging.info(f"Axiom added: {name}")

    def validate_inference(self, premise: str, conclusion: str) -> bool:
        """
        Validate if a conclusion logically follows from a premise.
        
        Args:
            premise: The premise statement
            conclusion: The conclusion statement
            
        Returns:
            True if inference is valid, False otherwise
        """
        # Simple logical validation - check if conclusion keywords are in premise
        premise_lower = premise.lower()
        conclusion_lower = conclusion.lower()
        
        # Basic inference rules
        if "if" in premise_lower and "then" in premise_lower:
            # Modus ponens: if "if A then B" and "A" then "B"
            parts = premise_lower.split("then")
            if len(parts) == 2:
                antecedent = parts[0].replace("if", "").strip()
                consequent = parts[1].strip()
                if antecedent in conclusion_lower or consequent in conclusion_lower:
                    logging.info(f"Inference validated: {premise} -> {conclusion}")
                    return True
        
        # If conclusion is a subset of premise, it's a valid extraction
        conclusion_words = set(conclusion_lower.split())
        premise_words = set(premise_lower.split())
        if conclusion_words.issubset(premise_words):
            logging.info(f"Inference validated (subset): {premise} -> {conclusion}")
            return True
            
        logging.info(f"Inference invalid: {premise} -> {conclusion}")
        return False

    def check_consistency(self, statements: List[str]) -> bool:
        """
        Check if a set of statements is logically consistent.
        
        Args:
            statements: List of statements to check
            
        Returns:
            True if consistent, False if contradictions detected
        """
        # Store normalized statements for comparison
        normalized = [s.lower().strip() for s in statements]
        
        # Check for explicit contradictions
        for i, stmt1 in enumerate(normalized):
            for stmt2 in normalized[i + 1:]:
                # Check for negation patterns
                if self._are_contradictory(stmt1, stmt2):
                    stmt2_index = normalized.index(stmt2)
                    logging.warning(
                        f"Contradiction detected: '{statements[i]}' vs '{statements[stmt2_index]}'"
                    )
                    return False
        
        logging.info(f"Statements are consistent: {len(statements)} statements checked")
        return True
    
    def _are_contradictory(self, stmt1: str, stmt2: str) -> bool:
        """Check if two statements contradict each other."""
        # Remove common words
        stmt1_clean = stmt1.replace("not", "").replace("no", "").strip()
        stmt2_clean = stmt2.replace("not", "").replace("no", "").strip()
        
        # Check if one negates the other
        if ("not" in stmt1 or "no" in stmt1) and stmt1_clean in stmt2:
            return True
        if ("not" in stmt2 or "no" in stmt2) and stmt2_clean in stmt1:
            return True
            
        # Check for opposite claims
        if "increase" in stmt1 and "decrease" in stmt2:
            if any(word in stmt1 for word in stmt2.split()):
                return True
        if "decrease" in stmt1 and "increase" in stmt2:
            if any(word in stmt1 for word in stmt2.split()):
                return True
                
        return False

    def derive_implications(self, hypothesis: str) -> List[str]:
        """
        Derive logical implications from a hypothesis.
        
        Args:
            hypothesis: The hypothesis statement
            
        Returns:
            List of derived implications
        """
        implications = []
        hypothesis_lower = hypothesis.lower()
        
        # Extract key relationships and derive implications
        if "if" in hypothesis_lower and "then" in hypothesis_lower:
            # Extract antecedent and consequent
            parts = hypothesis_lower.split("then")
            if len(parts) == 2:
                antecedent = parts[0].replace("if", "").strip()
                consequent = parts[1].strip()
                
                # Contrapositive: if A then B => if not B then not A
                implications.append(f"If not ({consequent}) then not ({antecedent})")
                
        # If hypothesis mentions increase/decrease, derive magnitude implications
        if "increase" in hypothesis_lower:
            implications.append("Magnitude will be greater than baseline")
        elif "decrease" in hypothesis_lower:
            implications.append("Magnitude will be less than baseline")

        # If hypothesis mentions improvement/degradation
        if any(word in hypothesis_lower for word in ["improve", "better", "enhance"]):
            implications.append("Performance metric will increase")
        elif any(word in hypothesis_lower for word in ["degrade", "worse", "reduce"]):
            implications.append("Performance metric will decrease")
            
        logging.info(f"Derived {len(implications)} implications from hypothesis")
        return implications

    def verify_hypothesis(self, hypothesis_id: str, constraints: List[Any]) -> bool:
        """
        Verify if a hypothesis is logically valid (legacy compatibility).
        
        Args:
            hypothesis_id: Identifier for the hypothesis
            constraints: List of constraints (not used in simple implementation)
            
        Returns:
            True (simple implementation always validates)
        """
        logging.info(f"Hypothesis {hypothesis_id} verification: VALID")
        return True

    def check_contradiction(self, h1: List[Any], h2: List[Any]) -> bool:
        """
        Check if two hypotheses contradict each other (legacy compatibility).
        
        Args:
            h1: First hypothesis constraints
            h2: Second hypothesis constraints
            
        Returns:
            False (simple implementation doesn't detect contradictions via constraints)
        """
        return False
