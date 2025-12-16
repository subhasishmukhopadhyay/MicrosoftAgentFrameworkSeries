"""
NEW 02: Use Existing Azure AI Foundry Agent (Interactive Demo)

This demo connects to an EXISTING agent in Azure AI Foundry.
You'll need to update the .env02 file with your agent ID.
"""

import asyncio
import os
from dotenv import load_dotenv

from azure.identity.aio import AzureCliCredential
from azure.ai.agents.aio import AgentsClient

# Load environment variables
load_dotenv('.env02')

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AI_AGENT_ID")


async def main():
    """Interactive demo: Connect to existing agent."""
    
    print("\n" + "="*70)
    print("🔗✨ DEMO: Connect to Existing Azure AI Foundry Virtual Agent")
    print("="*70)
    
    print(f"\n🧠 Connecting to agent: {AGENT_ID}")
    
    async with AzureCliCredential() as credential:
        async with AgentsClient(
            endpoint=PROJECT_ENDPOINT,
            credential=credential
        ) as agents_client:
            
            # Verify the agent exists
            agent = await agents_client.get_agent(agent_id=AGENT_ID)
            print(f"✅ Connected successfully to: {agent.name}")
            
            print("\n" + "="*70)
            print("💬 Interactive Chat (Type 'quit' to exit)")
            print("="*70 + "\n")
            
            thread_id = None
            
            while True:
                # Get user input
                user_input = input("You: ")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n🤝 Thank You!")
                    break
                
                if not user_input.strip():
                    continue
                
                print("Agent: ", end="", flush=True)
                
                if thread_id is None:
                    # First message - create thread and run
                    run = await agents_client.create_thread_and_run(
                        agent_id=AGENT_ID,
                        thread={"messages": [{"role": "user", "content": user_input}]}
                    )
                    thread_id = run.thread_id
                    
                    # Wait for completion
                    while run.status in ["queued", "in_progress"]:
                        await asyncio.sleep(0.5)
                        run = await agents_client.runs.get(thread_id=thread_id, run_id=run.id)
                    
                    # Get the assistant's last response
                    response = await agents_client.messages.get_last_message_text_by_role(
                        thread_id=thread_id,
                        role="assistant"
                    )
                    if hasattr(response, 'text') and hasattr(response.text, 'value'):
                        print(response.text.value)
                    else:
                        print(response)
                else:
                    # Subsequent messages - add to existing thread
                    await agents_client.messages.create(
                        thread_id=thread_id,
                        role="user",
                        content=user_input
                    )
                    run = await agents_client.runs.create(
                        thread_id=thread_id,
                        agent_id=AGENT_ID
                    )
                    
                    # Wait for completion
                    while run.status in ["queued", "in_progress"]:
                        await asyncio.sleep(0.5)
                        run = await agents_client.runs.get(thread_id=thread_id, run_id=run.id)
                    
                    # Get the assistant's last response
                    response = await agents_client.messages.get_last_message_text_by_role(
                        thread_id=thread_id,
                        role="assistant"
                    )
                    if hasattr(response, 'text') and hasattr(response.text, 'value'):
                        print(response.text.value)
                    else:
                        print(response)
                print()


if __name__ == "__main__":
    asyncio.run(main())
