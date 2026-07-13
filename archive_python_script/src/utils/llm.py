import os
from dotenv import load_dotenv

# Load env variables from .env if present
load_dotenv()

def get_gemini_client():
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables")
    return genai.Client(api_key=api_key)

def get_anthropic_client():
    from anthropic import Anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY in environment variables")
    return Anthropic(api_key=api_key)

def get_deepseek_client():
    from openai import OpenAI
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Missing DEEPSEEK_API_KEY in environment variables")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def call_llm(provider, model_name, prompt, system_instruction=None):
    provider = provider.lower()
    
    if provider == "gemini":
        client = get_gemini_client()
        config = {}
        if system_instruction:
            config["system_instruction"] = system_instruction
        
        # Using the standard modern google-genai library
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config
        )
        return response.text

    elif provider == "anthropic":
        client = get_anthropic_client()
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": model_name,
            "max_tokens": 16000,
            "messages": messages
        }
        if system_instruction:
            kwargs["system"] = system_instruction
            
        response = client.messages.create(**kwargs)
        # Handle message blocks properly
        return "".join([block.text for block in response.content if hasattr(block, 'text')])

    elif provider == "deepseek":
        client = get_deepseek_client()
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
