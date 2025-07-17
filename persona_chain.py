import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Read the prompt template from file
def load_prompt_template():
    with open("prompts/persona_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def generate_user_persona(user_data: dict) -> str:
    """
    Generates a user persona using LangChain and OpenAI LLM.
    user_data: Dict containing 'posts' and 'comments' (list of dicts with text and permalink).
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("Missing OpenRouter API key in environment variables.")

    # Prepare raw input content from user data
    content_chunks = []
    for section, items in user_data.items():
        for item in items[:20]:  # Limit per section to avoid token overflow
            content_chunks.append(f"[{section.upper()}] {item['text']}\nSource: {item['permalink']}\n")

    full_text = "\n---\n".join(content_chunks)

    # Load prompt template
    raw_prompt = load_prompt_template()

    # Prepare LangChain prompt
    prompt = PromptTemplate(
        input_variables=["user_content"],
        template=raw_prompt
    )

    # Initialize LLM with OpenRouter
    llm = ChatOpenAI(
        temperature=0.5, 
        model="openai/gpt-4o-mini",  # OpenRouter model format
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )

    # Create LLM chain (using newer syntax to avoid deprecation warnings)
    try:
        # Try newer syntax first
        chain = prompt | llm
        result = chain.invoke({"user_content": full_text})
        if hasattr(result, 'content'):
            result = result.content
    except Exception:
        # Fallback to older syntax if needed
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        )
        result = chain.run(user_content=full_text)

    return result
