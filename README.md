# AI Career Mentor & Resume Optimizer

## Project Overview

The AI Career Mentor is an intelligent resume optimization tool designed to help job seekers create compelling resumes tailored to specific roles. The system takes a user's basic information (name, current skills, target job role) and leverages AI to generate personalized resume bullet points while identifying skill gaps that need attention.

**The Problem**: Many job seekers struggle to write effective resume content that matches what employers are looking for. They often don't know how to phrase their experience or what skills they're missing for their target roles.

**The Solution**: Our AI-powered system analyzes the user's background against job requirements and industry best practices to generate:
- 3-5 professionally written, action-oriented resume bullet points
- 2-3 specific skill gaps with learning recommendations
- Tone customization (professional vs. creative writing styles)

**Target Users**: Students, recent graduates, and career changers who need help optimizing their resumes for specific job roles.

## How It Works

1. **User Input**: Collect name, current skills, target job role, and preferred tone
2. **Job Analysis**: Retrieve specific job requirements using function calling
3. **Knowledge Retrieval**: Get industry-specific resume writing tips using RAG
4. **AI Generation**: Send structured prompts to Gemini API with tuned parameters
5. **Structured Output**: Return formatted JSON with resume bullets and skill gaps

## Core AI Concepts Implementation

### 1. **Prompting (System & User Prompts)**

**What it is**: Prompting involves crafting specific instructions that guide the AI's behavior and responses. We use two types of prompts:

**System Prompt Implementation**:
- **Purpose**: Establishes the AI's role, expertise, and response format
- **Our Implementation**: Defines the AI as an expert career mentor and resume writer
- **Example**:
```python
SYSTEM_PROMPT = """You are an expert career mentor and resume writer specializing in helping job seekers optimize their resumes for specific roles. Your expertise includes:
- Creating compelling, action-oriented resume bullet points
- Identifying skill gaps between current abilities and job requirements  
- Tailoring advice to different industries and experience levels
Always respond in the exact JSON format requested with professional, actionable content."""
```

**User Prompt Implementation**:
- **Purpose**: Formats the user's specific request with all relevant context
- **Our Implementation**: Combines user data, job requirements, and career tips into a clear request
- **Example**:
```python
def create_user_prompt(user_data, job_requirements, career_tips, tone):
    return f"""
    Create a personalized resume optimization for:
    
    Candidate: {user_data['name']}
    Current Skills: {', '.join(user_data['skills'])}
    Target Role: {user_data['target_role']}
    Tone Preference: {tone}
    
    Job Requirements: {', '.join(job_requirements['required_skills'])}
    Industry Tips: {career_tips}
    
    Generate 3-5 tailored resume bullet points and identify 2-3 skill gaps.
    """
```

**Why This Matters**: Good prompts ensure consistent, relevant responses. The system prompt sets expectations, while the user prompt provides specific context for personalized results.

### 2. **Structured Output**

**What it is**: Structured output ensures the AI returns data in a consistent, parseable format (like JSON) rather than free-form text.

**Our Implementation**:
- **Method**: Prompt-based JSON schema enforcement with validation
- **Schema Definition**: We specify exact JSON format in the prompt
- **Validation**: Parse and validate the JSON response, retry if malformed
- **Error Handling**: Graceful fallback if JSON parsing fails

**Example Implementation**:
```python
JSON_SCHEMA = """
Respond ONLY with valid JSON in this exact format:
{
    "resumeBullets": [
        "Action-oriented bullet point 1",
        "Quantified achievement bullet point 2", 
        "Skills-focused bullet point 3"
    ],
    "skillGaps": [
        "Specific skill gap 1",
        "Technology/tool gap 2",
        "Certification/knowledge gap 3"
    ]
}
"""

def validate_json_response(response):
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "suggestion": "Please try again"}
```

**Why This Matters**: Structured output allows our application to programmatically process AI responses, display them consistently, and integrate with other systems.

### 3. **Function Calling**

**What it is**: Function calling allows the AI system to execute specific functions to retrieve or process data, extending its capabilities beyond just text generation.

**Our Implementation**:
- **Function**: `getJobRequirements(role)` - retrieves job-specific requirements
- **Data Source**: Local Python dictionary with predefined job roles and skills
- **Purpose**: Provides the AI with specific, accurate job market data

**Example Implementation**:
```python
def getJobRequirements(role):
    """
    Retrieves specific job requirements for different roles
    This simulates calling a job market API or database
    """
    job_data = {
        "frontend developer": {
            "role": "Frontend Developer",
            "required_skills": ["JavaScript", "React", "HTML", "CSS"],
            "nice_to_have": ["TypeScript", "Node.js", "Testing"]
        },
        "data scientist": {
            "role": "Data Scientist", 
            "required_skills": ["Python", "SQL", "Statistics", "Machine Learning"],
            "nice_to_have": ["R", "Tableau", "AWS"]
        },
        # ... more roles
    }
    return job_data.get(role.lower(), job_data["frontend developer"])
```

**Integration Flow**:
1. User specifies target job role
2. System calls `getJobRequirements(role)` 
3. Retrieved requirements are included in the user prompt
4. AI generates resume content based on actual job market needs

**Why This Matters**: Function calling ensures our AI has access to current, accurate job market data rather than relying solely on training data, making recommendations more relevant and actionable.

### 4. **RAG (Retrieval-Augmented Generation)**

**What it is**: RAG combines information retrieval with text generation. Instead of relying only on the AI's training data, we retrieve relevant information from a knowledge base and include it in the generation process.

**Our Implementation**:
- **Knowledge Base**: Curated collection of career tips and resume examples for different job roles
- **Retrieval Function**: `retrieveCareerTips(job_role)` - gets role-specific advice
- **Integration**: Retrieved tips are included in the user prompt to guide AI generation

**Example Implementation**:
```python
def retrieveCareerTips(job_role):
    """
    Retrieves role-specific career advice from our knowledge base
    This demonstrates RAG by combining stored knowledge with AI generation
    """
    knowledge_base = {
        "frontend developer": [
            "Emphasize user-facing projects and UI/UX improvements",
            "Mention specific frameworks and libraries used",
            "Highlight responsive design and cross-browser compatibility",
            "Show examples of interactive features you've built"
        ],
        "data scientist": [
            "Quantify impact with specific metrics and percentages", 
            "Mention data size and complexity handled",
            "Highlight business insights and recommendations made",
            "Include statistical methods and machine learning models used"
        ],
        # ... more roles
    }
    
    tips = knowledge_base.get(job_role.lower(), knowledge_base["frontend developer"])
    return " ".join(tips)
```

**RAG Process Flow**:
1. User specifies target job role
2. System retrieves relevant career tips using `retrieveCareerTips()`
3. Retrieved knowledge is included in the user prompt
4. AI generates resume content informed by both its training and our specific knowledge base

**Why This Matters**: RAG ensures our AI provides advice based on current industry best practices and specific domain knowledge, rather than just general resume writing principles. This makes the output more targeted and valuable.

## Setup Instructions

### 1. Install Dependencies
```bash
cd ai-career-mentor
pip install -r requirements.txt
```

### 2. Set Up API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run the Application
```bash
python main.py
```

## Example Usage

```
=== AI Career Mentor & Resume Optimizer ===

Enter your name: John Smith
Enter your current skills (comma-separated): Python, SQL, Excel
Enter target job role: Data Scientist
Choose tone (professional/creative): professional

Processing your request...

==================================================
RESULTS
==================================================

📝 RESUME BULLET POINTS:
------------------------------
1. Analyzed large datasets using Python and SQL to drive business decisions
2. Developed data models and statistical analyses to identify key trends  
3. Created automated reports using Excel and Python for stakeholder presentations

🎯 SKILL GAPS TO WORK ON:
------------------------------
1. Machine Learning frameworks (scikit-learn, TensorFlow)
2. Data visualization tools (Tableau, Power BI)
3. Cloud platforms (AWS, Azure)

==================================================
```

## File Structure

```
ai-career-mentor/
├── README.md               # Project documentation
├── main.py                 # Main CLI application
├── prompts.py              # System & User prompt implementations
├── gemini_client.py        # Gemini API & Structured output & Tunable parameters
├── job_functions.py        # Function calling implementation
├── rag_knowledge.py        # RAG knowledge base
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your actual API key (don't commit!)
└── .gitignore             # Git ignore file
```

## Next Steps

1. Get a Gemini API key from Google AI Studio
2. Implement the remaining course concept branches
3. Test with different job roles and skill combinations
4. Add more job roles and career tips to the knowledge base