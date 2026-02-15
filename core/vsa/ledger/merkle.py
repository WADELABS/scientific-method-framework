import hashlib
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

class MerkleBlock:
    """Represents a single block in the Merkle ledger."""
    
    def __init__(self, index: int, data: Any, previous_hash: str):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute SHA-256 hash of the block."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": str(self.data),
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class MerkleLedger:
    """
    Merkle Ledger for cryptographic provenance tracking.
    Provides an immutable chain of blocks for scientific data provenance.
    """
    
    def __init__(self):
        self.chain: List[MerkleBlock] = []
        self._create_genesis_block()
        logging.info("Merkle Ledger initialized with genesis block.")
    
    def _create_genesis_block(self):
        """Create the first block in the chain."""
        genesis = MerkleBlock(0, "Genesis Block", "0")
        self.chain.append(genesis)
    
    def add_block(self, data: Any) -> str:
        """
        Add a new data block to the ledger.
        
        Args:
            data: Data to store in the block (can be any JSON-serializable type)
            
        Returns:
            Hash of the newly created block
        """
        previous_block = self.chain[-1]
        new_index = len(self.chain)
        new_block = MerkleBlock(new_index, data, previous_block.hash)
        self.chain.append(new_block)
        
        logging.info(f"Block {new_index} added with hash: {new_block.hash[:16]}...")
        return new_block.hash
    
    def verify_chain(self) -> bool:
        """
        Verify the integrity of the entire blockchain.
        
        Returns:
            True if chain is valid, False if any block has been tampered with
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block._compute_hash():
                logging.error(f"Block {i} hash is invalid")
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                logging.error(f"Block {i} is not properly linked to previous block")
                return False
        
        logging.info(f"Chain verified: {len(self.chain)} blocks are valid")
        return True
    
    def get_provenance(self, block_id: int) -> Optional[List[Dict]]:
        """
        Retrieve the provenance trail for a specific block.
        
        Args:
            block_id: Index of the block to trace
            
        Returns:
            List of blocks from genesis to the specified block, or None if invalid
        """
        if block_id < 0 or block_id >= len(self.chain):
            logging.warning(f"Invalid block_id: {block_id}")
            return None
        
        # Return all blocks from genesis up to and including the target block
        provenance = [block.to_dict() for block in self.chain[:block_id + 1]]
        logging.info(f"Provenance retrieved for block {block_id}: {len(provenance)} blocks")
        return provenance
    
    def get_block(self, block_id: int) -> Optional[Dict]:
        """
        Get a specific block by ID.
        
        Args:
            block_id: Index of the block
            
        Returns:
            Block data as dictionary, or None if not found
        """
        if block_id < 0 or block_id >= len(self.chain):
            return None
        return self.chain[block_id].to_dict()
    
    def get_latest_block(self) -> Dict:
        """Get the most recent block in the chain."""
        return self.chain[-1].to_dict()
    
    def chain_length(self) -> int:
        """Get the total number of blocks in the chain."""
        return len(self.chain)
