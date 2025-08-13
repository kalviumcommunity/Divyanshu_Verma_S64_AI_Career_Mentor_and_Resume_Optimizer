"""
Gemini API Client for AI Career Mentor

This module handles communication with Google's Gemini API, including:
- API key management through environment variables
- Structured output (JSON format enforcement)
- Basic error handling for API failures
"""

import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Module-level flag to track initialization status
_INITIALIZED = False


def initialize_gemini():
    """
    Initialize the Gemini API with the API key from environment variables.
    Uses a module-level flag to prevent redundant reconfigurations.
    
    Raises:
        ValueError: If API key is not found in environment variables
    """
    global _INITIALIZED
    
    # Skip if already initialized
    if _INITIALIZED:
        return
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please check your .env file and make sure it contains: "
            "GEMINI_API_KEY=your_actual_api_key_here"
        )
    
    try:
        genai.configure(api_key=api_key)
        _INITIALIZED = True
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini API: {str(e)}")




def extract_json_from_response(response_text):
    """
    Extract JSON block from response text that may contain markdown fences or explanatory text.
    
    Args:
        response_text (str): Raw response text from Gemini API
    
    Returns:
        str: Extracted JSON string or original text if no JSON block found
    """
    # Remove markdown code fences if present
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*$', '', response_text, flags=re.MULTILINE)
    
    # Try to find JSON block using regex (first occurrence of {...})
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        return json_match.group(0).strip()
    
    # If no braces found, return original text (will likely fail JSON parsing)
    return response_text.strip()


def validate_json_response(response_text):
    """
    Validate and parse JSON response from Gemini, handling markdown fences and text.
    
    Args:
        response_text (str): Raw response text from Gemini API
    
    Returns:
        dict: Parsed JSON response or error dict if invalid
    """
    try:
        # Extract JSON from potentially wrapped response
        json_text = extract_json_from_response(response_text)
        
        # Try to parse the JSON
        parsed_response = json.loads(json_text)
        
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
        
        # Validate that all elements in resumeBullets are strings
        for i, bullet in enumerate(parsed_response["resumeBullets"]):
            if not isinstance(bullet, str):
                return {
                    "error": "Invalid resumeBullets format",
                    "suggestion": f"resumeBullets[{i}] must be a string, got {type(bullet).__name__}"
                }
        
        # Validate that all elements in skillGaps are strings
        for i, gap in enumerate(parsed_response["skillGaps"]):
            if not isinstance(gap, str):
                return {
                    "error": "Invalid skillGaps format",
                    "suggestion": f"skillGaps[{i}] must be a string, got {type(gap).__name__}"
                }
        
        return parsed_response
        
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON response from AI",
            "suggestion": f"JSON parsing failed: {str(e)}. Extracted text: {json_text[:100]}..."
        }


def get_generation_config(tone="professional"):
    """
    Get generation configuration based on tone preference.
    
    Temperature controls creativity and randomness in responses:
    - Lower temperature (0.3) = More consistent, focused, professional responses
    - Higher temperature (0.8) = More creative, varied, innovative responses
    
    Args:
        tone (str): Either "professional" or "creative"
    
    Returns:
        dict: Generation configuration for Gemini API
    
    Examples:
        Professional tone produces consistent, formal resume bullets:
        "Developed web applications using React and JavaScript"
        
        Creative tone produces more varied, dynamic language:
        "Crafted innovative web solutions leveraging React ecosystem"
    """
    if tone == "professional":
        return {
            "temperature": 0.3,  # Less creative, more consistent
            "max_output_tokens": 500
        }
    elif tone == "creative":
        return {
            "temperature": 0.8,  # More creative, more varied
            "max_output_tokens": 500
        }
    else:
        # Default to professional if invalid tone provided
        return {
            "temperature": 0.3,
            "max_output_tokens": 500
        }


def estimate_token_count(text):
    """
    Estimate token count based on text length.
    Rough approximation: 1 token ≈ 4 characters for English text.
    
    Args:
        text (str): Text to estimate tokens for
    
    Returns:
        int: Estimated token count
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def log_token_usage(response, input_text=""):
    """
    Log token usage information from Gemini API response.
    
    Args:
        response: Gemini API response object containing usage metadata
        input_text (str): Input text for token estimation if metadata unavailable
    """
    try:
        # Check multiple possible locations for usage metadata
        usage = None
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        
        # Try different ways to access usage metadata
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage = response.usage_metadata
            prompt_tokens = getattr(usage, 'prompt_token_count', 0)
            completion_tokens = getattr(usage, 'candidates_token_count', 0)
            total_tokens = getattr(usage, 'total_token_count', 0)
        elif hasattr(response, 'candidates') and response.candidates:
            # Try to get usage from candidates
            candidate = response.candidates[0]
            if hasattr(candidate, 'token_count'):
                completion_tokens = candidate.token_count
        
        # If we found any token information, display it
        if prompt_tokens > 0 or completion_tokens > 0 or total_tokens > 0:
            print("\n" + "="*50)
            print("📊 TOKEN USAGE REPORT")
            print("="*50)
            print(f"Input tokens:  {prompt_tokens:,}")
            print(f"Output tokens: {completion_tokens:,}")
            print(f"Total tokens:  {total_tokens:,}")
            print("="*50)
            print("💡 Token usage helps you understand API costs")
            print("   Gemini pricing is based on token consumption")
            print("="*50 + "\n")
        else:
            # Provide estimated token counts
            estimated_input = estimate_token_count(input_text)
            
            # Try to get output text for estimation
            output_text = ""
            if hasattr(response, 'parts') and response.parts:
                output_text = response.parts[0].text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    output_text = candidate.content.parts[0].text
            
            estimated_output = estimate_token_count(output_text)
            estimated_total = estimated_input + estimated_output
            
            print("\n" + "="*50)
            print("📊 TOKEN USAGE REPORT (ESTIMATED)")
            print("="*50)
            print(f"Input tokens:  ~{estimated_input:,} (estimated)")
            print(f"Output tokens: ~{estimated_output:,} (estimated)")
            print(f"Total tokens:  ~{estimated_total:,} (estimated)")
            print("="*50 + "\n")
            
    except Exception as e:
        print(f"\n⚠️  Could not retrieve token usage: {str(e)}\n")


def call_gemini_api(system_prompt, user_prompt, tone="professional", max_retries=1):
    """
    Send prompts to Google's Gemini API and return generated response.
    
    Args:
        system_prompt (str): System prompt defining AI behavior
        user_prompt (str): User prompt with specific request
        tone (str): Either "professional" (temp=0.3) or "creative" (temp=0.8)
        max_retries (int): Number of retries if JSON parsing fails
    
    Returns:
        dict: Parsed JSON response or error dict
    
    Temperature Examples:
        Professional (0.3): "Developed responsive web applications using React"
        Creative (0.8): "Architected dynamic user experiences with React ecosystem"
    
    Token Logging:
        Automatically logs input/output token counts after each API call
        to help users understand API usage and costs
    
    Example:
        response = call_gemini_api(
            system_prompt="You are a career mentor...",
            user_prompt="Help John optimize his resume...",
            tone="creative"
        )
    """
    try:
        # Initialize Gemini API
        initialize_gemini()
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
        
        # Get generation configuration based on tone
        generation_config = get_generation_config(tone)
        
        # Attempt to get response with retries
        for attempt in range(max_retries + 1):
            try:
                # Generate content with temperature control
                response = model.generate_content(
                    contents=full_prompt,
                    generation_config=generation_config
                )
                
                # Log token usage information with input text for estimation
                log_token_usage(response, full_prompt)
                
                # Get response text using proper accessor
                response_text = ""
                
                # Try response.parts first (recommended approach)
                if hasattr(response, 'parts') and response.parts:
                    response_text = response.parts[0].text.strip()
                # Fallback to candidate approach
                elif response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        response_text = candidate.content.parts[0].text.strip()
                
                if response_text:
                    validated_response = validate_json_response(response_text)
                    
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

