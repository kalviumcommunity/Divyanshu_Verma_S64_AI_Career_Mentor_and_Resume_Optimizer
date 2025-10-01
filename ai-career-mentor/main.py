#!/usr/bin/env python3
"""
AI Career Mentor & Resume Optimizer
Simple MVP that helps job seekers create better resumes
"""

# Import our custom modules
from job_functions import getJobRequirements, getAllJobRoles
from rag_knowledge import retrieveCareerTips, retrieveResumeExamples, searchKnowledgeBase, getVectorDatabaseStats
from gemini_client import call_gemini_api
from prompts import SYSTEM_PROMPT, create_user_prompt
import json

def collect_user_input():
    """Collect user information using simple input statements"""
    print("=== AI Career Mentor & Resume Optimizer ===")
    print()
    
    # Collect basic user information
    name = input("Enter your name: ").strip()
    
    # Collect skills as comma-separated list
    skills_input = input("Enter your current skills (comma-separated): ").strip()
    skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
    
    # Collect target job role
    target_role = input("Enter target job role: ").strip()
    
    # Collect tone preference
    print("\nChoose your preferred tone:")
    print("1. Professional (formal, consistent)")
    print("2. Creative (varied, innovative)")
    tone_choice = input("Enter choice (1 or 2): ").strip()
    
    # Convert choice to tone
    if tone_choice == "2":
        tone = "creative"
    else:
        tone = "professional"  # Default to professional
    
    # Collect top_k preference for vocabulary diversity
    print("\nChoose vocabulary diversity (Top K parameter):")
    print("1. Focused vocabulary (top_k=20) - More predictable, common words")
    print("2. Balanced vocabulary (top_k=40) - Default Gemini setting")
    print("3. Diverse vocabulary (top_k=80) - More creative, varied word choices")
    print("4. Skip (use default)")
    top_k_choice = input("Enter choice (1-4): ").strip()
    
    # Convert choice to top_k value
    top_k = None
    if top_k_choice == "1":
        top_k = 20
    elif top_k_choice == "2":
        top_k = 40
    elif top_k_choice == "3":
        top_k = 80
    # Choice 4 or invalid = None (use default)
    
    # Collect top_p preference for nucleus sampling
    print("\nChoose creativity level (Top P parameter):")
    print("1. Conservative (top_p=0.3) - Focused, predictable responses")
    print("2. Balanced (top_p=0.7) - Good balance of focus and creativity")
    print("3. Creative (top_p=0.9) - More diverse, creative responses")
    print("4. Skip (use default)")
    top_p_choice = input("Enter choice (1-4): ").strip()
    
    # Convert choice to top_p value
    top_p = None
    if top_p_choice == "1":
        top_p = 0.3
    elif top_p_choice == "2":
        top_p = 0.7
    elif top_p_choice == "3":
        top_p = 0.9
    # Choice 4 or invalid = None (use default)
    
    return {
        "name": name,
        "skills": skills,
        "target_role": target_role,
        "tone": tone,
        "top_k": top_k,
        "top_p": top_p
    }

def process_user_request(user_data):
    """Process the user request by calling all functions in the right order"""
    print("\n" + "="*50)
    print("PROCESSING YOUR REQUEST...")
    print("="*50)
    
    # Step 1: Get job requirements using function calling
    print("🔍 Step 1: Looking up job requirements...")
    job_requirements = getJobRequirements(user_data['target_role'])
    print(f"✓ Found requirements for: {job_requirements['role']}")
    
    # Step 2: Retrieve career tips using enhanced RAG with vector database
    print("📚 Step 2: Retrieving career tips from enhanced knowledge base...")
    career_tips = retrieveCareerTips(user_data['target_role'])
    print(f"✓ Retrieved {len(career_tips)} career tips using semantic search")
    
    # Step 3: Get resume examples using enhanced RAG with vector database
    print("📝 Step 3: Getting resume examples with semantic matching...")
    resume_examples = retrieveResumeExamples(user_data['target_role'])
    print(f"✓ Found {len(resume_examples)} resume examples using vector similarity")
    
    # Step 4: Analyze skill gaps
    print("🎯 Step 4: Analyzing skill gaps...")
    skill_gaps = analyze_skill_gaps(user_data['skills'], job_requirements['required_skills'])
    print(f"✓ Identified {len(skill_gaps)} skill gaps")
    
    # Step 5: Generate AI-powered resume bullets using structured output
    print("🤖 Step 5: Generating AI-powered resume bullets with structured output...")
    ai_response = generate_ai_response(user_data, job_requirements, career_tips)
    
    if "error" in ai_response:
        print(f"⚠️  AI generation failed: {ai_response['error']}")
    
    else:
        print(f"✓ AI generated {len(ai_response['resumeBullets'])} resume bullets")
        print(f"✓ AI identified {len(ai_response['skillGaps'])} skill gaps")
        resume_bullets = ai_response['resumeBullets']
        ai_skill_gaps = ai_response['skillGaps']
    
    return {
        "job_requirements": job_requirements,
        "career_tips": career_tips,
        "resume_examples": resume_examples,
        "skill_gaps": ai_skill_gaps,
        "resume_bullets": resume_bullets
    }

def analyze_skill_gaps(user_skills, required_skills):
    """Analyze what skills the user is missing"""
    # Convert to lowercase for comparison
    user_skills_lower = [skill.lower() for skill in user_skills]
    
    # Find missing skills
    missing_skills = []
    for required_skill in required_skills:
        if required_skill.lower() not in user_skills_lower:
            missing_skills.append(required_skill)
    
    # Return up to 3 skill gaps as specified in requirements
    return missing_skills[:3]

def generate_ai_response(user_data, job_requirements, career_tips):
    """Generate AI-powered resume bullets and skill gaps using structured output"""
    try:
        # Create user prompt with all the context
        user_prompt = create_user_prompt(user_data, job_requirements, career_tips)
        
        # Call Gemini API with structured output, temperature control, top_k, and top_p parameters
        response = call_gemini_api(SYSTEM_PROMPT, user_prompt, tone=user_data['tone'], top_k=user_data.get('top_k'), top_p=user_data.get('top_p'), max_retries=1)
        
        return response
        
    except Exception as e:
        return {
            "error": f"AI generation failed: {str(e)}",
            "suggestion": "Check your API key and internet connection"
        }

def generate_resume_bullets(user_data, job_requirements, career_tips, resume_examples):
    """Generate personalized resume bullets based on user data and knowledge"""
    # This simulates what the AI would do - combine user info with knowledge
    bullets = []
    
    # Use the first few resume examples as templates
    for i, example in enumerate(resume_examples[:3]):
        # Personalize the example with user's skills if possible
        personalized_bullet = example
        
        # Try to incorporate user's skills into the bullet
        for skill in user_data['skills']:
            if skill.lower() in example.lower():
                # This bullet already mentions one of their skills
                break
        else:
            # Add user's skills to make it more personalized
            if user_data['skills']:
                skill_to_add = user_data['skills'][0]  # Use first skill
                personalized_bullet = example.replace("using", f"using {skill_to_add} and")
        
        bullets.append(personalized_bullet)
    
    # Add one more bullet that's more generic but personalized
    if user_data['skills']:
        skills_str = ", ".join(user_data['skills'][:3])  # Use first 3 skills
        bullets.append(f"Leveraged {skills_str} to deliver high-quality solutions and exceed project expectations")
    
    return bullets[:4]  # Return up to 4 bullets as specified

def display_results(user_data, processed_data):
    """Display the final results in a structured format"""
    print("\n" + "="*60)
    print("🎉 AI CAREER MENTOR RESULTS")
    print("="*60)
    
    # Show vector database status
    db_stats = getVectorDatabaseStats()
    print(f"\n🗄️  Enhanced RAG System Status:")
    print(f"   Vector Database: {db_stats['status']}")
    if db_stats['status'] == 'available':
        print(f"   Knowledge Documents: {db_stats['count']}")
        print(f"   Search Method: Semantic similarity matching")
    else:
        print(f"   Fallback: Dictionary-based retrieval")
    
    # Display user info
    print(f"\n👤 Candidate: {user_data['name']}")
    print(f"🎯 Target Role: {processed_data['job_requirements']['role']}")
    print(f"🎨 Tone: {user_data['tone'].title()}")
    print(f"🎛️  Top K: {user_data.get('top_k', 'Default')} (vocabulary diversity)")
    print(f"🎯 Top P: {user_data.get('top_p', 'Default')} (nucleus sampling)")
    print(f"💼 Current Skills: {', '.join(user_data['skills'])}")
    
    # Display the main output in JSON format (as specified in requirements)
    print("\n" + "="*60)
    print("📋 RESUME OPTIMIZATION RESULTS")
    print("="*60)
    
    final_output = {
        "resumeBullets": processed_data['resume_bullets'],
        "skillGaps": processed_data['skill_gaps']
    }
    
    print(json.dumps(final_output, indent=2))
    
    # Display additional insights
    print("\n" + "="*60)
    print("💡 ADDITIONAL INSIGHTS")
    print("="*60)
    
    print(f"\n🔍 Job Requirements Analysis:")
    print(f"   Required Skills: {', '.join(processed_data['job_requirements']['required_skills'])}")
    print(f"   Nice to Have: {', '.join(processed_data['job_requirements']['nice_to_have'])}")
    
    print(f"\n📚 Top Career Tips for {processed_data['job_requirements']['role']}:")
    for i, tip in enumerate(processed_data['career_tips'][:3], 1):
        print(f"   {i}. {tip}")
    
    print(f"\n✅ Skills You Already Have:")
    matching_skills = [skill for skill in user_data['skills'] 
                      if skill.lower() in [req.lower() for req in processed_data['job_requirements']['required_skills']]]
    if matching_skills:
        print(f"   {', '.join(matching_skills)}")
    else:
        print("   Consider highlighting transferable skills that relate to the job requirements")
    
    return final_output

def main():
    """Main application entry point - connects everything together"""
    try:
        # Step 1: Collect user input
        user_data = collect_user_input()
        
        # Step 2: Validate that we have minimum required information
        if not user_data['name'] or not user_data['target_role']:
            print("\nError: Name and target role are required!")
            return
        
        if not user_data['skills']:
            print("\nWarning: No skills provided. Consider adding some skills for better results.")
            user_data['skills'] = []  # Ensure it's an empty list, not None
        
        # Step 3: Process the user request by calling all functions in order
        processed_data = process_user_request(user_data)
        
        # Step 4: Display the final results
        final_output = display_results(user_data, processed_data)
        
        # Step 5: Offer to run again or exit
        print("\n" + "="*60)
        print("🚀 PROGRAM COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nAll functions have been called and integrated:")
        print("✓ User input collection")
        print("✓ Function calling (getJobRequirements)")
        print("✓ RAG knowledge retrieval (career tips & examples)")
        print("✓ Skill gap analysis")
        print("✓ Resume bullet generation")
        print("✓ Structured JSON output")
        
        # Ask if user wants to try again
        print("\nWould you like to try with different information? (y/n): ", end="")
        try:
            choice = input().strip().lower()
            if choice == 'y' or choice == 'yes':
                print("\n" + "="*60)
                main()  # Recursive call to start over
        except:
            pass  # User pressed Ctrl+C or similar
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check that all required files are present and try again.")

if __name__ == "__main__":
    main()