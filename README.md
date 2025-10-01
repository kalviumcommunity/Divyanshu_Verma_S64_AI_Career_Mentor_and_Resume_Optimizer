# AI Career Mentor & Resume Optimizer

## Project Overview

The AI Career Mentor is an intelligent resume optimization tool designed to help job seekers create compelling resumes tailored to specific roles. The system takes a user's basic information (name, current skills, target job role) and leverages AI to generate personalized resume bullet points while identifying skill gaps that need attention.

**The Problem**: Many job seekers struggle to write effective resume content that matches what employers are looking for. They often don't know how to phrase their experience or what skills they're missing for their target roles.

**The Solution**: Our AI-powered system analyzes the user's background against job requirements and industry best practices to generate:
- 3-5 professionally written, action-oriented resume bullet points
- 2-3 specific skill gaps with learning recommendations
- Tone customization (professional vs. creative writing styles)
- Advanced AI parameters (Top K, Top P) for vocabulary and creativity control

**Target Users**: Students, recent graduates, and career changers who need help optimizing their resumes for specific job roles.

## ✨ Enhanced Features

### 🚀 Vector Database Integration
- **Semantic Search**: Finds relevant content based on meaning, not just keywords
- **Enhanced RAG**: Retrieval-Augmented Generation with similarity scoring
- **Dynamic Knowledge**: Add new career tips and resume examples without code changes
- **Cross-Role Discovery**: Discover relevant advice from related job roles
- **Persistent Storage**: Knowledge base persists across application restarts

### 🎛️ Advanced AI Parameters
- **Top K Control**: Vocabulary diversity (20-80 range for different creativity levels)
- **Top P Control**: Nucleus sampling (0.3-0.9 range for conservative to creative responses)
- **Temperature Settings**: Professional (0.3) vs Creative (0.8) tone control
- **Token Usage Tracking**: Monitor API costs and usage patterns

### 📊 Enhanced User Experience
- **Step-by-Step Processing**: Real-time progress updates during resume generation
- **Vector Database Status**: Live reporting of enhanced RAG system status
- **Detailed Results Display**: Comprehensive analysis with similarity scores
- **Interactive Parameter Selection**: User-friendly prompts for AI configuration

## How It Works

1. **User Input**: Collect name, current skills, target job role, tone preference, and AI parameters (Top K, Top P)
2. **Job Analysis**: Retrieve specific job requirements using function calling
3. **Enhanced Knowledge Retrieval**: Get industry-specific resume writing tips using vector database semantic search
4. **AI Generation**: Send structured prompts to Gemini API with advanced parameters (temperature, top_k, top_p)
5. **Structured Output**: Return formatted JSON with resume bullets and skill gaps
6. **Results Display**: Show comprehensive results with vector database status and token usage

## Advanced AI Parameters Guide

### 🎛️ Top K (Vocabulary Diversity)
Controls vocabulary selection by limiting to top K most likely tokens:
- **20 (Focused)**: Predictable, common vocabulary - "Developed standard web applications"
- **40 (Balanced)**: Default Gemini setting - "Developed responsive web applications"
- **80 (Diverse)**: Creative, varied vocabulary - "Architected sophisticated applications"

### 🎯 Top P (Nucleus Sampling)
Controls cumulative probability threshold for token selection:
- **0.3 (Conservative)**: Focused, predictable responses - "Standard industry practices"
- **0.7 (Balanced)**: Good balance of focus and creativity - "Effective professional approaches"
- **0.9 (Creative)**: Diverse, creative responses - "Innovative strategic methodologies"

### 🎨 Tone Settings
- **Professional (Temperature: 0.3)**: Formal, consistent, business-appropriate language
- **Creative (Temperature: 0.8)**: Varied, innovative, engaging language

### 💰 Token Usage Tracking
The system automatically logs and displays:
- Input token count (estimated vs actual)
- Output token count
- Total API usage for cost monitoring
- Gemini API pricing awareness

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
├── README.md                    # Project documentation
├── main.py                      # Main CLI application with enhanced UI
├── prompts.py                   # System & User prompt implementations
├── gemini_client.py             # Gemini API client with advanced parameters
├── job_functions.py             # Function calling implementation
├── rag_knowledge.py             # Enhanced RAG with vector database
├── vector_database.py           # Vector database for semantic search
├── demo_vector_db.py           # Vector database demonstration script
├── requirements.txt             # Python dependencies (updated)
├── TOP_K_EXAMPLES.md           # Top K parameter documentation
├── TOP_P_EXAMPLES.md           # Top P parameter documentation
├── VECTOR_DATABASE_README.md   # Vector database detailed documentation
├── .env.example                # Environment variables template
├── .env                        # Your actual API key (don't commit!)
├── .gitignore                  # Git ignore file (updated)
├── vector_db/                  # Vector database storage directory
└── __pycache__/               # Python bytecode cache
```

## Updated Dependencies

The project now includes additional dependencies for enhanced functionality:

```txt
google-generativeai==0.3.2      # Google's Gemini AI API
python-dotenv==1.0.0           # Environment variable management
sentence-transformers>=2.3.0    # Text embedding generation (NEW)
scikit-learn>=1.0.0            # Vector similarity calculations (NEW)
```

## Demo and Testing

### Vector Database Demo
Test the enhanced RAG capabilities with semantic search:

```bash
python demo_vector_db.py
```

**Demo Features**:
- Basic vector database functionality
- Semantic search capabilities
- Cross-role knowledge discovery
- Dynamic knowledge addition
- Similarity scoring demonstration

### Advanced Parameter Testing
Experiment with different AI parameters:

```bash
python main.py
```

**Interactive Options**:
- Choose vocabulary diversity (Top K: 20, 40, 80)
- Select creativity level (Top P: 0.3, 0.7, 0.9)
- Toggle tone (Professional vs Creative)
- View token usage and costs

## Enhanced RAG with Vector Database

### 🔍 Semantic Search Benefits
The vector database integration provides significant improvements over traditional keyword-based search:

**Before (Keyword Matching)**:
- Search for "leadership" → Only finds exact word "leadership"
- Limited to surface-level text matching
- Misses related concepts and synonyms

**After (Semantic Search)**:
- Search for "leadership" → Finds "team management", "project coordination", "mentoring"
- Understands context and meaning
- Discovers related concepts across different job roles

### 🚀 Key Improvements
1. **Better Relevance**: Similarity scoring ensures most relevant results appear first
2. **Cross-Role Learning**: Discover applicable knowledge from related job roles
3. **Dynamic Growth**: Add new knowledge without code changes
4. **Persistent Memory**: Knowledge base survives application restarts
5. **Fallback Safety**: Automatic fallback to dictionary-based approach if vector DB fails

### 📈 Performance Benefits
- **Quality**: More relevant and diverse career advice
- **Speed**: Efficient similarity search across large knowledge bases
- **Scalability**: Grows with your knowledge base size
- **Reliability**: Robust error handling and graceful degradation

## Next Steps & Recommendations

### 🚀 Immediate Actions
1. **Get Gemini API Key**: Obtain from [Google AI Studio](https://aistudio.google.com/)
2. **Test Enhanced Features**: Run `python demo_vector_db.py` to see semantic search in action
3. **Experiment with Parameters**: Try different Top K and Top P combinations in `main.py`

### 🔧 Development Opportunities
1. **Expand Knowledge Base**: Add more job roles and industry-specific advice
2. **Fine-tune Parameters**: Optimize Top K and Top P values for different use cases
3. **Add More Integrations**: Connect with job market APIs for real-time requirements
4. **User Interface**: Develop web-based interface for easier interaction

### 📊 Monitoring & Optimization
1. **Token Usage Tracking**: Monitor API costs with built-in usage reporting
2. **Performance Analytics**: Track which parameters and settings work best
3. **User Feedback**: Collect feedback on result quality and relevance
4. **Continuous Learning**: Use feedback to improve prompts and knowledge base

### 🎯 Advanced Features to Consider
1. **Personalization**: Remember user preferences and history
2. **Multi-language Support**: Extend to other languages beyond English
3. **Industry-specific Models**: Fine-tune for specific industries or job types
4. **Integration APIs**: Allow other applications to use the resume optimization engine

## Support & Documentation

### 📚 Additional Resources
- **[TOP_K_EXAMPLES.md](ai-career-mentor/TOP_K_EXAMPLES.md)**: Detailed Top K parameter guide
- **[TOP_P_EXAMPLES.md](ai-career-mentor/TOP_P_EXAMPLES.md)**: Comprehensive Top P documentation
- **[VECTOR_DATABASE_README.md](ai-career-mentor/VECTOR_DATABASE_README.md)**: In-depth vector database documentation

### 🛠️ Troubleshooting
- **Vector DB Issues**: Check that all dependencies are installed correctly
- **API Key Problems**: Verify `.env` file contains valid Gemini API key
- **Search Results**: If semantic search fails, system automatically uses fallback method
- **Performance**: Monitor token usage to optimize API costs

## Contributing

The AI Career Mentor is designed to be extensible. Consider contributing:
- New job role definitions
- Enhanced career tips and examples
- Improved prompt engineering
- Additional AI parameter options
- User interface enhancements

---

**✨ Ready to optimize your resume?** Run `python main.py` and experience the power of enhanced AI with vector database integration!
