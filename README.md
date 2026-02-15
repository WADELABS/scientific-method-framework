# Scientific-Method: The Professor's Revenge 🔬

> **"State of Doubt is the precursor to Wisdom."**

The **Scientific-Method Framework** is a Cognitive Guardrail for Large Language Models. It solves the "Academic Arms Race" by forcing AI agents out of the "Confident Liar" state and into a rigorous "Hypothesis -> Research -> Synthesis" pipeline.

## 🏛️ The Problem: Intellectual Laziness
In the current LLM landscape, AI generates fluent but unverified claims. Students submit these "confidently hallucinated" papers, skipping the "messy middle" of actual research.

## 🛡️ The Solution: Empirical Validation Substrate
This framework refactors the AI's cognitive process to mirror a PhD candidate's laboratory workflow:

1.  **Hypothesis Generation**: The AI's intuition is captured as an `UNVERIFIED_CLAIM`. It is never presented to the user at this stage.
2.  **The Trial by Fire (Active Research)**: The agent designs search queries and retrieves data from a **Strict Source Registry** (.edu, .gov, peer-reviewed databases).
3.  **Conflict Detection**: Evidence is cross-verified. Discrepancies between the AI's intuition and external facts trigger a `REFINE_OR_REJECT` loop.
4.  **Synthesis & Provenance**: The final conclusion is delivered with a complete **Research Log**, ensuring zero-hallucination outputs.

## ⚙️ Architecture

![Scientific Method Diagram](images/scientific_method_diagram.jpg)

### Core Components
- **`main.py`**: Orchestrates the `ScientificAgent` using a "Doubt First" methodology.
- **`credibility.py`**: The **Substrate Registry** that enforces academic-grade source requirements.
- **`research.py`**: The **Active Researcher** that performs cross-verification and conflict detection.

## 🚀 Deployment

```bash
# Initialize the PhD Agent
python -m src.scientific_method.main
```

---
*Part of the WADELABS Precision Engineering Suite. Zero-Friction. Zero-Hallucination.*
