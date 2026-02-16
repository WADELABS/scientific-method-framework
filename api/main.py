"""
Scientific Method Framework REST API

FastAPI implementation providing REST endpoints for hypothesis management,
experiment execution, provenance tracking, and negative space exploration.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import logging

# Import core SMF components
from core.scientific_agent import (
    ScientificAgent, KnowledgeBase, Hypothesis, Experiment, 
    Evidence, Theory, HypothesisStatus
)
from core.vsa.provenance.ledger import MerkleLedger
from core.negative_space import NegativeSpaceExplorer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Scientific Method Framework API",
    version="1.0.0",
    description="REST API for the Verifiable Scientific Agent Framework",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global instances (in production, use dependency injection)
kb = KnowledgeBase()
agents: Dict[str, ScientificAgent] = {}
ledger = MerkleLedger(db_path="provenance.db")
explorers: Dict[str, NegativeSpaceExplorer] = {}


# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================

class HypothesisStatusEnum(str, Enum):
    """Hypothesis status enumeration."""
    PROPOSED = "PROPOSED"
    TESTING = "TESTING"
    SUPPORTED = "SUPPORTED"
    WELL_SUPPORTED = "WELL_SUPPORTED"
    REFUTED = "REFUTED"
    DISCARDED = "DISCARDED"


class HypothesisCreate(BaseModel):
    """Request model for creating a hypothesis."""
    statement: str = Field(..., min_length=10, description="Hypothesis statement")
    variables: Dict[str, str] = Field(default_factory=dict, description="Variables involved")
    relationships: List[str] = Field(default_factory=list, description="Relationship types")
    domain: str = Field(..., description="Research domain")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Initial confidence level")
    complexity: float = Field(..., ge=0.0, le=1.0, description="Complexity score")
    novelty: float = Field(..., ge=0.0, le=1.0, description="Novelty score")
    testability: float = Field(..., ge=0.0, le=1.0, description="Testability score")

    class Config:
        schema_extra = {
            "example": {
                "statement": "Increased temperature accelerates chemical reaction rate",
                "variables": {
                    "independent": "temperature",
                    "dependent": "reaction_rate"
                },
                "relationships": ["accelerates", "affects"],
                "domain": "chemistry",
                "confidence": 0.7,
                "complexity": 0.5,
                "novelty": 0.6,
                "testability": 0.9
            }
        }


class HypothesisResponse(BaseModel):
    """Response model for hypothesis operations."""
    id: str
    statement: str
    status: str
    confidence: float
    domain: str
    created_at: str
    novelty: float
    testability: float

    class Config:
        schema_extra = {
            "example": {
                "id": "h_abc123",
                "statement": "Increased temperature accelerates chemical reaction rate",
                "status": "PROPOSED",
                "confidence": 0.7,
                "domain": "chemistry",
                "created_at": "2026-02-16T14:30:00",
                "novelty": 0.6,
                "testability": 0.9
            }
        }


class ExperimentSubmit(BaseModel):
    """Request model for submitting an experiment."""
    hypothesis_id: str = Field(..., description="ID of hypothesis to test")
    design: Dict[str, Any] = Field(default_factory=dict, description="Experiment design")
    conditions: List[str] = Field(default_factory=list, description="Experimental conditions")
    controls: List[str] = Field(default_factory=list, description="Control conditions")
    measurements: List[str] = Field(default_factory=list, description="Measurements to collect")
    sample_size: int = Field(..., gt=0, description="Sample size")

    class Config:
        schema_extra = {
            "example": {
                "hypothesis_id": "h_abc123",
                "design": {"type": "controlled_experiment", "duration": "30min"},
                "conditions": ["25°C", "50°C", "75°C"],
                "controls": ["baseline_measurement"],
                "measurements": ["reaction_time", "product_yield"],
                "sample_size": 100
            }
        }


class ExperimentResponse(BaseModel):
    """Response model for experiment operations."""
    id: str
    hypothesis_id: str
    status: str
    created_at: str
    sample_size: int


class ExperimentResults(BaseModel):
    """Response model for experiment results."""
    experiment_id: str
    hypothesis_id: str
    results: Optional[Dict[str, Any]]
    analysis: Optional[Dict[str, Any]]
    status: str
    recorded_to_ledger: bool
    ledger_block_hash: Optional[str]


class LedgerBlock(BaseModel):
    """Response model for ledger block."""
    block_id: int
    block_hash: str
    timestamp: str
    data: Dict[str, Any]
    prev_hash: str


class LedgerVerification(BaseModel):
    """Response model for ledger verification."""
    valid: bool
    total_blocks: int
    verification_timestamp: str
    message: str


class NegativeSpaceMap(BaseModel):
    """Response model for negative space mapping."""
    domain: str
    explored_count: int
    total_estimated: int
    coverage: float
    frontier_regions: List[Dict[str, Any]]
    timestamp: str


class FrontierHypotheses(BaseModel):
    """Response model for frontier hypothesis generation."""
    count: int
    hypotheses: List[HypothesisResponse]
    timestamp: str


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str
    version: str
    timestamp: str


# ============================================================================
# Helper Functions
# ============================================================================

def get_or_create_agent(domain: str) -> ScientificAgent:
    """Get existing agent or create new one for domain."""
    if domain not in agents:
        agents[domain] = ScientificAgent(domain=domain, knowledge_base=kb)
        logger.info(f"Created new agent for domain: {domain}")
    return agents[domain]


def get_or_create_explorer(domain: str) -> NegativeSpaceExplorer:
    """Get existing explorer or create new one for domain."""
    if domain not in explorers:
        explorers[domain] = NegativeSpaceExplorer(kb, domain=domain)
        logger.info(f"Created new explorer for domain: {domain}")
    return explorers[domain]


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/v1/hypotheses", response_model=HypothesisResponse, status_code=status.HTTP_201_CREATED)
async def create_hypothesis(hypothesis: HypothesisCreate):
    """
    Create a new hypothesis.
    
    Creates a hypothesis and adds it to the knowledge base.
    Returns the created hypothesis with its assigned ID.
    """
    try:
        # Generate unique ID
        hypothesis_id = f"h_{uuid.uuid4().hex[:8]}"
        
        # Create Hypothesis object
        hyp = Hypothesis(
            id=hypothesis_id,
            statement=hypothesis.statement,
            variables=hypothesis.variables,
            relationships=hypothesis.relationships,
            domain=hypothesis.domain,
            timestamp=datetime.now(),
            confidence=hypothesis.confidence,
            complexity=hypothesis.complexity,
            novelty=hypothesis.novelty,
            testability=hypothesis.testability,
            status=HypothesisStatus.PROPOSED
        )
        
        # Add to knowledge base
        kb.add_hypothesis(hyp)
        
        # Record to ledger
        ledger_entry = {
            "type": "hypothesis_created",
            "hypothesis_id": hypothesis_id,
            "statement": hypothesis.statement,
            "domain": hypothesis.domain,
            "timestamp": datetime.now().isoformat()
        }
        block_hash = ledger.add_entry(ledger_entry)
        
        logger.info(f"Created hypothesis: {hypothesis_id} (ledger: {block_hash[:16]}...)")
        
        return HypothesisResponse(
            id=hyp.id,
            statement=hyp.statement,
            status=hyp.status.name,
            confidence=hyp.confidence,
            domain=hyp.domain,
            created_at=hyp.timestamp.isoformat(),
            novelty=hyp.novelty,
            testability=hyp.testability
        )
        
    except Exception as e:
        logger.error(f"Error creating hypothesis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create hypothesis: {str(e)}"
        )


@app.get("/api/v1/hypotheses/{hypothesis_id}", response_model=HypothesisResponse)
async def get_hypothesis(hypothesis_id: str):
    """
    Get hypothesis by ID.
    
    Retrieves detailed information about a specific hypothesis.
    """
    if hypothesis_id not in kb.hypotheses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hypothesis {hypothesis_id} not found"
        )
    
    hyp = kb.hypotheses[hypothesis_id]
    
    return HypothesisResponse(
        id=hyp.id,
        statement=hyp.statement,
        status=hyp.status.name,
        confidence=hyp.confidence,
        domain=hyp.domain,
        created_at=hyp.timestamp.isoformat(),
        novelty=hyp.novelty,
        testability=hyp.testability
    )


@app.get("/api/v1/hypotheses", response_model=List[HypothesisResponse])
async def list_hypotheses(domain: Optional[str] = None, status: Optional[str] = None):
    """
    List all hypotheses, optionally filtered by domain and/or status.
    """
    hypotheses = list(kb.hypotheses.values())
    
    # Filter by domain
    if domain:
        hypotheses = [h for h in hypotheses if h.domain == domain]
    
    # Filter by status
    if status:
        try:
            status_enum = HypothesisStatus[status.upper()]
            hypotheses = [h for h in hypotheses if h.status == status_enum]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status}"
            )
    
    return [
        HypothesisResponse(
            id=h.id,
            statement=h.statement,
            status=h.status.name,
            confidence=h.confidence,
            domain=h.domain,
            created_at=h.timestamp.isoformat(),
            novelty=h.novelty,
            testability=h.testability
        )
        for h in hypotheses
    ]


@app.post("/api/v1/experiments", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
async def submit_experiment(experiment: ExperimentSubmit):
    """
    Submit an experiment for execution.
    
    Creates an experiment design linked to a hypothesis.
    In production, this would trigger execution in The Crucible.
    """
    # Verify hypothesis exists
    if experiment.hypothesis_id not in kb.hypotheses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hypothesis {experiment.hypothesis_id} not found"
        )
    
    try:
        # Generate experiment ID
        experiment_id = f"exp_{uuid.uuid4().hex[:8]}"
        
        # Create Experiment object
        exp = Experiment(
            id=experiment_id,
            hypothesis_id=experiment.hypothesis_id,
            design=experiment.design,
            conditions=experiment.conditions,
            controls=experiment.controls,
            measurements=experiment.measurements,
            sample_size=experiment.sample_size,
            randomization_procedure="standard",
            statistical_tests=["anova", "t-test"]
        )
        
        # Add to knowledge base
        kb.experiments[experiment_id] = exp
        
        # Record to ledger (pre-registration)
        ledger_entry = {
            "type": "experiment_pre_registration",
            "experiment_id": experiment_id,
            "hypothesis_id": experiment.hypothesis_id,
            "design": experiment.design,
            "sample_size": experiment.sample_size,
            "timestamp": datetime.now().isoformat()
        }
        block_hash = ledger.add_entry(ledger_entry)
        
        logger.info(f"Submitted experiment: {experiment_id} (ledger: {block_hash[:16]}...)")
        
        return ExperimentResponse(
            id=exp.id,
            hypothesis_id=exp.hypothesis_id,
            status="submitted",
            created_at=datetime.now().isoformat(),
            sample_size=exp.sample_size
        )
        
    except Exception as e:
        logger.error(f"Error submitting experiment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit experiment: {str(e)}"
        )


@app.get("/api/v1/experiments/{experiment_id}/results", response_model=ExperimentResults)
async def get_experiment_results(experiment_id: str):
    """
    Get experiment results.
    
    Retrieves results and analysis for a completed experiment.
    """
    if experiment_id not in kb.experiments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment {experiment_id} not found"
        )
    
    exp = kb.experiments[experiment_id]
    
    # Determine status
    if exp.results is None:
        exp_status = "pending"
        recorded_to_ledger = False
        ledger_block_hash = None
    else:
        exp_status = "completed"
        recorded_to_ledger = True
        # In production, retrieve actual block hash
        ledger_block_hash = "simulated_block_hash"
    
    return ExperimentResults(
        experiment_id=exp.id,
        hypothesis_id=exp.hypothesis_id,
        results=exp.results,
        analysis=exp.analysis,
        status=exp_status,
        recorded_to_ledger=recorded_to_ledger,
        ledger_block_hash=ledger_block_hash
    )


@app.get("/api/v1/ledger/blocks/{block_id}", response_model=LedgerBlock)
async def get_ledger_block(block_id: int):
    """
    Get ledger block by ID.
    
    Retrieves a specific block from the provenance ledger.
    """
    import sqlite3
    
    try:
        with sqlite3.connect(ledger.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, prev_hash, timestamp, data_json, block_hash FROM blocks WHERE id = ?",
                (block_id,)
            )
            row = cursor.fetchone()
            
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Block {block_id} not found"
                )
            
            import json
            block_data = json.loads(row[3])
            
            return LedgerBlock(
                block_id=row[0],
                prev_hash=row[1],
                timestamp=row[2],
                data=block_data,
                block_hash=row[4]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving block: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve block: {str(e)}"
        )


@app.post("/api/v1/ledger/verify", response_model=LedgerVerification)
async def verify_ledger():
    """
    Verify integrity of the provenance chain.
    
    Validates the entire Merkle Ledger chain to ensure no tampering.
    """
    try:
        is_valid = ledger.verify_chain()
        
        # Count blocks
        import sqlite3
        with sqlite3.connect(ledger.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM blocks")
            total_blocks = cursor.fetchone()[0]
        
        return LedgerVerification(
            valid=is_valid,
            total_blocks=total_blocks,
            verification_timestamp=datetime.now().isoformat(),
            message="Chain integrity verified" if is_valid else "Chain integrity compromised"
        )
        
    except Exception as e:
        logger.error(f"Error verifying ledger: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify ledger: {str(e)}"
        )


@app.get("/api/v1/negative-space/map", response_model=NegativeSpaceMap)
async def map_negative_space(domain: str):
    """
    Get current negative space mapping for a domain.
    
    Analyzes the unexplored hypothesis space and returns coverage metrics.
    """
    try:
        explorer = get_or_create_explorer(domain)
        neg_space_map = explorer.map_negative_space()
        
        return NegativeSpaceMap(
            domain=neg_space_map["domain"],
            explored_count=neg_space_map["explored_count"],
            total_estimated=neg_space_map["total_estimated"],
            coverage=neg_space_map["coverage"],
            frontier_regions=neg_space_map["frontier_regions"],
            timestamp=neg_space_map["timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Error mapping negative space: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to map negative space: {str(e)}"
        )


@app.post("/api/v1/negative-space/generate", response_model=FrontierHypotheses)
async def generate_frontier_hypotheses(domain: str, count: int = 5):
    """
    Generate new hypotheses from the exploration frontier.
    
    Creates novel hypotheses from unexplored regions of the hypothesis space.
    """
    if count < 1 or count > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Count must be between 1 and 50"
        )
    
    try:
        explorer = get_or_create_explorer(domain)
        hypotheses = explorer.generate_frontier_hypotheses(count=count)
        
        # Add to knowledge base
        for hyp in hypotheses:
            kb.add_hypothesis(hyp)
        
        # Convert to response format
        hypothesis_responses = [
            HypothesisResponse(
                id=h.id,
                statement=h.statement,
                status=h.status.name,
                confidence=h.confidence,
                domain=h.domain,
                created_at=h.timestamp.isoformat(),
                novelty=h.novelty,
                testability=h.testability
            )
            for h in hypotheses
        ]
        
        logger.info(f"Generated {len(hypotheses)} frontier hypotheses for domain: {domain}")
        
        return FrontierHypotheses(
            count=len(hypotheses),
            hypotheses=hypothesis_responses,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error generating frontier hypotheses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate hypotheses: {str(e)}"
        )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("SMF API starting up...")
    logger.info(f"Merkle Ledger: {ledger.db_path}")
    logger.info("SMF API ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("SMF API shutting down...")
    logger.info("SMF API stopped")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
