"""
System Prompt Management for AI Career Mentor

This module contains the system prompt that defines how the AI behaves
as a career mentor and resume writer.
"""

# System Prompt - Defines the AI's role and behavior
SYSTEM_PROMPT = """You are an expert career mentor and resume writer specializing in helping job seekers optimize their resumes for specific roles. 

Your expertise includes:
- Creating compelling, action-oriented resume bullet points that highlight achievements
- Identifying skill gaps between current abilities and job requirements  
- Tailoring advice to different industries and experience levels
- Providing practical, actionable career guidance

Your responses should be:
- Professional and encouraging
- Specific and actionable
- Based on real industry knowledge
- Formatted exactly as requested

Always respond in the exact JSON format requested with professional, actionable content that helps users improve their job prospects."""


def create_user_prompt(user_data, job_requirements, career_tips):
    """
    Creates a user prompt that formats user information for the AI career mentor.
    
    Args:
        user_data (dict): User information containing name, skills, target_role, tone
        job_requirements (dict): Job requirements from getJobRequirements function
        career_tips (list): Career tips from RAG knowledge base
    
    Returns:
        str: Formatted user prompt for the AI
    
    Example:
        user_data = {
            "name": "John Smith",
            "skills": ["Python", "SQL", "Excel"],
            "target_role": "Data Scientist",
            "tone": "professional"
        }
        
        job_requirements = {
            "required_skills": ["Python", "SQL", "Machine Learning", "Statistics"],
            "nice_to_have": ["R", "Tableau", "AWS"]
        }
        
        career_tips = [
            "Quantify impact with specific metrics and percentages",
            "Mention data size and complexity handled"
        ]
        
        prompt = create_user_prompt(user_data, job_requirements, career_tips)
    """
    
    # Format the user prompt with clear sections
    user_prompt = f"""Create a personalized resume optimization for the following candidate:

CANDIDATE INFORMATION:
- Name: {user_data.get('name', 'N/A')}
- Current Skills: {', '.join(user_data.get('skills', []))}
- Target Role: {user_data.get('target_role', 'N/A')}
- Tone Preference: {user_data.get('tone', 'professional')}

JOB REQUIREMENTS:
- Required Skills: {', '.join(job_requirements.get('required_skills', []))}
- Nice to Have: {', '.join(job_requirements.get('nice_to_have', []))}

INDUSTRY GUIDANCE:
{\n.join(f'- {tip}' for tip in career_tips)}

TASK:
Generate 3-5 tailored resume bullet points that showcase the candidate's experience in a way that aligns with the target role. Also identify 2-3 specific skill gaps they should focus on developing.

Respond in JSON format:
{{
    "resumeBullets": [
        "Action-oriented bullet point 1",
        "Achievement-focused bullet point 2", 
        "Skills-demonstrating bullet point 3"
    ],
    "skillGaps": [
        "Specific skill or technology gap 1",
        "Knowledge area gap 2",
        "Tool or certification gap 3"
    ]
}}"""

    return user_prompt


