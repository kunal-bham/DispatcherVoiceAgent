import os
import json
from typing import List, Dict, Optional
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DispatcherRAG:
    """Retrieval Augmented Generation system for emergency dispatcher information"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.embeddings_cache = {}
        self.emergency_protocols = self._load_emergency_protocols()
        self.location_data = self._load_location_data()
        self.medical_guidelines = self._load_medical_guidelines()
        
    def _load_emergency_protocols(self) -> Dict:
        """Load emergency response protocols from JSON"""
        try:
            protocol_path = self.knowledge_base_path / "emergency_protocols.json"
            if protocol_path.exists():
                with open(protocol_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading emergency protocols: {e}")
            return {}
            
    def _load_location_data(self) -> Dict:
        """Load location-specific emergency data"""
        try:
            location_path = self.knowledge_base_path / "location_data.json"
            if location_path.exists():
                with open(location_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading location data: {e}")
            return {}
            
    def _load_medical_guidelines(self) -> Dict:
        """Load medical emergency guidelines"""
        try:
            medical_path = self.knowledge_base_path / "medical_guidelines.json"
            if medical_path.exists():
                with open(medical_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading medical guidelines: {e}")
            return {}
            
    def get_relevant_protocols(self, emergency_type: str) -> List[Dict]:
        """Retrieve relevant emergency protocols based on emergency type"""
        try:
            return self.emergency_protocols.get(emergency_type, [])
        except Exception as e:
            logger.error(f"Error retrieving protocols: {e}")
            return []
            
    def get_location_specific_info(self, location: str) -> Dict:
        """Get location-specific emergency information"""
        try:
            return self.location_data.get(location, {})
        except Exception as e:
            logger.error(f"Error retrieving location info: {e}")
            return {}
            
    def get_medical_guidelines(self, condition: str) -> Dict:
        """Retrieve medical guidelines for specific conditions"""
        try:
            return self.medical_guidelines.get(condition, {})
        except Exception as e:
            logger.error(f"Error retrieving medical guidelines: {e}")
            return {}
            
    def update_knowledge_base(self, new_data: Dict, data_type: str) -> bool:
        """Update the knowledge base with new information"""
        try:
            if data_type == "protocols":
                self.emergency_protocols.update(new_data)
                self._save_to_file("emergency_protocols.json", self.emergency_protocols)
            elif data_type == "locations":
                self.location_data.update(new_data)
                self._save_to_file("location_data.json", self.location_data)
            elif data_type == "medical":
                self.medical_guidelines.update(new_data)
                self._save_to_file("medical_guidelines.json", self.medical_guidelines)
            return True
        except Exception as e:
            logger.error(f"Error updating knowledge base: {e}")
            return False
            
    def _save_to_file(self, filename: str, data: Dict) -> None:
        """Save data to JSON file"""
        try:
            file_path = self.knowledge_base_path / filename
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            
    def get_emergency_response_plan(self, 
                                  emergency_type: str, 
                                  location: str, 
                                  condition: Optional[str] = None) -> Dict:
        """Generate comprehensive emergency response plan"""
        try:
            response_plan = {
                "timestamp": datetime.now().isoformat(),
                "emergency_type": emergency_type,
                "location": location,
                "protocols": self.get_relevant_protocols(emergency_type),
                "location_info": self.get_location_specific_info(location),
                "medical_guidelines": self.get_medical_guidelines(condition) if condition else {},
                "recommended_actions": self._generate_recommended_actions(
                    emergency_type, location, condition
                )
            }
            return response_plan
        except Exception as e:
            logger.error(f"Error generating response plan: {e}")
            return {}
            
    def _generate_recommended_actions(self, 
                                    emergency_type: str, 
                                    location: str, 
                                    condition: Optional[str]) -> List[str]:
        """Generate recommended actions based on emergency type and location"""
        try:
            actions = []
            protocols = self.get_relevant_protocols(emergency_type)
            location_info = self.get_location_specific_info(location)
            
            # Add protocol-based actions
            for protocol in protocols:
                actions.extend(protocol.get("recommended_actions", []))
                
            # Add location-specific actions
            actions.extend(location_info.get("recommended_actions", []))
            
            # Add medical-specific actions if condition is provided
            if condition:
                medical_guidelines = self.get_medical_guidelines(condition)
                actions.extend(medical_guidelines.get("recommended_actions", []))
                
            return list(set(actions))  # Remove duplicates
        except Exception as e:
            logger.error(f"Error generating recommended actions: {e}")
            return []

# Example usage (commented out to prevent actual execution)
"""
if __name__ == "__main__":
    # Initialize the RAG system
    dispatcher_rag = DispatcherRAG()
    
    # Example emergency scenario
    emergency_type = "medical"
    location = "downtown"
    condition = "cardiac_arrest"
    
    # Get comprehensive response plan
    response_plan = dispatcher_rag.get_emergency_response_plan(
        emergency_type, location, condition
    )
    
    # Print response plan
    print(json.dumps(response_plan, indent=2))
""" 