# Customer Support Agentic AI Workflow

**Built with AWS Strands Agents SDK**

An intelligent, multi-agent customer support system that automatically analyzes, routes, and resolves customer inquiries using AI agents powered by Amazon Bedrock and AWS Strands Agents framework.

## 🎯 Overview

This project demonstrates a production-ready agentic AI workflow for customer support automation using AWS Strands Agents SDK. The system uses multiple specialized AI agents that collaborate to provide intelligent customer support at scale.

### Use Case: Automated Customer Support

The workflow handles:
- **Technical Support**: Troubleshooting, error resolution, performance issues
- **Billing Support**: Payment inquiries, refunds, subscription management
- **Product Information**: Feature questions, integrations, best practices
- **Escalation Management**: Automatic detection of cases requiring human intervention

## 🏗️ Architecture

```
Customer Inquiry
      ↓
┌─────────────────┐
│  Intake Agent   │  ← Analyzes & classifies inquiry
│                 │  ← Uses: sentiment, urgency, intent tools
└────────┬────────┘
         ↓
    [Classification]
         ↓
    ┌────┴────┐
    │ Router  │
    └────┬────┘
         ↓
    ┌────┴────────────────┬─────────────────┐
    ↓                     ↓                  ↓
┌──────────┐      ┌──────────┐      ┌──────────┐
│Technical │      │ Billing  │      │ Product  │
│ Support  │      │ Support  │      │   Info   │
│  Agent   │      │  Agent   │      │  Agent   │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     ↓                 ↓                  ↓
[KB Search]       [KB Search]        [KB Search]
     ↓                 ↓                  ↓
[Resolution]      [Resolution]        [Resolution]
     └─────────────────┴──────────────────┘
                       ↓
              [Final Response]
```

## ✨ Key Features

### Multi-Agent Orchestration
- **Intake Agent**: Analyzes customer sentiment, urgency, and intent
- **Specialist Agents**: Domain-specific expertise (Technical, Billing, Product)
- **Intelligent Routing**: Automatically routes to the right specialist
- **Escalation Detection**: Identifies cases requiring human intervention

### Built with AWS Strands Agents
- **Model-Driven Approach**: Simple, maintainable agent definitions
- **Tool Integration**: Custom tools using `@tool` decorator
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

### Using Individual Agents

```python
from agents.intake_agent import IntakeAgent
from agents.specialist_agents import TechnicalSupportAgent

# Intake agent
intake = IntakeAgent()
analysis = intake.analyze("My app keeps crashing")

# Technical support agent
tech_agent = TechnicalSupportAgent()
resolution = tech_agent.resolve("My app keeps crashing")
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
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── tools/                         # Reusable tools for agents
│   ├── customer_analysis.py       # Sentiment, urgency, intent tools
│   └── knowledge_base.py          # KB search tools
│
├── agents/                        # AI agent definitions
│   ├── intake_agent.py            # Initial analysis agent
│   └── specialist_agents.py       # Domain specialist agents
│
├── orchestrator.py                # Multi-agent orchestration
│
└── examples/                      # Usage examples
    ├── simple_test.py             # Setup verification
    └── basic_usage.py             # Comprehensive examples
```

## 🎓 Examples

Run the comprehensive examples:

```bash
python examples/basic_usage.py
```

This demonstrates:
1. ✅ Technical support inquiry
2. ✅ Billing inquiry with refund request
3. ✅ Product information question
4. ✅ Escalation scenario
5. ✅ Streaming workflow
6. ✅ Batch processing multiple inquiries

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

## 🎯 Workflow Details

### 1. Intake Agent Analysis

The intake agent uses specialized tools to analyze:
- **Sentiment**: POSITIVE, NEUTRAL, NEGATIVE, FRUSTRATED
- **Urgency**: CRITICAL, HIGH, MEDIUM, LOW
- **Intent**: TECHNICAL, BILLING, PRODUCT_INFO, GENERAL
- **Escalation**: Automatic detection of escalation needs

### 2. Intelligent Routing

Based on the intake analysis:
- **TECHNICAL** → Routes to Technical Support Agent
- **BILLING** → Routes to Billing Support Agent
- **PRODUCT_INFO** → Routes to Product Information Agent
- **GENERAL** → Routes to Product Information Agent (default)

### 3. Specialist Resolution

Each specialist agent:
- Searches relevant knowledge base
- Provides domain-specific expertise
- Returns actionable resolution steps
- Includes KB article references

### 4. Escalation Handling

Automatic escalation triggered by:
- Critical urgency keywords (emergency, critical, urgent)
- Legal keywords (lawsuit, attorney, legal)
- Security keywords (breach, fraud, security incident)
- Frustrated sentiment + high urgency combination

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
