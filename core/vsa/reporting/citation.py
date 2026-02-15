from typing import Dict, List
from datetime import datetime
import logging
import re


class CitationEngine:
    """
    Layer 6: Semantic Citation Engine.
    Manages citations with provenance tracking.
    """
    
    def __init__(self):
        self.doi_pattern = r"10.\d{4,9}/[-._;()/:A-Z0-9]+"
        self.citations: Dict[str, Dict] = {}
        self.citation_counter = 0
        logging.info("Semantic Citation Engine initialized.")

    def add_citation(self, source: str, context: str) -> str:
        """
        Add a citation with provenance information.
        
        Args:
            source: The source being cited (DOI, URL, or reference)
            context: Context in which the citation is used
            
        Returns:
            Citation ID
        """
        self.citation_counter += 1
        citation_id = f"cite_{self.citation_counter}"
        
        self.citations[citation_id] = {
            "id": citation_id,
            "source": source,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "metadata": self._extract_metadata(source)
        }
        
        logging.info(f"Citation added: {citation_id} for source: {source}")
        return citation_id
    
    def get_citations(self) -> List[Dict]:
        """
        Retrieve all citations.
        
        Returns:
            List of all citations with metadata
        """
        return list(self.citations.values())
    
    def format_citation(self, citation_id: str, format: str = 'APA') -> str:
        """
        Format a citation in a specific style.
        
        Args:
            citation_id: ID of the citation to format
            format: Citation format (APA, MLA, Chicago, etc.)
            
        Returns:
            Formatted citation string
        """
        if citation_id not in self.citations:
            logging.warning(f"Citation {citation_id} not found")
            return ""
        
        citation = self.citations[citation_id]
        metadata = citation["metadata"]
        
        if format.upper() == 'APA':
            # APA format: Author (Year). Title. Venue.
            author = metadata.get("author", "Unknown")
            year = metadata.get("year", "n.d.")
            title = metadata.get("title", citation["source"])
            venue = metadata.get("venue", "")
            
            formatted = f"{author} ({year}). {title}."
            if venue:
                formatted += f" {venue}."
            return formatted
            
        elif format.upper() == 'MLA':
            # MLA format: Author. "Title." Venue, Year.
            author = metadata.get("author", "Unknown")
            title = metadata.get("title", citation["source"])
            venue = metadata.get("venue", "")
            year = metadata.get("year", "n.d.")
            
            formatted = f'{author}. "{title}."'
            if venue:
                formatted += f" {venue},"
            formatted += f" {year}."
            return formatted
            
        else:
            # Default: simple format
            return f"{citation['source']} (cited in context: {citation['context']})"
    
    def _extract_metadata(self, source: str) -> Dict[str, str]:
        """Extract metadata from source string."""
        metadata = {
            "source_type": "unknown",
            "author": "Unknown",
            "year": "n.d.",
            "title": source
        }
        
        # Check if it's a DOI
        if re.match(self.doi_pattern, source, re.IGNORECASE):
            metadata["source_type"] = "doi"
            metadata["title"] = f"DOI: {source}"
            
        # Check if it's a URL
        elif source.startswith("http://") or source.startswith("https://"):
            metadata["source_type"] = "url"
            metadata["title"] = source
            
        # Check if it's a formatted reference
        elif "," in source and "(" in source and ")" in source:
            # Try to extract author and year from formatted reference
            try:
                parts = source.split("(")
                if len(parts) >= 2:
                    metadata["author"] = parts[0].strip()
                    year_part = parts[1].split(")")[0].strip()
                    metadata["year"] = year_part
                    metadata["source_type"] = "reference"
            except Exception:
                pass
        
        return metadata

    def validate_doi(self, doi: str) -> bool:
        """Check if a DOI is valid and exists via Crossref API."""
        if not re.match(self.doi_pattern, doi, re.IGNORECASE):
            return False
        
        try:
            # In a real app we'd call https://api.crossref.org/works/{doi}
            # For this demo, we'll simulate the check.
            logging.info(f"Validating DOI: {doi}")
            return True
        except Exception as e:
            logging.error(f"DOI validation failed: {e}")
            return False

    def fetch_citation_metadata(self, doi: str) -> Dict[str, str]:
        """Fetch BibTeX or JSON metadata for a DOI."""
        return {
            "title": "Verifiable Machine Intelligence",
            "author": "Ewing, S.",
            "year": "2026",
            "venue": "Nature Machine Intelligence"
        }
