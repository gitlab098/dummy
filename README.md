# Customer Support Agentic AI Workflow

**Built with AWS Strands Agents SDK using "Agents as Tools" Pattern**

An intelligent, multi-agent customer support system that automatically analyzes, routes, and resolves customer inquiries using AI agents powered by Amazon Bedrock and AWS Strands Agents framework.

✨ **Features the "Agents as Tools" pattern** - specialist agents are exposed as tools to an orchestrator agent, enabling model-driven routing decisions.

## 🎯 Overview

This project demonstrates a production-ready agentic AI workflow for customer support automation using AWS Strands Agents SDK. The system uses multiple specialized AI agents that collaborate to provide intelligent customer support at scale.

### Use Case: Automated Customer Support

The workflow handles:
- **Technical Support**: Troubleshooting, error resolution, performance issues
- **Billing Support**: Payment inquiries, refunds, subscription management
- **Product Information**: Feature questions, integrations, best practices
- **Escalation Management**: Automatic detection of cases requiring human intervention

## 🏗️ Architecture - "Agents as Tools" Pattern

```
                    Customer Inquiry
                           ↓
        ┌─────────────────────────────────┐
        │  Orchestrator Agent             │
        │  (Model-driven routing)         │
        └──────────┬──────────────────────┘
                   │
                   │ Has access to tools:
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
   [Analysis Tools]    [Specialist Agents as Tools]
        │                     │
        ├─ analyze_sentiment  ├─ technical_support_agent() ← Agent as Tool!
        ├─ determine_urgency  ├─ billing_support_agent()   ← Agent as Tool!
        ├─ classify_intent    └─ product_information_agent() ← Agent as Tool!
        └─ check_escalation
                   │
                   ▼
        Model decides which tools to invoke
                   │
                   ▼
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
  [Analysis]         [Specialist Agent]
                            │
                            ├─ Has own tools (KB search)
                            ├─ Domain expertise
                            └─ Returns resolution
                   │
                   ▼
            [Final Response]
```

**Key Innovation**: The orchestrator is itself an Agent that has specialist agents available as tools. The model intelligently decides which specialist to invoke - no manual routing logic!

## ✨ Key Features

### "Agents as Tools" Pattern ⭐
- **Specialist Agents as Tools**: Each specialist agent (Technical, Billing, Product) is exposed as a tool using the `@tool` decorator
- **Model-Driven Routing**: The orchestrator agent decides which specialist to invoke based on the inquiry - no manual routing code!
- **Intelligent Decision Making**: The LLM analyzes the query and chooses the appropriate specialist agent(s)
- **Composable Architecture**: Easy to add new specialist agents - just add them as tools

### Multi-Agent Orchestration
- **Orchestrator Agent**: Main agent with access to all analysis tools and specialist agents
- **Analysis Tools**: Sentiment, urgency, intent classification, escalation detection
- **Specialist Agents**: Domain-specific expertise (Technical, Billing, Product) - each is itself an Agent with its own tools
- **Collaborative Resolution**: Can invoke multiple specialists for complex inquiries

### Built with AWS Strands Agents SDK
- **Model-Driven Approach**: Simple, declarative agent definitions
- **Tool Integration**: Custom tools using `@tool` decorator
- **Agent Composition**: Agents can use other agents as tools
- **Amazon Bedrock**: Powered by Claude 3.5 Sonnet
- **Streaming Support**: Real-time response generation
- **Production-Ready**: Battle-tested framework used by AWS teams

### Knowledge Base Integration
- Technical troubleshooting articles
- Billing policies and procedures
- Product documentation and guides
- Simulated KB (easily replaceable with real vector DB)

## 📋 Prerequisites

- Python 3.10 or later
- AWS Account with access to Amazon Bedrock
- AWS CLI configured with credentials
- Bedrock model access: `anthropic.claude-3-5-sonnet-20241022-v2:0`

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd dummy
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-west-2)
```

### 5. Verify Setup

```bash
python examples/simple_test.py
```

## 📖 Usage

### Quick Start

```python
from orchestrator import handle_customer_inquiry

# Process a customer inquiry
result = handle_customer_inquiry(
    message="I'm getting a 500 error when calling the API",
    customer_id="CUST-12345"
)

print(f"Status: {result['status']}")
print(f"Resolution: {result['resolution']}")
```

### Using the Orchestrator

```python
from orchestrator import CustomerSupportOrchestrator

# Create orchestrator instance
orchestrator = CustomerSupportOrchestrator(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    region="us-west-2",
    enable_logging=True
)

# Process inquiry
result = orchestrator.process_inquiry(
    customer_message="How do I set up Salesforce integration?",
    customer_id="CUST-67890"
)

print(f"Workflow ID: {result['workflow_id']}")
print(f"Classification: {result['classification']}")
print(f"Resolution: {result['resolution']}")
```

### Streaming Responses

```python
# Stream workflow updates
for update in orchestrator.process_inquiry_streaming(message, customer_id):
    print(f"Update: {update['type']} - {update.get('status', '')}")
```

### Using Specialist Agents Directly

```python
from agents.specialist_agents import (
    technical_support_agent,
    billing_support_agent,
    product_information_agent
)

# Call specialist agent tools directly
response = technical_support_agent("My app keeps crashing")
# Note: Usually the orchestrator agent decides which to call,
# but you can invoke them directly for testing
```

### Creating Custom Tools

```python
from strands import tool

@tool
def check_account_status(customer_id: str) -> dict:
    """
    Check the account status for a customer.

    Args:
        customer_id: The customer's unique identifier

    Returns:
        Dictionary with account information
    """
    # Your implementation here
    return {
        "status": "active",
        "tier": "premium",
        "support_level": "priority"
    }

# Add to agent
from strands import Agent

agent = Agent(tools=[check_account_status])
response = agent("What's the status of account CUST-123?")
```

## 📂 Project Structure

```
dummy/
├── README.md                      # This file
├── requirements.txt               # Python dependencies (Strands Agents SDK)
├── .gitignore
│
├── tools/                         # @tool decorated functions
│   ├── customer_analysis.py       # Analysis tools (sentiment, urgency, intent)
│   └── knowledge_base.py          # KB search tools
│
├── agents/
│   └── specialist_agents.py       # Specialist agents exposed as @tools
│                                  # - technical_support_agent()
│                                  # - billing_support_agent()
│                                  # - product_information_agent()
│
├── orchestrator.py                # Orchestrator Agent (uses agents as tools)
│
└── examples/
    ├── simple_test.py             # Setup verification
    └── basic_usage.py             # "Agents as Tools" examples
```

## 🎓 Understanding "Agents as Tools"

### What is This Pattern?

The "Agents as Tools" pattern is a key multi-agent orchestration primitive in AWS Strands Agents SDK that allows you to:

1. **Create Specialist Agents** - Build focused agents with domain expertise
2. **Expose as Tools** - Wrap agents using `@tool` decorator
3. **Model-Driven Routing** - Let the LLM decide which agent to invoke

### Code Example

```python
# Step 1: Create a specialist agent
technical_agent = Agent(
    model=BedrockModel(...),
    tools=[search_technical_kb],
    system="You are a technical support specialist..."
)

# Step 2: Expose the agent as a tool
@tool
def technical_support_agent(customer_inquiry: str) -> str:
    """Handles technical issues and troubleshooting."""
    return technical_agent(customer_inquiry)

# Step 3: Orchestrator agent uses it as a tool
orchestrator = Agent(
    tools=[
        analyze_sentiment,
        technical_support_agent,  # ← Agent as a tool!
        billing_support_agent,    # ← Agent as a tool!
    ],
    system="Route inquiries to the appropriate specialist agent..."
)

# The model decides which tool/agent to invoke
response = orchestrator("I'm getting API errors")
# ↑ Model will likely invoke technical_support_agent()
```

### Benefits

✅ **No Manual Routing** - Model intelligence drives decisions
✅ **Declarative Code** - Simple, maintainable architecture
✅ **Easy to Extend** - Add new specialists by adding tools
✅ **Agent Collaboration** - Multiple agents can work together
✅ **Production-Ready** - Pattern used by AWS teams

## 🎓 Examples

Run the comprehensive examples:

```bash
python examples/basic_usage.py
```

This demonstrates:
1. ✅ Technical support inquiry → model invokes `technical_support_agent()`
2. ✅ Billing inquiry → model invokes `billing_support_agent()`
3. ✅ Product question → model invokes `product_information_agent()`
4. ✅ Multi-agent scenario → model may invoke multiple specialist agents
5. ✅ Streaming workflow → real-time agent tool calls
6. ✅ Intelligent routing → model-driven routing decisions
7. ✅ Pattern explanation → detailed "Agents as Tools" walkthrough

## 🔧 Configuration

### Model Configuration

Change the Bedrock model in `orchestrator.py`:

```python
orchestrator = CustomerSupportOrchestrator(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",  # Change model
    region="us-west-2",                                      # Change region
)
```

### Agent Customization

Modify agent system prompts in `agents/`:

```python
self.agent = Agent(
    model=self.model,
    tools=[...],
    system="""Your custom system prompt here"""
)
```

### Knowledge Base Integration

Replace simulated KB in `tools/knowledge_base.py` with real vector DB:

```python
@tool
def search_technical_kb(query: str) -> List[Dict[str, str]]:
    # Replace with your vector DB query
    # Example: OpenSearch, Pinecone, Weaviate, etc.
    results = vector_db.search(query, k=3)
    return results
```

## 🎯 Workflow Details - "Agents as Tools" Execution

### 1. Customer Inquiry Received

The orchestrator agent receives the customer message and begins processing.

### 2. Analysis Phase (Model-Driven)

The orchestrator agent has access to analysis tools and **decides** which to use:
- `analyze_sentiment()` - Detects: POSITIVE, NEUTRAL, NEGATIVE, FRUSTRATED
- `determine_urgency()` - Classifies: CRITICAL, HIGH, MEDIUM, LOW
- `classify_intent()` - Identifies: TECHNICAL, BILLING, PRODUCT_INFO, GENERAL
- `check_escalation_needed()` - Flags critical cases

**Key Point**: The model determines which analysis tools to invoke and in what order.

### 3. Intelligent Routing (Model-Driven)

Based on its analysis, the orchestrator agent **chooses** which specialist agent to invoke:
- `technical_support_agent()` - For technical issues, errors, bugs
- `billing_support_agent()` - For payments, refunds, subscriptions
- `product_information_agent()` - For features, capabilities, integrations

**Key Point**: No manual routing code! The model reads tool descriptions and decides which specialist agent to call. It can even invoke multiple specialists for complex inquiries.

### 4. Specialist Resolution

Each specialist agent (which is itself an Agent with tools):
- Searches relevant knowledge base using its own tools
- Applies domain-specific expertise
- Returns actionable resolution steps
- Includes KB article references

### 5. Final Response

The orchestrator synthesizes the specialist's response and returns it to the customer.

### 6. Escalation Handling

Automatic escalation triggered by:
- Critical urgency keywords (emergency, critical, urgent)
- Legal keywords (lawsuit, attorney, legal)
- Security keywords (breach, fraud, security incident)
- Frustrated sentiment + high urgency combination

**Architecture Advantage**: Adding new specialists is as simple as creating a new agent and exposing it as a tool!

## 🚀 Production Deployment

### AWS Lambda Deployment

Each agent can be deployed as a separate Lambda function:

```python
# lambda_handler.py
from orchestrator import handle_customer_inquiry
import json

def lambda_handler(event, context):
    message = event['body']['message']
    customer_id = event['body'].get('customer_id')

    result = handle_customer_inquiry(message, customer_id)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

### API Gateway Integration

Expose via REST API:
```
POST /support/inquiry
{
  "message": "Customer message here",
  "customer_id": "CUST-12345"
}
```

### Step Functions Workflow

Orchestrate with AWS Step Functions for:
- Durable execution
- Error handling and retries
- State management
- Audit logging

## 📊 Performance Considerations

- **Agent Caching**: Specialist agents are cached and reused
- **Parallel Processing**: Multiple inquiries can be processed concurrently
- **Streaming**: Enables real-time user experience
- **Bedrock Optimization**: Uses latest Claude models for best performance

## 🔐 Security Best Practices

1. **IAM Roles**: Use IAM roles for Bedrock access, not access keys
2. **Secrets**: Store API keys in AWS Secrets Manager
3. **Logging**: Enable CloudWatch logs for audit trail
4. **Input Validation**: Sanitize customer inputs
5. **Rate Limiting**: Implement rate limits on API endpoints

## 📈 Monitoring & Observability

### Logging

The orchestrator includes built-in logging:

```python
orchestrator = CustomerSupportOrchestrator(enable_logging=True)
```

### CloudWatch Integration

```python
import logging
import watchtower

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

### Metrics to Track

- Inquiry volume by intent type
- Average resolution time
- Escalation rate
- Customer sentiment distribution
- Agent success rate

## 🧪 Testing

```bash
# Run setup verification
python examples/simple_test.py

# Run examples
python examples/basic_usage.py

# Test individual components
python -c "from tools.customer_analysis import analyze_sentiment; print(analyze_sentiment('This is great!'))"
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

Apache 2.0 License

## 🔗 Resources

- [AWS Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [AWS Prescriptive Guidance - Agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/)

## 💡 Use Case Extensions

This workflow can be extended for:
- **Sales Support**: Lead qualification, product recommendations
- **IT Helpdesk**: Ticket triage, incident management
- **HR Support**: Employee inquiries, policy questions
- **E-commerce**: Order tracking, returns, product questions
- **Healthcare**: Appointment scheduling, symptom assessment
- **Finance**: Account inquiries, transaction support

## 🎉 Acknowledgments

Built with:
- **AWS Strands Agents SDK** - Simplifying AI agent development
- **Amazon Bedrock** - Managed foundation model service
- **Claude 3.5 Sonnet** - Advanced language model by Anthropic

---

**Questions or Issues?**
Open an issue or reach out to the team.

**Ready to deploy?**
Check out the production deployment guide in `/docs/deployment.md`
