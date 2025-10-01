#!/usr/bin/env python3
"""
Vector Database Demo Script

This script demonstrates the enhanced RAG capabilities with vector database integration.
It shows how semantic search improves knowledge retrieval compared to keyword matching.
"""

from rag_knowledge import (
    retrieveCareerTips, 
    retrieveResumeExamples, 
    searchKnowledgeBase,
    addKnowledgeToDatabase,
    getVectorDatabaseStats
)
import json

def demo_basic_functionality():
    """Demonstrate basic enhanced RAG functionality"""
    print("="*60)
    print("🚀 VECTOR DATABASE DEMO - Enhanced RAG System")
    print("="*60)
    
    # Show database stats
    stats = getVectorDatabaseStats()
    print(f"\n📊 Vector Database Stats:")
    print(f"   Status: {stats['status']}")
    print(f"   Documents: {stats.get('count', 0)}")
    
    # Test career tips retrieval
    print(f"\n🎯 Testing Career Tips Retrieval:")
    job_role = "data scientist"
    tips = retrieveCareerTips(job_role)
    print(f"   Job Role: {job_role}")
    print(f"   Retrieved {len(tips)} tips:")
    for i, tip in enumerate(tips[:3], 1):
        print(f"   {i}. {tip}")
    
    # Test resume examples retrieval
    print(f"\n📝 Testing Resume Examples Retrieval:")
    examples = retrieveResumeExamples(job_role)
    print(f"   Job Role: {job_role}")
    print(f"   Retrieved {len(examples)} examples:")
    for i, example in enumerate(examples[:2], 1):
        print(f"   {i}. {example}")

def demo_semantic_search():
    """Demonstrate semantic search capabilities"""
    print(f"\n🔍 Testing Semantic Search:")
    
    # Test queries that should work well with semantic search
    test_queries = [
        "How to show leadership skills on resume",
        "Machine learning project examples",
        "API development best practices",
        "User experience design tips"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        results = searchKnowledgeBase(query)
        
        print(f"   Search Method: {results.get('search_method', 'unknown')}")
        
        if results['career_tips']:
            print(f"   Top Career Tip: {results['career_tips'][0]}")
        
        if results['resume_examples']:
            print(f"   Top Resume Example: {results['resume_examples'][0]}")
        
        # Show similarity scores if available
        if 'tip_scores' in results and results['tip_scores']:
            print(f"   Tip Similarity: {results['tip_scores'][0]:.3f}")
        if 'example_scores' in results and results['example_scores']:
            print(f"   Example Similarity: {results['example_scores'][0]:.3f}")

def demo_add_knowledge():
    """Demonstrate adding new knowledge to the database"""
    print(f"\n➕ Testing Knowledge Addition:")
    
    # Add a new career tip
    new_tip = "Highlight open source contributions and community involvement to show passion for technology"
    success = addKnowledgeToDatabase(
        content=new_tip,
        job_role="software_engineer",
        content_type="career_tip",
        source="demo_script"
    )
    
    print(f"   Added new career tip: {success}")
    print(f"   Content: {new_tip}")
    
    # Add a new resume example
    new_example = "Contributed to 5+ open source projects with 100+ GitHub stars, demonstrating collaborative coding skills"
    success = addKnowledgeToDatabase(
        content=new_example,
        job_role="software_engineer", 
        content_type="resume_example",
        source="demo_script"
    )
    
    print(f"   Added new resume example: {success}")
    print(f"   Content: {new_example}")
    
    # Test searching for the new content
    print(f"\n   Testing search for new content:")
    results = searchKnowledgeBase("open source contributions")
    if results['career_tips']:
        print(f"   Found tip: {results['career_tips'][0]}")
    if results['resume_examples']:
        print(f"   Found example: {results['resume_examples'][0]}")

def demo_cross_role_search():
    """Demonstrate cross-role semantic search"""
    print(f"\n🌐 Testing Cross-Role Search:")
    
    # Search without specifying a role - should find relevant content across all roles
    query = "teamwork and collaboration"
    results = searchKnowledgeBase(query)
    
    print(f"   Query: '{query}'")
    print(f"   Search Method: {results.get('search_method', 'unknown')}")
    print(f"   Found {len(results['career_tips'])} tips and {len(results['resume_examples'])} examples")
    
    # Show diverse results from different roles
    if 'tip_scores' in results:
        for i, (tip, score) in enumerate(zip(results['career_tips'][:3], results['tip_scores'][:3])):
            print(f"   Tip {i+1} (score: {score:.3f}): {tip[:80]}...")

def main():
    """Run all demonstrations"""
    try:
        demo_basic_functionality()
        demo_semantic_search()
        demo_add_knowledge()
        demo_cross_role_search()
        
        print(f"\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nKey Benefits of Vector Database Integration:")
        print("• Semantic search finds relevant content even without exact keyword matches")
        print("• Cross-role knowledge discovery for better recommendations")
        print("• Dynamic knowledge addition without code changes")
        print("• Similarity scoring for result relevance")
        print("• Automatic fallback to dictionary-based approach if vector DB fails")
        print("• Persistent storage of knowledge across application restarts")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure to install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()