""" 
config.py
--------------

One place to load all settings for the chatbot.
Uses python-dotenv to read from your .env file.

Why have a separate config file?
  - You never scatter os.getenv() calls all over the code 
  - Easy to see every settings in one place 
  - Easy to add new settings later (e.g. temperature, max_tokens)

Groq models available :
  llama-3.3-70b-versatile  <- default, best quality
  llama3-8b-8192
  mixtral-8x7b-32768
  gemma2-9b-it
""" 

import os 
from dotenv import load_dotenv 

# Load the .env file into the process environment 
# This makes ANTHROPIC_API_KEY as os.environ["ANTHROPIC_API_KEY"]

load_dotenv()

def get_config() -> dict:
    """
    Returns a dictionary of all settings the chatbot needs.
    Raises a clear error if the API key is missing.
    """
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key == "gsk_your-key-here":
        raise ValueError(
            "\n\n GROQ_API_KEY is not set!\n"
            "    1. Copy .env.example  ->  .env\n"
            "    2. Paste your real key from https://console.groq.com\n" 
            
        )
        
    base_prompt =  os.getenv(
        "SYSTEM_PROMPT",
        "You are a personal mentor and expert teacher. Keep answers short and direct. Talk like a smart friend, not a textbook.",
            
    )
    
    
    return {
        "api_key": api_key,
        "model": os.getenv("MODEL", "llama-3.3-70b-versatile"),
        "system_prompt": base_prompt,
        "max_tokens": int(os.getenv("MAX_TOKENS", "1024")),
        
    }
        