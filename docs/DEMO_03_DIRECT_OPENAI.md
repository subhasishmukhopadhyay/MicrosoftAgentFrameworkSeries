# ⚡ Demo 03: Direct Azure OpenAI Chat

## Overview

This demo shows you how to use **Azure OpenAI directly** without the Azure AI Foundry Agent Service. The chat session created here is **temporary** – it exists only for the duration of your session and is not saved to the cloud.

This approach is perfect for quick prototyping and scenarios where persistence isn't needed.

---

## 🎯 What You'll Learn

- How to connect directly to Azure OpenAI using the `openai` SDK
- Understanding the difference between persistent agents and session-only chat
- Using API key authentication
- Building lightweight chat applications with conversation history
- Streaming responses for real-time output

---

## 🔄 When to Use This Approach

| Use Direct Azure OpenAI When... | Use Azure AI Foundry Agents When... |
|--------------------------------|-------------------------------------|
| Quick prototyping | Production applications |
| No persistence needed | Agent reuse required |
| Simple chat scenarios | Complex agent workflows |
| Testing models | Team collaboration |
| Cost-conscious development | Enterprise features needed |

---

## ⚙️ Configuration

### Step 1: Get Your Azure OpenAI Details

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your **Azure OpenAI** resource
3. Go to **Keys and Endpoint**
4. Copy:
   - **Endpoint** (e.g., `https://your-resource.openai.azure.com/`)
   - **API Key** (Key 1 or Key 2)
5. Go to **Model Deployments** → Copy your **Deployment Name**

### Step 2: Update Environment File

Edit the `src/.env03` file:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_KEY=your-actual-api-key-here
AZURE_OPENAI_API_VERSION=2024-11-20
```

⚠️ **Security Note:** Never commit API keys to version control!

> **Important:** Make sure the endpoint matches your actual Azure OpenAI resource. The resource name in the URL must be correct (e.g., `your-resource` in `https://your-resource.openai.azure.com/`).

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

Or install the OpenAI package directly:
```bash
pip install openai python-dotenv
```

### Step 4: Run the Script

**Option A: From the src directory**
```bash
cd src
python 03_direct_chat_with_azure_openai.py
```

**Option B: Using full Python path**
```powershell
cd c:\Demo\AzureAIFoundary\src
C:/Demo/AzureAIFoundary/.venv/Scripts/python.exe 03_direct_chat_with_azure_openai.py
```

**Note:** No `az login` required – this demo uses API key authentication!

---

## 💬 Expected Output

```
======================================================================
🤖✨ DEMO: Direct Azure OpenAI Chat (API Key Auth)
======================================================================

✅ Client created (temporary session, not saved to cloud)

======================================================================
💬 Interactive Chat (Type 'quit' to exit)
======================================================================

You: What's the capital of France?
Agent: The capital of France is Paris.

You: Tell me a fun fact about it.
Agent: The Eiffel Tower was originally intended to be a temporary installation 
       for the 1889 World's Fair and was almost demolished in 1909, but was 
       saved because of its usefulness as a radio transmission tower!

You: exit

🤝 Thank You!
```

---

## 📝 Key Code Explanation

### Imports and Setup

```python
from openai import AzureOpenAI

# Load environment variables
load_dotenv('.env03')

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-11-20")
```

### Creating the Azure OpenAI Client

```python
# Create Azure OpenAI client using API Key
client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)
```

This code:
1. **Connects directly to Azure OpenAI** (bypasses AI Foundry Agent Service)
2. **Uses API key authentication** (no Azure CLI needed)
3. **Creates a client** for chat completions
4. **Session is NOT saved** to any cloud service

### Managing Conversation History

```python
# Maintain conversation history
messages = [
    {"role": "system", "content": "You are a helpful assistant. Be concise and clear."}
]

# Add user message
messages.append({"role": "user", "content": user_input})

# Get streaming response
response = client.chat.completions.create(
    model=DEPLOYMENT,
    messages=messages,
    stream=True
)

# Add assistant response to history
messages.append({"role": "assistant", "content": assistant_response})
```

---

## 📊 Comparison: Three Approaches

| Feature | Demo 01 | Demo 02 | Demo 03 |
|---------|---------|---------|---------|
| **Service** | AI Foundry | AI Foundry | Direct OpenAI |
| **Persistence** | ✅ Creates new agent | ✅ Uses existing agent | ❌ Session only |
| **Authentication** | Azure CLI | Azure CLI | API Key |
| **Setup Complexity** | Medium | Low | Low |
| **Best For** | Initial setup | Production | Prototyping |
| **Script Name** | `01_create_agent_aifoundry.py` | `02_use_existing_agent_from_aifoundry.py` | `03_direct_chat_with_azure_openai.py` |

---

## 🔒 Security Best Practices

1. **Never hardcode API keys** – Always use environment variables
2. **Use .gitignore** – Ensure `.env03` is in your `.gitignore`
3. **Rotate keys regularly** – Change API keys periodically
4. **Consider managed identity** – For production, use Azure CLI auth

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Check API key is correct and belongs to this resource |
| `404 Not Found` | See detailed explanation below |
| `Model not found` | Check deployment name matches exactly in Azure Portal |
| `Rate limited` | Wait and retry, or upgrade tier |
| `Connection refused` | Verify network connectivity and firewall rules |

### 🔴 Common 404 Error Issue

If you receive a `404 Resource Not Found` error, the most common cause is using the **wrong endpoint URL**.

**Important:** Azure AI Foundry and Azure OpenAI use **different endpoints**:

| Service | Endpoint Format |
|---------|-----------------|
| **Azure AI Foundry** | `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| **Azure OpenAI** | `https://<resource>.openai.azure.com/` |

**This demo requires the Azure OpenAI endpoint** (the `*.openai.azure.com` format).

**To find your correct endpoint:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Azure OpenAI" resources (not AI Foundry)
3. Select your Azure OpenAI resource
4. Go to **Keys and Endpoint**
5. Copy the endpoint URL

**Alternative: Use Azure CLI Authentication**

If you don't have a separate Azure OpenAI resource, you can modify the code to use Azure CLI credentials instead:

```python
from openai import AzureOpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider

# Use Azure CLI credential instead of API key
credential = AzureCliCredential()
token_provider = get_bearer_token_provider(
    credential, 
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=ENDPOINT,  # Can use AI Foundry endpoint
    azure_ad_token_provider=token_provider,
    api_version=API_VERSION
)
```

This approach works with Azure AI Foundry endpoints and doesn't require a separate API key

---

## 💡 Pro Tips

1. **API Version Matters** – Use the latest stable version for new features
2. **Streaming** – This demo uses streaming for real-time responses
3. **Error Handling** – Add try-catch in production code
4. **Logging** – Consider adding logging for debugging

---

## ➡️ Next Steps

You've completed all three demos! Here's what to explore next:

- 🔧 **Add Tools** – Give your agents capabilities like web search
- 🧠 **RAG** – Implement Retrieval Augmented Generation
- 🔗 **Multi-Agent** – Build systems with multiple specialized agents
- 📊 **Evaluation** – Add tracing and evaluation to your agents

---

**🎉 Congratulations!** You've mastered three ways to build AI agents with Azure!

---

## 📚 Additional Resources

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
