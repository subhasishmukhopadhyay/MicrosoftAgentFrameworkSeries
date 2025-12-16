# 🔗 Demo 02: Use Existing Azure AI Foundry Agent

## Overview

This demo shows you how to **connect to an existing AI agent** that was previously created in Azure AI Foundry. This is perfect for scenarios where you want to reuse agents across multiple sessions or applications.

---

## 🎯 What You'll Learn

- How to connect to an existing agent using its ID
- How to use the `azure-ai-agents` SDK to retrieve and use agents
- Understanding persistent agent benefits
- Building applications with reusable agents
- Creating conversation threads with existing agents

---

## 📋 Prerequisites

Before running this demo, you need:

1. ✅ An existing agent in Azure AI Foundry
   - Either created through Demo 01, or
   - Created manually in the Azure AI Foundry portal
2. ✅ The **Agent ID** (e.g., `asst_XImpDvpbEADxhkr7m670zkLB`)
3. ✅ Azure CLI logged in to the correct subscription

---

## ⚙️ Configuration

### Step 1: Get Your Agent ID

If you ran Demo 01, you should have noted the Agent ID from the output:
```
✅ Agent created successfully!
   Agent ID: asst_XImpDvpbEADxhkr7m670zkLB  <-- This is your Agent ID
```

Alternatively, find existing agents in Azure AI Foundry Portal:
1. Go to [Azure AI Foundry Portal](https://ai.azure.com)
2. Navigate to your project → **Agents**
3. Click on your agent to view its ID

### Step 2: Update Environment File

Edit the `src/.env02` file:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_AI_AGENT_ID=asst_XImpDvpbEADxhkr7m670zkLB
```

Replace with your actual endpoint and agent ID.

### Step 3: Ensure Correct Azure Subscription

Make sure you're logged into the Azure subscription that contains your AI Foundry resource:

```bash
az account list --output table
az account set --subscription "Your-Subscription-Name"
```

---

## 🚀 Running the Demo

### Step 1: Create and Configure Virtual Environment

If you haven't set up the virtual environment yet:

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

```bash
pip install -r requirements.txt
```

### Step 4: Login to Azure (if not already)

```bash
az login
```

### Step 5: Run the Script

**Option A: From the src directory**
```bash
cd src
python 02_use_existing_agent_from_aifoundry.py
```

**Option B: Using full Python path**
```powershell
cd c:\Demo\AzureAIFoundary\src
C:/Demo/AzureAIFoundary/.venv/Scripts/python.exe 02_use_existing_agent_from_aifoundry.py
```

---

## 💬 Expected Output

```
======================================================================
🔗✨ DEMO: Connect to Existing Azure AI Foundry Virtual Agent
======================================================================

🧠 Connecting to agent: asst_XImpDvpbEADxhkr7m670zkLB
✅ Connected successfully to: 01_Create_Agent_AiFoundry-DemoAgent

======================================================================
💬 Interactive Chat (Type 'quit' to exit)
======================================================================

You: What can you help me with?
Agent: I'm a helpful AI assistant! I can answer questions, help with tasks, 
       provide explanations, and assist with various topics. How can I help 
       you today?

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
load_dotenv('.env02')

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AI_AGENT_ID")
```

### Connecting to Existing Agent

```python
async with AzureCliCredential() as credential:
    async with AgentsClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential
    ) as agents_client:
        
        # Verify the agent exists
        agent = await agents_client.get_agent(agent_id=AGENT_ID)
        print(f"✅ Connected successfully to: {agent.name}")
```

This code:
1. **Uses Azure CLI credentials** for authentication
2. **Creates an AgentsClient** connected to your Azure AI Foundry project
3. **Retrieves the existing agent** using `get_agent()` to verify it exists
4. **Does NOT create a new agent** – reuses what already exists

### Creating Conversation Thread

```python
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

# Get the assistant's response
response = await agents_client.messages.get_last_message_text_by_role(
    thread_id=thread_id,
    role="assistant"
)
```

---

## 🔄 Key Differences from Demo 01

| Aspect | Demo 01 | Demo 02 |
|--------|---------|---------|
| Agent Creation | Creates new agent | Uses existing agent |
| Agent ID | Generated new | Must be provided in `.env02` |
| Use Case | Initial setup | Production apps |
| Idempotent | No (creates each run) | Yes (same agent) |
| Script Name | `01_create_agent_aifoundry.py` | `02_use_existing_agent_from_aifoundry.py` |

---

## 💡 Use Cases

**Why use existing agents?**

1. **Cost Efficiency** – Don't recreate agents unnecessarily
2. **Consistency** – Same agent behavior across sessions
3. **Production Apps** – Connect deployed apps to centralized agents
4. **Team Collaboration** – Multiple team members using same agent
5. **Testing** – Consistent agent for QA testing

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Agent not found` | Verify the Agent ID is correct in `.env02` |
| `AuthenticationError` | Run `az login` with correct subscription |
| `Tenant does not match` | Switch subscription: `az account set --subscription "name"` |
| `Permission denied` | Ensure you have access to the Azure AI project |
| `DNS resolution failed` | Check endpoint URL and network connectivity |

---

## ➡️ Next Steps

To explore a simpler approach without persistent agents, check out [Demo 03: Direct Azure OpenAI Chat](DEMO_03_DIRECT_OPENAI.md).

---

**🎉 Great job!** You've learned how to connect to existing Azure AI Foundry agents!
