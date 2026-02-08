# The Verifiable Scientific Agent (VSA)

## 🏛️ Core Architecture: The Reproducible Scientific Method

**Current Status:** Prototype / Concept  
**Domain:** Cognitive Science / CI/CD for Truth

### Overview
The Verifiable Scientific Agent (VSA) is an attempt to solve the "Hallucination Problem" in Large Language Models not by training, but by architecture. It enforces the scientific method as a computational constraint.

### Key Innovations

1.  **Complete Provenance Tracking**
    *   Every operation has a cryptographic checksum (SHA-256).
    *   All inputs, parameters, and execution environments are recorded in an immutable ledger.

2.  **Citation-Embedded Knowledge**
    *   Every claim is linked to a verifiable source (DOI, ISBN, URL).
    *   Automatic generation of BibTeX references.

3.  **Reflective Learning Loop**
    *   The agent monitors its own "Hypothesis Success Rate."
    *   It auto-tunes detailed parameters (e.g., sample size multipliers) based on past performance.

4.  **Statistical Rigor by Design**
    *   Enforced power analysis before experimentation.
    *   Mandatory assumption checking (normality, homogeneity) for all statistical tests.

### Project Goals
*   **From "Guessing" to "Proving":** Move AI from probabilistic token generation to verifiable, reproducible logic.
*   **Automated Discovery:** Enable agents to conduct autonomous research cycles that human scientists can trust.

### Usage
See `vsa.py` for the core implementation of the `ReflectiveScientificAgent`.
