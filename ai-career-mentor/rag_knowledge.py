"""
RAG Knowledge Module - Retrieval-Augmented Generation Implementation

This module provides simple RAG functionality by storing and retrieving
career tips and resume examples for different job roles. This demonstrates
the RAG concept using basic Python dictionaries and string matching.
"""

def retrieveCareerTips(job_role):
    """
    Simple RAG implementation that retrieves relevant career tips
    for a specific job role from a predefined knowledge base.
    
    Args:
        job_role (str): The job role to get career tips for
        
    Returns:
        list: List of career tips relevant to the job role
    """
    
    # Knowledge base of career tips for different roles
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
    
    # Return career tips for the specified role, or default to frontend developer
    return career_tips_db.get(job_role.lower(), career_tips_db["frontend developer"])


def retrieveResumeExamples(job_role):
    """
    Retrieves example resume bullet points for a specific job role.
    This provides additional RAG content for resume generation.
    
    Args:
        job_role (str): The job role to get resume examples for
        
    Returns:
        list: List of example resume bullet points
    """
    
    # Knowledge base of resume examples for different roles
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
            "Led cross-functional team of 8 engineers and designers to deliver 3 major product features",
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
    
    # Return resume examples for the specified role, or default to frontend developer
    return resume_examples_db.get(job_role.lower(), resume_examples_db["frontend developer"])


def searchKnowledgeBase(query, job_role=None):
    """
    Simple search function to find relevant knowledge based on a query.
    This demonstrates basic RAG retrieval functionality.
    
    Args:
        query (str): Search query
        job_role (str, optional): Specific job role to search within
        
    Returns:
        dict: Dictionary containing relevant tips and examples
    """
    
    if job_role:
        # Search within specific job role
        tips = retrieveCareerTips(job_role)
        examples = retrieveResumeExamples(job_role)
    else:
        # Search across all roles (simplified - just return general tips)
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
        "job_role": job_role
    }