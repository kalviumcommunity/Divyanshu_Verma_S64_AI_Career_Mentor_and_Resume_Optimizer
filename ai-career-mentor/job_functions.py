"""
Job Functions Module - Function Calling Implementation

This module provides simple function calling functionality by returning
predefined job requirements for different roles. This demonstrates the
function calling concept in a straightforward way.
"""

def getJobRequirements(role):
    """
    Simple function that returns predefined job requirements for different roles.
    This implements the Function Calling concept by providing structured data
    based on the input role.
    
    Args:
        role (str): The job role to get requirements for
        
    Returns:
        dict: Dictionary containing required_skills and nice_to_have skills
    """
    
    # Basic dictionary of job requirements for common roles
    job_data = {
        "frontend developer": {
            "role": "Frontend Developer",
            "required_skills": ["JavaScript", "React", "HTML", "CSS", "Git"],
            "nice_to_have": ["TypeScript", "Node.js", "Testing", "Webpack", "SASS"]
        },
        
        "backend developer": {
            "role": "Backend Developer", 
            "required_skills": ["Python", "SQL", "REST APIs", "Git", "Linux"],
            "nice_to_have": ["Docker", "AWS", "Redis", "GraphQL", "Microservices"]
        },
        
        "data scientist": {
            "role": "Data Scientist",
            "required_skills": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas"],
            "nice_to_have": ["R", "Tableau", "AWS", "TensorFlow", "Jupyter"]
        },
        
        "product manager": {
            "role": "Product Manager",
            "required_skills": ["Product Strategy", "User Research", "Analytics", "Communication", "Agile"],
            "nice_to_have": ["SQL", "Figma", "A/B Testing", "Roadmapping", "Stakeholder Management"]
        },
        
        "marketing specialist": {
            "role": "Marketing Specialist",
            "required_skills": ["Digital Marketing", "Content Creation", "Analytics", "Social Media", "SEO"],
            "nice_to_have": ["Google Ads", "Email Marketing", "Photoshop", "CRM", "Marketing Automation"]
        },
        
        "ux designer": {
            "role": "UX Designer",
            "required_skills": ["User Research", "Wireframing", "Prototyping", "Figma", "User Testing"],
            "nice_to_have": ["Adobe Creative Suite", "HTML/CSS", "Animation", "Design Systems", "Accessibility"]
        }
    }
    
    # Return the job data for the specified role, or default to frontend developer
    return job_data.get(role.lower(), job_data["frontend developer"])


def getAllJobRoles():
    """
    Helper function to get all available job roles.
    
    Returns:
        list: List of all available job role names
    """
    return [
        "Frontend Developer",
        "Backend Developer", 
        "Data Scientist",
        "Product Manager",
        "Marketing Specialist",
        "UX Designer"
    ]