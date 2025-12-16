"""
NEW 01: Create Azure AI Foundry Agent (Interactive Demo)

This is an INTERACTIVE demo where you can create a new agent in Azure AI Foundry
and chat with it in real-time.

The agent is persistent and will be saved to Azure AI Foundry service.

Please ensure you delete the agent from the Azure AI Foundry portal after running this demo
"""

import asyncio
import os
from dotenv import load_dotenv

from azure.identity.aio import AzureCliCredential
from azure.ai.agents.aio import AgentsClient

# Load environment variables
load_dotenv('.env01')

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")


async def main():
    """Interactive demo: Create agent and chat."""
    
    print("\n" + "="*70)
    print("🤖✨ DEMO: Create Azure AI Foundry Virtual Agent (Interactive)")
    print("="*70)
    
    async with AzureCliCredential() as credential:
        # Create the agents client for Azure AI Foundry
        async with AgentsClient(
            endpoint=PROJECT_ENDPOINT,
            credential=credential
        ) as agents_client:
            
            print("\n🧠 Creating a new virtual agent in Azure AI Foundry...")
            
            created_agent = await agents_client.create_agent(
                model=MODEL_DEPLOYMENT,
                name="01_Create_Agent_AiFoundry-DemoAgent",
                instructions="You are a helpful AI agent assistant. Please be concise and friendly."
            )
            
            print(f"✅ Agent created successfully!")
            print(f"   Agent ID: {created_agent.id}")
            
            print("\n" + "="*70)
            print("💬 Interactive Chat (Type 'quit' to exit)")
            print("="*70 + "\n")
            
            thread_id = None
            
            while True:
                # Get user input
                user_input = input("You: ")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n 🤝 Thank You!")
                    break
                
                if not user_input.strip():
                    continue
                
                print("Agent: ", end="", flush=True)
                
                if thread_id is None:
                    # First message - create thread and run
                    run = await agents_client.create_thread_and_run(
                        agent_id=created_agent.id,
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
                        agent_id=created_agent.id
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
