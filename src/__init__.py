"""
Scientific Method Framework - Source Package
Re-exports core modules for convenient importing.
"""

from core.agent import *
from core.scientific_agent import *
from core.foundations import *
from core.visualization import *

__all__ = [
    'DeepScientificAgent',
    'KnowledgeBase',
    'Hypothesis',
    'ScientificParadigm',
    'EnhancedScientificVisualizer',
]
