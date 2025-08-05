# AI Career Mentor & Resume Optimizer

A simple Python application that helps job seekers create better resumes by generating tailored bullet points and identifying skill gaps. This project demonstrates 5 key AI concepts in an easy-to-understand way.

## What This Project Does

Input your name, skills, and target job role, and get:
- 3-5 personalized resume bullet points
- 2-3 skills you should learn next
- Professional or creative tone options

## The 5 AI Concepts Explained

### 1. System Prompt & User Prompt
**What it is:** Instructions that tell the AI what role to play and what you want

### 2. Structured Output
**What it is:** Making sure the AI returns data in a specific format (like JSON)

### 3. Function Calling
**What it is:** The AI can call specific functions to get information

### 4. Tunable Parameters
**What it is:** Settings that control how creative or consistent the AI is

### 5. RAG (Retrieval-Augmented Generation)
**What it is:** The AI uses a knowledge base to give better, more accurate answers

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.8+ installed on your computer.

### 2. Clone/Download Project
```bash
git clone <your-repo-url>
cd ai-career-mentor
```

### 3. Create Virtual Environment
```bash
python -m venv venv
```

### 4. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Set Up API Key
1. Copy `.env.example` to `.env`
2. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Add your key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

### 7. Run the Program
```bash
python main.py
```

## How to Use

1. Run `python main.py`
2. Enter your name when prompted
3. List your current skills (comma-separated)
4. Enter your target job role
5. Choose tone: "professional" or "creative"
6. Get your personalized resume help!


## Project Structure
```
ai-career-mentor/
├── main.py              # Main program - run this!
├── prompts.py           # System & user prompts
├── gemini_client.py     # AI API calls & settings
├── job_functions.py     # Job requirements function
├── rag_knowledge.py     # Career tips knowledge base
├── requirements.txt     # Python packages needed
├── .env.example        # API key template
└── README.md           # This file!
```

## Troubleshooting

**"No module named 'google.generativeai'"**
- Make sure you activated your virtual environment
- Run `pip install -r requirements.txt`

**"API key not found"**
- Check your `.env` file has `GEMINI_API_KEY=your_key`
- Make sure `.env` is in the same folder as `main.py`

**"Invalid JSON response"**
- The AI sometimes returns broken JSON - just try again
- Check your internet connection
