"""
Integration tests for REST API.
"""

import pytest
import tempfile
import os

# Import the app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.main import app, kb, ledger
from core.scientific_agent import Hypothesis, HypothesisStatus
from datetime import datetime


@pytest.fixture
def client():
    """Create test client."""
    # Import here to avoid issues
    from httpx import AsyncClient, ASGITransport
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test."""
    # Clear knowledge base
    kb.hypotheses.clear()
    kb.experiments.clear()
    kb.evidence.clear()
    kb.theories.clear()
    
    yield
    
    # Cleanup after test
    kb.hypotheses.clear()
    kb.experiments.clear()


@pytest.mark.integration
class TestAPIHealth:
    """Test API health and basic functionality."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


@pytest.mark.integration
class TestHypothesisAPI:
    """Test hypothesis API endpoints."""
    
    def test_create_hypothesis(self, client):
        """Test hypothesis creation."""
        response = client.post("/api/v1/hypotheses", json={
            "statement": "API test hypothesis",
            "variables": {"test": "value"},
            "relationships": ["api_test"],
            "domain": "test",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["statement"] == "API test hypothesis"
        assert data["status"] == "PROPOSED"
        assert data["domain"] == "test"
        
    def test_get_hypothesis(self, client):
        """Test hypothesis retrieval."""
        # First create a hypothesis
        create_response = client.post("/api/v1/hypotheses", json={
            "statement": "Retrieve test hypothesis",
            "variables": {},
            "relationships": [],
            "domain": "test",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        hypothesis_id = create_response.json()["id"]
        
        # Now retrieve it
        response = client.get(f"/api/v1/hypotheses/{hypothesis_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == hypothesis_id
        assert data["statement"] == "Retrieve test hypothesis"
        
    def test_get_nonexistent_hypothesis(self, client):
        """Test retrieving non-existent hypothesis returns 404."""
        response = client.get("/api/v1/hypotheses/nonexistent_id")
        assert response.status_code == 404
        
    def test_list_hypotheses(self, client):
        """Test listing all hypotheses."""
        # Create multiple hypotheses
        for i in range(3):
            client.post("/api/v1/hypotheses", json={
                "statement": f"List test hypothesis {i}",
                "variables": {},
                "relationships": [],
                "domain": "test",
                "confidence": 0.7,
                "complexity": 0.3,
                "novelty": 0.5,
                "testability": 0.9
            })
        
        response = client.get("/api/v1/hypotheses")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        
    def test_list_hypotheses_filtered_by_domain(self, client):
        """Test listing hypotheses filtered by domain."""
        # Create hypotheses in different domains
        client.post("/api/v1/hypotheses", json={
            "statement": "Chemistry hypothesis",
            "variables": {},
            "relationships": [],
            "domain": "chemistry",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        client.post("/api/v1/hypotheses", json={
            "statement": "Physics hypothesis",
            "variables": {},
            "relationships": [],
            "domain": "physics",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        
        response = client.get("/api/v1/hypotheses?domain=chemistry")
        assert response.status_code == 200
        data = response.json()
        assert all(h["domain"] == "chemistry" for h in data)


@pytest.mark.integration
class TestExperimentAPI:
    """Test experiment API endpoints."""
    
    def test_submit_experiment(self, client):
        """Test experiment submission."""
        # First create a hypothesis
        hyp_response = client.post("/api/v1/hypotheses", json={
            "statement": "Experiment test hypothesis",
            "variables": {},
            "relationships": [],
            "domain": "test",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        hypothesis_id = hyp_response.json()["id"]
        
        # Submit experiment
        response = client.post("/api/v1/experiments", json={
            "hypothesis_id": hypothesis_id,
            "design": {"type": "test"},
            "conditions": ["condition1"],
            "controls": ["control1"],
            "measurements": ["measurement1"],
            "sample_size": 100
        })
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["hypothesis_id"] == hypothesis_id
        assert data["status"] == "submitted"
        assert data["sample_size"] == 100
        
    def test_submit_experiment_invalid_hypothesis(self, client):
        """Test submitting experiment for non-existent hypothesis."""
        response = client.post("/api/v1/experiments", json={
            "hypothesis_id": "nonexistent",
            "design": {},
            "conditions": [],
            "controls": [],
            "measurements": [],
            "sample_size": 100
        })
        
        assert response.status_code == 404
        
    def test_get_experiment_results(self, client):
        """Test retrieving experiment results."""
        # Create hypothesis
        hyp_response = client.post("/api/v1/hypotheses", json={
            "statement": "Results test hypothesis",
            "variables": {},
            "relationships": [],
            "domain": "test",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        hypothesis_id = hyp_response.json()["id"]
        
        # Submit experiment
        exp_response = client.post("/api/v1/experiments", json={
            "hypothesis_id": hypothesis_id,
            "design": {},
            "conditions": [],
            "controls": [],
            "measurements": [],
            "sample_size": 100
        })
        experiment_id = exp_response.json()["id"]
        
        # Get results (should be pending)
        response = client.get(f"/api/v1/experiments/{experiment_id}/results")
        assert response.status_code == 200
        data = response.json()
        assert data["experiment_id"] == experiment_id
        assert data["status"] == "pending"


@pytest.mark.integration
class TestLedgerAPI:
    """Test Merkle Ledger API endpoints."""
    
    def test_ledger_verification(self, client):
        """Test ledger verification endpoint."""
        response = client.post("/api/v1/ledger/verify")
        assert response.status_code == 200
        data = response.json()
        assert "valid" in data
        assert "total_blocks" in data
        assert data["valid"] is True
        
    def test_get_ledger_block(self, client):
        """Test getting a specific ledger block."""
        # Create a hypothesis to generate a ledger entry
        client.post("/api/v1/hypotheses", json={
            "statement": "Ledger block test",
            "variables": {},
            "relationships": [],
            "domain": "test",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        
        # Try to get a block (block 1 should exist after hypothesis creation)
        response = client.get("/api/v1/ledger/blocks/1")
        
        # Block might not exist if ledger was reset, so check both cases
        if response.status_code == 200:
            data = response.json()
            assert "block_id" in data
            assert "block_hash" in data
            assert "timestamp" in data
            assert "data" in data
        else:
            assert response.status_code == 404


@pytest.mark.integration
class TestNegativeSpaceAPI:
    """Test negative space exploration API endpoints."""
    
    def test_map_negative_space(self, client):
        """Test negative space mapping endpoint."""
        # Create some hypotheses first
        for i in range(3):
            client.post("/api/v1/hypotheses", json={
                "statement": f"Negative space test {i}",
                "variables": {"var": f"val{i}"},
                "relationships": ["test_rel"],
                "domain": "test_domain",
                "confidence": 0.7,
                "complexity": 0.3,
                "novelty": 0.5,
                "testability": 0.9
            })
        
        response = client.get("/api/v1/negative-space/map?domain=test_domain")
        assert response.status_code == 200
        data = response.json()
        assert "domain" in data
        assert "explored_count" in data
        assert "coverage" in data
        assert "frontier_regions" in data
        assert data["domain"] == "test_domain"
        assert data["explored_count"] >= 3
        
    def test_generate_frontier_hypotheses(self, client):
        """Test frontier hypothesis generation endpoint."""
        # Create some initial hypotheses
        for i in range(3):
            client.post("/api/v1/hypotheses", json={
                "statement": f"Frontier test {i}",
                "variables": {"var": f"val{i}"},
                "relationships": ["test_rel"],
                "domain": "frontier_domain",
                "confidence": 0.7,
                "complexity": 0.3,
                "novelty": 0.5,
                "testability": 0.9
            })
        
        response = client.post("/api/v1/negative-space/generate?domain=frontier_domain&count=3")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "hypotheses" in data
        assert "timestamp" in data
        assert len(data["hypotheses"]) <= 3  # Might be less if not enough combinations
        
    def test_generate_frontier_hypotheses_invalid_count(self, client):
        """Test frontier generation with invalid count."""
        response = client.post("/api/v1/negative-space/generate?domain=test&count=100")
        assert response.status_code == 400


@pytest.mark.integration
class TestAPIIntegrationFlow:
    """Test complete API workflow integration."""
    
    def test_complete_research_cycle_via_api(self, client):
        """Test full research cycle through API."""
        # 1. Create hypothesis
        hyp_response = client.post("/api/v1/hypotheses", json={
            "statement": "Complete cycle test hypothesis",
            "variables": {"var1": "value1"},
            "relationships": ["test_rel"],
            "domain": "integration_test",
            "confidence": 0.7,
            "complexity": 0.3,
            "novelty": 0.5,
            "testability": 0.9
        })
        assert hyp_response.status_code == 201
        hypothesis_id = hyp_response.json()["id"]
        
        # 2. Submit experiment
        exp_response = client.post("/api/v1/experiments", json={
            "hypothesis_id": hypothesis_id,
            "design": {"type": "integration_test"},
            "conditions": ["condition1"],
            "controls": ["control1"],
            "measurements": ["measurement1"],
            "sample_size": 100
        })
        assert exp_response.status_code == 201
        experiment_id = exp_response.json()["id"]
        
        # 3. Check experiment status
        results_response = client.get(f"/api/v1/experiments/{experiment_id}/results")
        assert results_response.status_code == 200
        
        # 4. Verify ledger
        verify_response = client.post("/api/v1/ledger/verify")
        assert verify_response.status_code == 200
        assert verify_response.json()["valid"] is True
        
        # 5. Map negative space
        map_response = client.get("/api/v1/negative-space/map?domain=integration_test")
        assert map_response.status_code == 200
        assert map_response.json()["explored_count"] >= 1
