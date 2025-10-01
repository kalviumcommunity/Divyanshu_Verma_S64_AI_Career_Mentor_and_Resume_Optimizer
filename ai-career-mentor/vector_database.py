"""
Vector Database Module - Enhanced RAG with Semantic Search

This module implements a vector database using scikit-learn for semantic similarity search
of career knowledge. It enhances the existing RAG functionality by enabling:
- Semantic search instead of exact keyword matching
- Dynamic knowledge addition without code changes
- Better relevance scoring for career tips and resume examples
"""

import numpy as np
import pickle
import os
import json
from typing import List, Dict, Optional, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDatabase:
    """
    Vector database implementation using scikit-learn for career knowledge storage and retrieval
    """
    
    def __init__(self, persist_directory: str = "./vector_db"):
        """
        Initialize the vector database
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        self.embeddings = None
        self.documents = []
        self.metadata = []
        self.embeddings_model = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize sentence transformer model and load existing database"""
        try:
            # Create persist directory if it doesn't exist
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Initialize sentence transformer model
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Try to load existing database
            embeddings_path = os.path.join(self.persist_directory, "embeddings.npy")
            metadata_path = os.path.join(self.persist_directory, "metadata.pkl")
            documents_path = os.path.join(self.persist_directory, "documents.pkl")
            
            if os.path.exists(embeddings_path) and os.path.exists(metadata_path):
                # Load existing database
                self.embeddings = np.load(embeddings_path)
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                with open(documents_path, 'rb') as f:
                    self.documents = pickle.load(f)
                logger.info(f"Loaded existing vector database with {len(self.documents)} documents")
            else:
                # Create new database
                self.embeddings = np.array([]).reshape(0, 384)  # Empty array with correct shape
                self.documents = []
                self.metadata = []
                self._populate_initial_knowledge()
                logger.info(f"Created new vector database with {len(self.documents)} documents")
                
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {e}")
            self.embeddings = None
            self.embeddings_model = None
    
    def _populate_initial_knowledge(self):
        """Populate the database with initial career knowledge"""
        logger.info("Populating vector database with initial knowledge...")
        
        # Career tips knowledge base
        career_tips = {
            "frontend_developer": [
                "Emphasize user-facing projects and UI/UX improvements in your resume",
                "Mention specific frameworks and libraries you've used (React, Vue, Angular)",
                "Highlight responsive design and cross-browser compatibility experience",
                "Include links to your portfolio or GitHub projects",
                "Quantify performance improvements (load time reductions, user engagement)"
            ],
            "backend_developer": [
                "Focus on system architecture and scalability achievements",
                "Highlight API design and database optimization experience", 
                "Mention specific technologies and frameworks (Django, Flask, Express)",
                "Quantify system performance improvements and uptime statistics",
                "Include experience with cloud platforms and deployment processes"
            ],
            "data_scientist": [
                "Quantify impact with specific metrics and percentages",
                "Mention data size and complexity you've handled (millions of records, etc.)",
                "Highlight business insights and recommendations that drove decisions",
                "Include specific ML algorithms and tools used (scikit-learn, TensorFlow)",
                "Show progression from data analysis to actionable business outcomes"
            ],
            "product_manager": [
                "Focus on product outcomes and user impact metrics",
                "Highlight cross-functional collaboration and stakeholder management",
                "Mention specific methodologies used (Agile, Scrum, Design Thinking)",
                "Quantify product success (user growth, revenue impact, feature adoption)",
                "Show strategic thinking and market analysis capabilities"
            ],
            "marketing_specialist": [
                "Quantify campaign results with specific ROI and conversion metrics",
                "Highlight multi-channel campaign experience and audience targeting",
                "Mention specific tools and platforms used (Google Analytics, HubSpot)",
                "Show creative problem-solving and A/B testing experience",
                "Include brand building and content strategy achievements"
            ],
            "ux_designer": [
                "Focus on user-centered design process and research methodologies",
                "Highlight usability improvements and user satisfaction metrics",
                "Mention design tools and prototyping experience (Figma, Sketch)",
                "Show collaboration with development teams and design system work",
                "Include accessibility considerations and inclusive design practices"
            ]
        }
        
        # Resume examples knowledge base
        resume_examples = {
            "frontend_developer": [
                "Developed responsive web applications using React and JavaScript, improving user engagement by 25%",
                "Collaborated with UX designers to implement pixel-perfect designs across multiple browsers",
                "Optimized application performance through code splitting and lazy loading, reducing load times by 40%",
                "Built reusable component library used across 5+ projects, reducing development time by 30%"
            ],
            "backend_developer": [
                "Designed and implemented RESTful APIs serving 10,000+ daily active users",
                "Optimized database queries and indexing, improving response times by 60%",
                "Built scalable microservices architecture using Docker and Kubernetes",
                "Implemented automated testing and CI/CD pipelines, reducing deployment time by 50%"
            ],
            "data_scientist": [
                "Developed machine learning models that improved customer retention by 15%",
                "Analyzed large datasets (10M+ records) to identify key business trends and opportunities",
                "Created automated reporting dashboards that saved 20 hours of manual work per week",
                "Collaborated with product teams to implement A/B testing framework for feature optimization"
            ],
            "product_manager": [
                "Led cross-functional team of 8 engineers and designers to deliver 3 major product features",
                "Increased user engagement by 35% through data-driven product improvements",
                "Conducted user research and market analysis to inform product roadmap decisions",
                "Managed product backlog and sprint planning, improving team velocity by 25%"
            ],
            "marketing_specialist": [
                "Executed multi-channel marketing campaigns that generated $500K in revenue",
                "Increased social media engagement by 150% through targeted content strategy",
                "Optimized email marketing campaigns, improving open rates by 40% and CTR by 25%",
                "Managed Google Ads campaigns with $50K monthly budget, achieving 3:1 ROAS"
            ],
            "ux_designer": [
                "Redesigned user onboarding flow, reducing drop-off rate by 30%",
                "Conducted user research with 100+ participants to inform design decisions",
                "Created design system and component library used across 10+ product teams",
                "Improved accessibility compliance from 60% to 95% through inclusive design practices"
            ]
        }
        
        # Add career tips to vector database
        documents = []
        metadatas = []
        ids = []
        
        doc_id = 0
        
        for job_role, tips in career_tips.items():
            for tip in tips:
                documents.append(tip)
                metadatas.append({
                    "job_role": job_role,
                    "content_type": "career_tip",
                    "source": "initial_knowledge"
                })
                ids.append(f"tip_{doc_id}")
                doc_id += 1
        
        # Add resume examples to vector database
        for job_role, examples in resume_examples.items():
            for example in examples:
                documents.append(example)
                metadatas.append({
                    "job_role": job_role,
                    "content_type": "resume_example",
                    "source": "initial_knowledge"
                })
                ids.append(f"example_{doc_id}")
                doc_id += 1
        
        # Generate embeddings and add to database
        if documents:
            new_embeddings = self.embeddings_model.encode(documents)
            
            # Add to embeddings array
            if self.embeddings.size == 0:
                self.embeddings = new_embeddings
            else:
                self.embeddings = np.vstack([self.embeddings, new_embeddings])
            
            # Store documents and metadata
            self.documents.extend(documents)
            self.metadata.extend(metadatas)
            
            # Save to disk
            self._save_database()
            
            logger.info(f"Added {len(documents)} documents to vector database")
    
    def semantic_search(self, query: str, job_role: Optional[str] = None, 
                       content_type: Optional[str] = None, n_results: int = 5) -> List[Dict]:
        """
        Perform semantic similarity search
        
        Args:
            query: Search query text
            job_role: Filter by specific job role (optional)
            content_type: Filter by content type ('career_tip' or 'resume_example')
            n_results: Number of results to return
            
        Returns:
            List of dictionaries containing documents, metadata, and similarity scores
        """
        if self.embeddings is None or self.embeddings_model is None or len(self.documents) == 0:
            logger.warning("Vector database not available, returning empty results")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embeddings_model.encode([query])
            
            # Calculate cosine similarity with all embeddings
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Get indices sorted by similarity (descending)
            sorted_indices = np.argsort(similarities)[::-1]
            
            # Filter results based on criteria and format
            formatted_results = []
            for idx in sorted_indices:
                metadata = self.metadata[idx]
                
                # Apply filters
                if job_role and metadata.get('job_role') != job_role:
                    continue
                if content_type and metadata.get('content_type') != content_type:
                    continue
                
                formatted_results.append({
                    'document': self.documents[idx],
                    'metadata': metadata,
                    'similarity_score': float(similarities[idx]),
                    'id': f"doc_{idx}"
                })
                
                if len(formatted_results) >= n_results:
                    break
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error performing semantic search: {e}")
            return []
    
    def add_knowledge(self, content: str, job_role: str, content_type: str, 
                     source: str = "user_added") -> bool:
        """
        Add new knowledge to the vector database
        
        Args:
            content: The text content to add
            job_role: Job role this content relates to
            content_type: Type of content ('career_tip' or 'resume_example')
            source: Source of the content
            
        Returns:
            True if successful, False otherwise
        """
        if self.embeddings is None or not self.embeddings_model:
            logger.warning("Vector database not available")
            return False
        
        try:
            # Check for duplicates
            existing = self.semantic_search(content, job_role, content_type, n_results=1)
            if existing and existing[0]['similarity_score'] > 0.95:
                logger.info("Similar content already exists, skipping duplicate")
                return False
            
            # Generate embedding
            new_embedding = self.embeddings_model.encode([content])
            
            # Add to embeddings array
            if self.embeddings.size == 0:
                self.embeddings = new_embedding
            else:
                self.embeddings = np.vstack([self.embeddings, new_embedding])
            
            # Add to documents and metadata
            self.documents.append(content)
            self.metadata.append({
                "job_role": job_role,
                "content_type": content_type,
                "source": source
            })
            
            # Save to disk
            self._save_database()
            
            logger.info(f"Added new knowledge: {content_type}_{len(self.documents)-1}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            return False
    
    def _save_database(self):
        """Save the database to disk"""
        try:
            embeddings_path = os.path.join(self.persist_directory, "embeddings.npy")
            metadata_path = os.path.join(self.persist_directory, "metadata.pkl")
            documents_path = os.path.join(self.persist_directory, "documents.pkl")
            
            np.save(embeddings_path, self.embeddings)
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            with open(documents_path, 'wb') as f:
                pickle.dump(self.documents, f)
                
        except Exception as e:
            logger.error(f"Error saving database: {e}")
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        if self.embeddings is None:
            return {"status": "unavailable", "count": 0}
        
        try:
            return {
                "status": "available",
                "count": len(self.documents),
                "persist_directory": self.persist_directory,
                "embedding_dimension": self.embeddings.shape[1] if self.embeddings.size > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "error": str(e)}

# Global instance
vector_db = VectorDatabase()