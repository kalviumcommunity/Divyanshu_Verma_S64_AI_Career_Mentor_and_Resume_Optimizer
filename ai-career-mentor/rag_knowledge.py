"""
RAG Knowledge Module - Enhanced Retrieval-Augmented Generation Implementation

This module provides enhanced RAG functionality using a vector database for semantic search.
It maintains backward compatibility with the original dictionary-based approach as a fallback.
The vector database enables more intelligent retrieval of career tips and resume examples
based on semantic similarity rather than exact keyword matching.
"""

from vector_database import vector_db
import logging

logger = logging.getLogger(__name__)

def retrieveCareerTips(job_role):
    """
    Enhanced RAG implementation that retrieves relevant career tips using vector database
    semantic search, with fallback to dictionary-based approach.
    
    Args:
        job_role (str): The job role to get career tips for
        
    Returns:
        list: List of career tips relevant to the job role
    """
    
    # Try vector database first for semantic search
    try:
        # Create a search query that includes the job role and career guidance context
        search_query = f"career tips advice guidance for {job_role} professional development resume"
        
        # Perform semantic search for career tips
        results = vector_db.semantic_search(
            query=search_query,
            job_role=job_role.lower().replace(" ", "_"),
            content_type="career_tip",
            n_results=5
        )
        
        if results:
            # Extract documents from results and log similarity scores
            tips = [result['document'] for result in results]
            logger.info(f"Retrieved {len(tips)} career tips from vector database for {job_role}")
            for i, result in enumerate(results):
                logger.debug(f"Tip {i+1} similarity: {result['similarity_score']:.3f}")
            return tips
            
    except Exception as e:
        logger.warning(f"Vector database search failed: {e}, falling back to dictionary")
    
    # Fallback to original dictionary-based approach
    career_tips_db = {
        "frontend developer": [
            "Emphasize user-facing projects and UI/UX improvements in your resume",
            "Mention specific frameworks and libraries you've used (React, Vue, Angular)",
            "Highlight responsive design and cross-browser compatibility experience",
            "Include links to your portfolio or GitHub projects",
            "Quantify performance improvements (load time reductions, user engagement)"
        ],
        
        "backend developer": [
            "Focus on system architecture and scalability achievements",
            "Highlight API design and database optimization experience", 
            "Mention specific technologies and frameworks (Django, Flask, Express)",
            "Quantify system performance improvements and uptime statistics",
            "Include experience with cloud platforms and deployment processes"
        ],
        
        "data scientist": [
            "Quantify impact with specific metrics and percentages",
            "Mention data size and complexity you've handled (millions of records, etc.)",
            "Highlight business insights and recommendations that drove decisions",
            "Include specific ML algorithms and tools used (scikit-learn, TensorFlow)",
            "Show progression from data analysis to actionable business outcomes"
        ],
        
        "product manager": [
            "Focus on product outcomes and user impact metrics",
            "Highlight cross-functional collaboration and stakeholder management",
            "Mention specific methodologies used (Agile, Scrum, Design Thinking)",
            "Quantify product success (user growth, revenue impact, feature adoption)",
            "Show strategic thinking and market analysis capabilities"
        ],
        
        "marketing specialist": [
            "Quantify campaign results with specific ROI and conversion metrics",
            "Highlight multi-channel campaign experience and audience targeting",
            "Mention specific tools and platforms used (Google Analytics, HubSpot)",
            "Show creative problem-solving and A/B testing experience",
            "Include brand building and content strategy achievements"
        ],
        
        "ux designer": [
            "Focus on user-centered design process and research methodologies",
            "Highlight usability improvements and user satisfaction metrics",
            "Mention design tools and prototyping experience (Figma, Sketch)",
            "Show collaboration with development teams and design system work",
            "Include accessibility considerations and inclusive design practices"
        ]
    }
    
    logger.info(f"Using fallback dictionary for {job_role}")
    return career_tips_db.get(job_role.lower(), career_tips_db["frontend developer"])


def retrieveResumeExamples(job_role):
    """
    Enhanced retrieval of resume examples using vector database semantic search,
    with fallback to dictionary-based approach.
    
    Args:
        job_role (str): The job role to get resume examples for
        
    Returns:
        list: List of example resume bullet points
    """
    
    # Try vector database first for semantic search
    try:
        # Create a search query for resume examples
        search_query = f"resume bullet points examples achievements for {job_role} professional experience"
        
        # Perform semantic search for resume examples
        results = vector_db.semantic_search(
            query=search_query,
            job_role=job_role.lower().replace(" ", "_"),
            content_type="resume_example",
            n_results=4
        )
        
        if results:
            # Extract documents from results
            examples = [result['document'] for result in results]
            logger.info(f"Retrieved {len(examples)} resume examples from vector database for {job_role}")
            for i, result in enumerate(results):
                logger.debug(f"Example {i+1} similarity: {result['similarity_score']:.3f}")
            return examples
            
    except Exception as e:
        logger.warning(f"Vector database search failed: {e}, falling back to dictionary")
    
    # Fallback to original dictionary-based approach
    resume_examples_db = {
        "frontend developer": [
            "Developed responsive web applications using React and JavaScript, improving user engagement by 25%",
            "Collaborated with UX designers to implement pixel-perfect designs across multiple browsers",
            "Optimized application performance through code splitting and lazy loading, reducing load times by 40%",
            "Built reusable component library used across 5+ projects, reducing development time by 30%"
        ],
        
        "backend developer": [
            "Designed and implemented RESTful APIs serving 10,000+ daily active users",
            "Optimized database queries and indexing, improving response times by 60%",
            "Built scalable microservices architecture using Docker and Kubernetes",
            "Implemented automated testing and CI/CD pipelines, reducing deployment time by 50%"
        ],
        
        "data scientist": [
            "Developed machine learning models that improved customer retention by 15%",
            "Analyzed large datasets (10M+ records) to identify key business trends and opportunities",
            "Created automated reporting dashboards that saved 20 hours of manual work per week",
            "Collaborated with product teams to implement A/B testing framework for feature optimization"
        ],
        
        "product manager": [
            "Led cross-functional team of 8 engineers and designers to deliver 3 major project features",
            "Increased user engagement by 35% through data-driven product improvements",
            "Conducted user research and market analysis to inform product roadmap decisions",
            "Managed product backlog and sprint planning, improving team velocity by 25%"
        ],
        
        "marketing specialist": [
            "Executed multi-channel marketing campaigns that generated $500K in revenue",
            "Increased social media engagement by 150% through targeted content strategy",
            "Optimized email marketing campaigns, improving open rates by 40% and CTR by 25%",
            "Managed Google Ads campaigns with $50K monthly budget, achieving 3:1 ROAS"
        ],
        
        "ux designer": [
            "Redesigned user onboarding flow, reducing drop-off rate by 30%",
            "Conducted user research with 100+ participants to inform design decisions",
            "Created design system and component library used across 10+ product teams",
            "Improved accessibility compliance from 60% to 95% through inclusive design practices"
        ]
    }
    
    logger.info(f"Using fallback dictionary for {job_role}")
    return resume_examples_db.get(job_role.lower(), resume_examples_db["frontend developer"])


def searchKnowledgeBase(query, job_role=None):
    """
    Enhanced search function using vector database for semantic similarity search.
    This provides more intelligent RAG retrieval based on query meaning rather than keywords.
    
    Args:
        query (str): Search query
        job_role (str, optional): Specific job role to search within
        
    Returns:
        dict: Dictionary containing relevant tips and examples with similarity scores
    """
    
    try:
        # Perform semantic search across all content types
        all_results = vector_db.semantic_search(
            query=query,
            job_role=job_role.lower().replace(" ", "_") if job_role else None,
            n_results=10
        )
        
        if all_results:
            # Separate tips and examples
            tips = []
            examples = []
            
            for result in all_results:
                if result['metadata']['content_type'] == 'career_tip':
                    tips.append({
                        'content': result['document'],
                        'similarity_score': result['similarity_score'],
                        'job_role': result['metadata']['job_role']
                    })
                elif result['metadata']['content_type'] == 'resume_example':
                    examples.append({
                        'content': result['document'],
                        'similarity_score': result['similarity_score'],
                        'job_role': result['metadata']['job_role']
                    })
            
            # Limit to top 5 of each type
            tips = tips[:5]
            examples = examples[:5]
            
            logger.info(f"Vector search found {len(tips)} tips and {len(examples)} examples for query: '{query}'")
            
            return {
                "career_tips": [tip['content'] for tip in tips],
                "resume_examples": [example['content'] for example in examples],
                "query": query,
                "job_role": job_role,
                "search_method": "vector_database",
                "tip_scores": [tip['similarity_score'] for tip in tips],
                "example_scores": [example['similarity_score'] for example in examples]
            }
            
    except Exception as e:
        logger.warning(f"Vector database search failed: {e}, using fallback")
    
    # Fallback to role-based retrieval
    if job_role:
        tips = retrieveCareerTips(job_role)
        examples = retrieveResumeExamples(job_role)
    else:
        # General tips for any role
        tips = [
            "Use action verbs to start each bullet point (Developed, Implemented, Optimized)",
            "Quantify achievements with specific numbers and percentages",
            "Tailor your resume to match the job description keywords",
            "Focus on results and impact rather than just responsibilities"
        ]
        examples = [
            "Increased team productivity by 25% through process improvements",
            "Led project that resulted in $100K cost savings annually",
            "Collaborated with cross-functional teams to deliver key initiatives"
        ]
    
    return {
        "career_tips": tips,
        "resume_examples": examples,
        "query": query,
        "job_role": job_role,
        "search_method": "fallback_dictionary"
    }


def addKnowledgeToDatabase(content, job_role, content_type, source="user_added"):
    """
    Add new knowledge to the vector database
    
    Args:
        content (str): The content to add
        job_role (str): Job role this content relates to
        content_type (str): 'career_tip' or 'resume_example'
        source (str): Source of the content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        success = vector_db.add_knowledge(content, job_role, content_type, source)
        if success:
            logger.info(f"Successfully added {content_type} for {job_role}")
        return success
    except Exception as e:
        logger.error(f"Failed to add knowledge: {e}")
        return False


def getVectorDatabaseStats():
    """
    Get statistics about the vector database
    
    Returns:
        dict: Database statistics
    """
    return vector_db.get_stats()