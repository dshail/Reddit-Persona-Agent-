import os
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from reddit_scraper import scrape_reddit_user

load_dotenv()

def compare_personas(url1: str, url2: str) -> str:
    """
    Compare two Reddit users and generate a comparison report.
    """
    # Scrape data for both users
    print("🔍 Scraping first user...")
    user1_data = scrape_reddit_user(url1)
    username1 = url1.strip("/").split("/")[-1]
    
    print("🔍 Scraping second user...")
    user2_data = scrape_reddit_user(url2)
    username2 = url2.strip("/").split("/")[-1]
    
    # Prepare content for comparison
    user1_content = prepare_user_content(user1_data, username1)
    user2_content = prepare_user_content(user2_data, username2)
    
    # Generate comparison using LLM
    comparison_prompt = """
    You are an expert in behavioral analysis and user comparison.
    
    Compare these two Reddit users and provide a detailed comparison report:
    
    USER 1 ({username1}):
    {user1_content}
    
    USER 2 ({username2}):
    {user2_content}
    
    Generate a comparison report with:
    1. **Common Interests & Similarities**
    2. **Key Differences in Personality**
    3. **Communication Style Comparison**
    4. **Engagement Pattern Differences**
    5. **Subreddit Preferences Comparison**
    6. **Overall Compatibility Assessment**
    
    For each section, cite specific examples from their posts/comments.
    """
    
    prompt = PromptTemplate(
        input_variables=["username1", "user1_content", "username2", "user2_content"],
        template=comparison_prompt
    )
    
    llm = ChatOpenAI(
        temperature=0.5,
        model="openai/gpt-4o-mini",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.run(
        username1=username1,
        user1_content=user1_content,
        username2=username2,
        user2_content=user2_content
    )
    
    return result

def prepare_user_content(user_data: Dict, username: str) -> str:
    """Prepare user content for comparison analysis."""
    content_chunks = []
    for section, items in user_data.items():
        for item in items[:15]:  # Limit to avoid token overflow
            content_chunks.append(f"[{section.upper()}] {item['text'][:200]}...")
    
    return "\n---\n".join(content_chunks)