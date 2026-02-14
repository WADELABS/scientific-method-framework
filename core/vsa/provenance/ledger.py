import sqlite3
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
import logging

class MerkleLedger:
    """
    Layer 1: Distributed Ledger Orchestration.
    Provides immutable storage for experiment provenance with Merkle-tree validation.
    """
    
    def __init__(self, db_path: str = "provenance.db"):
        self.db_path = db_path
        self._init_db()
        logging.info(f"Merkle Ledger initialized at {db_path}")

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prev_hash TEXT,
                    merkle_root TEXT,
                    timestamp DATETIME,
                    data_json TEXT,
                    block_hash TEXT
                )
            """)
            conn.commit()

    def _compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()

    def add_entry(self, data: Dict[str, Any]) -> str:
        """Add a new entry to the immutable ledger as a block."""
        with sqlite3.connect(self.db_path) as conn:
            # Get latest block hash
            cursor = conn.execute("SELECT block_hash FROM blocks ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            prev_hash = row[0] if row else "0" * 64
            
            data_str = json.dumps(data, sort_keys=True)
            merkle_root = self._compute_hash(data_str) # Simple Merkle root for single-data block
            timestamp = datetime.now().isoformat()
            
            block_content = f"{prev_hash}{merkle_root}{timestamp}"
            block_hash = self._compute_hash(block_content)
            
            conn.execute("""
                INSERT INTO blocks (prev_hash, merkle_root, timestamp, data_json, block_hash)
                VALUES (?, ?, ?, ?, ?)
            """, (prev_hash, merkle_root, timestamp, data_str, block_hash))
            conn.commit()
            
            logging.info(f"Block added to ledger. Hash: {block_hash}")
            return block_hash

    def verify_chain(self) -> bool:
        """Verify the entire integrity of the ledger chain."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT prev_hash, merkle_root, timestamp, block_hash FROM blocks ORDER BY id ASC")
            blocks = cursor.fetchall()
            
            expected_prev_hash = "0" * 64
            for prev_hash, merkle_root, timestamp, block_hash in blocks:
                if prev_hash != expected_prev_hash:
                    logging.error(f"Chain broken at block {block_hash}: Expected prev_hash {expected_prev_hash}, got {prev_hash}")
                    return False
                
                block_content = f"{prev_hash}{merkle_root}{timestamp}"
                computed_hash = self._compute_hash(block_content)
                if computed_hash != block_hash:
                    logging.error(f"Integrity check failed at block {block_hash}")
                    return False
                
                expected_prev_hash = block_hash
                
            logging.info("Ledger integrity verified successfully.")
            return True
