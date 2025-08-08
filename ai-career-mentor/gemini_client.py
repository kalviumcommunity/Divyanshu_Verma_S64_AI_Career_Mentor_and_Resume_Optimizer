"""
Gemini API Client for AI Career Mentor

This module handles communication with Google's Gemini API, including:
- API key management through environment variables
- Structured output (JSON format enforcement)
- Basic error handling for API failures
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize_gemini():
    """
    Initialize the Gemini API with the API key from environment variables.
    
    Returns:
        bool: True if initialization successful, False otherwise
    
    Raises:
        ValueError: If API key is not found in environment variables
    """
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please check your .env file and make sure it contains: "
            "GEMINI_API_KEY=your_actual_api_key_here"
        )
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini API: {str(e)}")


def get_generation_config():
    """
    Get basic generation configuration for Gemini API.
    
    Returns:
        dict: Basic generation configuration
    """
    return {
        "max_output_tokens": 500,
        "top_k": 40,
        "top_p": 0.8,
        "temperature": 0.7  # Default balanced temperature
    }


def validate_json_response(response_text):
    """
    Validate and parse JSON response from Gemini.
    
    Args:
        response_text (str): Raw response text from Gemini API
    
    Returns:
        dict: Parsed JSON response or error dict if invalid
    """
    try:
        # Try to parse the JSON
        parsed_response = json.loads(response_text)
        
        # Validate that required fields exist
        if "resumeBullets" not in parsed_response or "skillGaps" not in parsed_response:
            return {
                "error": "Invalid response format",
                "suggestion": "Response missing required fields: resumeBullets or skillGaps"
            }
        
        # Validate that fields are lists
        if not isinstance(parsed_response["resumeBullets"], list) or not isinstance(parsed_response["skillGaps"], list):
            return {
                "error": "Invalid response format", 
                "suggestion": "resumeBullets and skillGaps must be arrays"
            }
        
        return parsed_response
        
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON response from AI",
            "suggestion": f"JSON parsing failed: {str(e)}"
        }


def call_gemini_api(system_prompt, user_prompt, max_retries=1):
    """
    Send prompts to Google's Gemini API and return generated response.
    
    Args:
        system_prompt (str): System prompt defining AI behavior
        user_prompt (str): User prompt with specific request
        max_retries (int): Number of retries if JSON parsing fails
    
    Returns:
        dict: Parsed JSON response or error dict
    
    Example:
        response = call_gemini_api(
            system_prompt="You are a career mentor...",
            user_prompt="Help John optimize his resume..."
        )
    """
    try:
        # Initialize Gemini API
        initialize_gemini()
        
        # Get basic generation configuration
        generation_config = get_generation_config()
        
        # Create the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Add JSON format instruction to ensure structured output
        json_instruction = """

IMPORTANT: Respond ONLY with valid JSON in this exact format:
{
    "resumeBullets": [
        "bullet point 1",
        "bullet point 2", 
        "bullet point 3"
    ],
    "skillGaps": [
        "skill gap 1",
        "skill gap 2",
        "skill gap 3"
    ]
}

Do not include any text before or after the JSON."""
        
        # Combine prompts with JSON instruction
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n{json_instruction}"
        
        # Attempt to get response with retries
        for attempt in range(max_retries + 1):
            try:
                # Generate content
                response = model.generate_content(
                    contents=full_prompt,
                    generation_config=generation_config
                )
                
                # Validate and parse the response
                if response.text:
                    validated_response = validate_json_response(response.text.strip())
                    
                    # If validation successful, return the response
                    if "error" not in validated_response:
                        return validated_response
                    
                    # If this was the last attempt, return the error
                    if attempt == max_retries:
                        return validated_response
                        
                else:
                    if attempt == max_retries:
                        return {
                            "error": "Empty response from Gemini API",
                            "suggestion": "Try again or check your API key"
                        }
                        
            except Exception as api_error:
                if attempt == max_retries:
                    return {
                        "error": f"Gemini API call failed: {str(api_error)}",
                        "suggestion": "Check your internet connection and API key"
                    }
                    
    except ValueError as init_error:
        return {
            "error": str(init_error),
            "suggestion": "Check your .env file and API key setup"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "suggestion": "Please try again or contact support"
        }

