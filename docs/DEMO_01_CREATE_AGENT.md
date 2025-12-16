# 🤖 Demo 01: Create Azure AI Foundry Agent

## Overview

This demo shows you how to **create a brand new AI agent** in Azure AI Foundry and have an interactive conversation with it. The agent you create is **persistent** – it gets saved to your Azure AI Foundry service and can be reused later.

---

## 🎯 What You'll Learn

- How to connect to Azure AI Foundry using Azure CLI credentials
- How to use the `azure-ai-agents` SDK to create agents
- How to create conversation threads and process messages
- How to have interactive conversations with your agent
- Understanding the agent lifecycle

---

## ⚙️ Configuration

### Step 1: Get Your Azure AI Foundry Details

1. Go to [Azure AI Foundry Portal](https://ai.azure.com)
2. Navigate to your project
3. Copy your **Project Endpoint** (looks like `https://your-resource.services.ai.azure.com/api/projects/your-project`)
4. Note your **Model Deployment Name** (e.g., `gpt-4o`, `gpt-35-turbo`)

### Step 2: Update Environment File

Edit the `src/.env01` file:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

### Step 3: Ensure Correct Azure Subscription

Make sure you're logged into the Azure subscription that contains your AI Foundry resource:

```bash
az account list --output table
az account set --subscription "Your-Subscription-Name"
```

---

## 🚀 Running the Demo

### Step 1: Create and Configure Virtual Environment

If you haven't set up the virtual environment yet, create it first:

```bash
# Navigate to project root
cd c:\Demo\AzureAIFoundary

# Create virtual environment (one-time setup)
python -m venv .venv
```

### Step 2: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
cd c:\Demo\AzureAIFoundary
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
cd c:\Demo\AzureAIFoundary
.\.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
cd /path/to/AzureAIFoundary
source .venv/bin/activate
```

> 💡 **Tip:** You'll know the virtual environment is active when you see `(.venv)` at the beginning of your terminal prompt.

### Step 3: Install Dependencies

Install required packages (one-time setup or when dependencies change):

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install azure-ai-agents azure-identity python-dotenv aiohttp azure-core
```

### Step 4: Login to Azure

```bash
az login
```

Make sure you're logged into the correct subscription that has access to your Azure AI Foundry project.

### Step 5: Run the Script

**Option A: From the src directory**
```bash
cd src
python 01_create_agent_aifoundry.py
```

**Option B: Using full Python path (if virtual environment activation has issues)**
```powershell
cd c:\Demo\AzureAIFoundary\src
C:/Demo/AzureAIFoundary/.venv/Scripts/python.exe 01_create_agent_aifoundry.py
```

---

## 💬 Expected Output

```
======================================================================
🤖 DEMO: Create Azure AI Foundry Agent (Interactive)
======================================================================

📋 Creating a new agent in Azure AI Foundry...
✅ Agent created successfully!
   Agent ID: asst_9XH1ilIRf3jbufwxf9s9PgkE

======================================================================
💬 Interactive Chat (Type 'quit' to exit)
======================================================================

You: what is azure open AI?
Agent: Azure OpenAI Service is a Microsoft service that provides access to OpenAI's 
       powerful AI models, like GPT, Codex, and DALL·E, through the Azure cloud 
       platform. It enables developers and organizations to integrate advanced AI 
       capabilities, such as natural language understanding, code generation, and 
       image creation, into their apps and workflows securely and at scale.

You: exit

🤝 Thank You!
```

---

## 📝 Key Code Explanation

### Imports and Setup

```python
from azure.identity.aio import AzureCliCredential
from azure.ai.agents.aio import AgentsClient

# Load environment variables
load_dotenv('.env01')

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
```

### Creating the Agent

```python
async with AgentsClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential
) as agents_client:
    
    created_agent = await agents_client.create_agent(
        model=MODEL_DEPLOYMENT,
        name="01_Create_Agent_AiFoundry-DemoAgent",
        instructions="You are a helpful AI assistant. Be concise and friendly."
    )
```

This code:
1. **Creates an AgentsClient** connected to your Azure AI Foundry project
2. **Creates a new agent** with the specified model and instructions
3. **Returns an agent object** with an ID that you can use later

### Creating Thread and Running Conversation

```python
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

# Get the assistant's response
response = await agents_client.messages.get_last_message_text_by_role(
    thread_id=thread_id,
    role="assistant"
)
```

---

## 🔑 Important Notes

1. **Save Your Agent ID!** – The agent ID printed after creation (e.g., `asst_9XH1ilIRf3jbufwxf9s9PgkE`) can be used in Demo 02 to reconnect
2. **Costs Apply** – Creating and using agents incurs Azure costs
3. **Agent Persists** – Unlike Demo 03, this agent is saved and can be reused
4. **Tenant Matching** – Ensure your Azure CLI is logged into the same tenant as your AI Foundry resource

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `AuthenticationError` | Run `az login` and ensure correct subscription |
| `Tenant does not match` | Switch subscription: `az account set --subscription "name"` |
| `Endpoint not found` | Verify `AZURE_AI_PROJECT_ENDPOINT` is correct |
| `Model not found` | Check `MODEL_DEPLOYMENT_NAME` matches your deployment |
| `DNS resolution failed` | Check endpoint URL and network connectivity |

---

## ➡️ Next Steps

After creating your agent, note the **Agent ID** and proceed to [Demo 02: Use Existing Agent](DEMO_02_USE_EXISTING_AGENT.md) to learn how to reconnect to it.

---

**🎉 Congratulations!** You've created your first Azure AI Foundry agent!
