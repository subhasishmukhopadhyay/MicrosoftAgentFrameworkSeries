# 📘 Azure AI Agent Framework - Common Guide

A comprehensive reference guide covering common topics, best practices, and troubleshooting for all three demo scenarios.

---

## 📊 Comparison: Three Approaches

This project demonstrates three different ways to build AI agents with Azure:

| Feature | Demo 01 | Demo 02 | Demo 03 |
|---------|---------|---------|---------|
| **Purpose** | Create new agent | Use existing agent | Direct chat (no agent) |
| **Service** | Azure AI Foundry | Azure AI Foundry | Azure OpenAI |
| **Persistence** | ✅ Creates new agent | ✅ Uses existing agent | ❌ Session only |
| **Authentication** | Azure CLI | Azure CLI | API Key |
| **Setup Complexity** | Medium | Low | Low |
| **Best For** | Initial setup | Production | Prototyping |
| **Script Name** | `01_create_agent_aifoundry.py` | `02_use_existing_agent_from_aifoundry.py` | `03_direct_chat_with_azure_openai.py` |
| **Environment File** | `.env01` | `.env02` | `.env03` |
| **Requires az login** | ✅ Yes | ✅ Yes | ❌ No |

### When to Use Each Approach

#### 🆕 Demo 01: Create Agent in AI Foundry
- **Use when:** Setting up a new project or creating specialized agents
- **Benefits:** Full AI Foundry features, persistent agents, team collaboration
- **Trade-offs:** Requires Azure CLI authentication, creates resources in cloud

#### 🔄 Demo 02: Use Existing Agent
- **Use when:** Production applications, reusing trained agents
- **Benefits:** No duplicate agents, consistent behavior, cost-effective
- **Trade-offs:** Requires existing agent ID

#### ⚡ Demo 03: Direct Azure OpenAI
- **Use when:** Quick prototyping, testing, simple chat scenarios
- **Benefits:** No agent management, API key auth, lightweight
- **Trade-offs:** No persistence, no AI Foundry features

---

## 🔒 Security Best Practices

### Environment Variables

1. **Never hardcode credentials** – Always use environment variables
   ```python
   # ❌ Bad
   API_KEY = "sk-abc123..."
   
   # ✅ Good
   API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
   ```

2. **Use separate environment files** – Each demo has its own `.env` file
   - `.env01` - AI Foundry endpoint
   - `.env02` - AI Foundry endpoint + Agent ID
   - `.env03` - Azure OpenAI endpoint + API Key

3. **Add to .gitignore** – Ensure all environment files are ignored
   ```gitignore
   .env*
   *.env
   ```

### API Key Management

| Practice | Description |
|----------|-------------|
| **Rotate regularly** | Change API keys every 90 days |
| **Use separate keys** | Different keys for dev/staging/prod |
| **Monitor usage** | Set up alerts for unusual activity |
| **Limit scope** | Use keys with minimum required permissions |

### Authentication Methods

| Method | Security Level | Use Case |
|--------|---------------|----------|
| **Managed Identity** | 🟢 Highest | Production on Azure |
| **Azure CLI** | 🟡 High | Development & testing |
| **API Key** | 🟠 Medium | Quick prototyping |
| **Hardcoded** | 🔴 Never | ❌ Never use |

### Recommended for Production

```python
from azure.identity import DefaultAzureCredential

# Uses managed identity in Azure, Azure CLI locally
credential = DefaultAzureCredential()
```

---

## 🔧 Troubleshooting

### Quick Reference Table

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `401 Unauthorized` | Invalid credentials | Check API key or run `az login` |
| `403 Forbidden` | Insufficient permissions | Verify RBAC roles |
| `404 Not Found` | Wrong endpoint or resource | See [Common 404 Error Issue](#-common-404-error-issue) |
| `429 Too Many Requests` | Rate limit exceeded | Wait and retry with backoff |
| `500 Internal Server Error` | Service issue | Retry later, check Azure status |
| `Connection refused` | Network issue | Check firewall, VPN settings |
| `Model not found` | Wrong deployment name | Verify deployment in Azure Portal |

### Authentication Issues

#### Azure CLI Authentication (Demo 01 & 02)

**Problem:** `DefaultAzureCredential failed`

**Solution:**
```powershell
# Login to Azure
az login

# Set correct subscription
az account set --subscription "Your Subscription Name"

# Verify
az account show
```

**Problem:** `Tenant mismatch` or wrong subscription

**Solution:**
```powershell
# List all subscriptions
az account list --output table

# Switch to correct subscription
az account set --subscription "subscription-id-or-name"
```

#### API Key Authentication (Demo 03)

**Problem:** `401 Unauthorized`

**Solution:**
1. Go to Azure Portal → Your Azure OpenAI resource
2. Navigate to **Keys and Endpoint**
3. Copy Key 1 or Key 2
4. Update `.env03` file

### Virtual Environment Issues

**Problem:** `Module not found` errors

**Solution:**
```powershell
# Ensure venv is activated (look for (.venv) in prompt)
cd c:\Demo\AzureAIFoundary
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem:** Wrong Python interpreter

**Solution:**
```powershell
# Use full path to venv Python
C:/Demo/AzureAIFoundary/.venv/Scripts/python.exe your_script.py
```

---

## 🔴 Common 404 Error Issue

### Understanding the Problem

A `404 Resource Not Found` error typically means you're using the **wrong endpoint URL**. This is especially common when confusing Azure AI Foundry with Azure OpenAI.

### Azure Endpoint Types

| Service | Endpoint Format | Used By |
|---------|-----------------|---------|
| **Azure AI Foundry** | `https://<resource>.services.ai.azure.com/api/projects/<project>` | Demo 01, Demo 02 |
| **Azure OpenAI** | `https://<resource>.openai.azure.com/` | Demo 03 |
| **GitHub Models** | `https://models.inference.ai.azure.com/` | Not in this project |

### Common Mistakes

#### ❌ Mistake 1: Using AI Foundry endpoint for Demo 03

```env
# Wrong for Demo 03
AZURE_OPENAI_ENDPOINT=https://a2ademo-resource.services.ai.azure.com/api/projects/a2ademo

# Correct for Demo 03
AZURE_OPENAI_ENDPOINT=https://a2ademo-resource.openai.azure.com/
```

#### ❌ Mistake 2: Using Azure OpenAI endpoint for Demo 01/02

```env
# Wrong for Demo 01/02
PROJECT_ENDPOINT=https://a2ademo-resource.openai.azure.com/

# Correct for Demo 01/02
PROJECT_ENDPOINT=https://a2ademo-resource.services.ai.azure.com/api/projects/a2ademo
```

### Finding the Correct Endpoint

#### For Demo 01 & 02 (Azure AI Foundry)

1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Select your project
3. Go to **Project Settings** → **Properties**
4. Copy the **Project endpoint**

#### For Demo 03 (Azure OpenAI)

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for **"Azure OpenAI"** (not AI Foundry)
3. Select your Azure OpenAI resource
4. Go to **Keys and Endpoint**
5. Copy the **Endpoint** URL

### Alternative: Use Azure CLI Auth for All Demos

If you don't have a separate Azure OpenAI resource, modify Demo 03 to use Azure CLI authentication:

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

---

## 🌐 Environment Setup Checklist

### Prerequisites

- [ ] Python 3.10+ installed
- [ ] Azure subscription active
- [ ] Azure CLI installed (`az --version`)
- [ ] VS Code with Python extension

### Project Setup

```powershell
# 1. Navigate to project
cd c:\Demo\AzureAIFoundary

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Azure login (for Demo 01 & 02)
az login
az account set --subscription "Your Subscription"
```

### Environment Files Checklist

#### .env01 (Demo 01)
- [ ] `PROJECT_ENDPOINT` - AI Foundry project endpoint
- [ ] `MODEL_DEPLOYMENT_NAME` - Model deployment name

#### .env02 (Demo 02)
- [ ] `PROJECT_ENDPOINT` - AI Foundry project endpoint
- [ ] `MODEL_DEPLOYMENT_NAME` - Model deployment name
- [ ] `AGENT_ID` - Existing agent ID from Demo 01

#### .env03 (Demo 03)
- [ ] `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint (*.openai.azure.com)
- [ ] `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` - Deployment name
- [ ] `AZURE_OPENAI_API_KEY` - API key
- [ ] `AZURE_OPENAI_API_VERSION` - API version (e.g., 2024-11-20)

---

## 💡 Pro Tips

### Performance

1. **Reuse clients** – Don't create new clients for each request
2. **Use streaming** – For real-time responses in chat scenarios
3. **Batch requests** – When possible, combine multiple operations

### Development

1. **Start with Demo 03** – Quickest way to test your setup
2. **Use Demo 01** – Once verified, create persistent agents
3. **Use Demo 02** – For production with existing agents

### Debugging

1. **Enable logging** – Add verbose logging during development
2. **Check diagnostics** – Use SDK diagnostic strings for troubleshooting
3. **Monitor costs** – Set up Azure cost alerts

---

## 📚 Additional Resources

### Documentation
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)

### SDKs
- [azure-ai-agents (PyPI)](https://pypi.org/project/azure-ai-agents/)
- [openai (PyPI)](https://pypi.org/project/openai/)
- [azure-identity (PyPI)](https://pypi.org/project/azure-identity/)

### Support
- [Azure Status Page](https://status.azure.com/)
- [Stack Overflow - Azure AI](https://stackoverflow.com/questions/tagged/azure-ai)
- [Microsoft Q&A](https://learn.microsoft.com/answers/)

---

**📝 Last Updated:** December 2024
