"""
NEW 03: Direct Azure OpenAI Chat (Interactive Demo)

This demo uses Azure OpenAI DIRECTLY (not Azure AI Foundry Agent Service).
The chat is not persistent - it exists only for this session.
"""

import os
from dotenv import load_dotenv

from openai import AzureOpenAI

# Load environment variables
load_dotenv('.env03')

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-11-20")


def main():
    """Interactive demo: Azure OpenAI direct chat."""
    
    print("\n" + "="*70)
    print("🤖✨ DEMO: Direct Azure OpenAI Chat (API Key Auth)")
    print("="*70)
    
    # Create Azure OpenAI client using API Key
    client = AzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=API_KEY,
        api_version=API_VERSION
    )
    
    print("\n✅ Client created (temporary session, not saved to cloud)")
    
    print("\n" + "="*70)
    print("💬 Interactive Chat (Type 'quit' to exit)")
    print("="*70 + "\n")
    
    # Maintain conversation history
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Be concise and clear."}
    ]
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n🤝 Thank You!")
            break
        
        if not user_input.strip():
            continue
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Get streaming response
        print("Agent: ", end="", flush=True)
        
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages,
            stream=True
        )
        
        assistant_response = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                assistant_response += content
        
        # Add assistant response to history
        messages.append({"role": "assistant", "content": assistant_response})
        print("\n")


if __name__ == "__main__":
    main()
