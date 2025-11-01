"""
Specialist Agents - Handle specific types of customer inquiries

Built using AWS Strands Agents SDK with "Agents as Tools" pattern
"""

from strands import Agent, tool
from strands.models import BedrockModel
from tools.knowledge_base import (
    search_technical_kb,
    search_billing_kb,
    search_product_kb
)


# Initialize specialist agents globally so they can be reused
_technical_agent = None
_billing_agent = None
_product_agent = None


def get_technical_agent(model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
    """Get or create the technical support agent"""
    global _technical_agent
    if _technical_agent is None:
        model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.7,
            streaming=False  # Set to False for tool usage
        )

        _technical_agent = Agent(
            model=model,
            tools=[search_technical_kb],
            system="""You are a Technical Support Specialist. Your role is to:

1. Diagnose technical issues based on customer descriptions
2. Search the knowledge base for relevant troubleshooting articles
3. Provide clear, step-by-step solutions
4. Explain technical concepts in customer-friendly language
5. Determine if the issue requires engineering escalation

Guidelines:
- Always search the knowledge base first
- Provide specific, actionable steps
- Be patient and thorough
- Reference KB article IDs when applicable
- If the issue is beyond standard troubleshooting, recommend escalation

Your goal is to resolve technical issues efficiently while maintaining excellent customer experience."""
        )
    return _technical_agent


def get_billing_agent(model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
    """Get or create the billing support agent"""
    global _billing_agent
    if _billing_agent is None:
        model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.5,
            streaming=False
        )

        _billing_agent = Agent(
            model=model,
            tools=[search_billing_kb],
            system="""You are a Billing Support Specialist. Your role is to:

1. Handle billing inquiries and disputes
2. Explain charges and payment processes clearly
3. Guide customers through refund requests
4. Provide subscription management assistance
5. Escalate complex financial issues when needed

Guidelines:
- Search the billing knowledge base for policies
- Be precise with financial information
- Show empathy for billing concerns
- Follow company policies strictly
- Clearly explain billing cycles and charges
- Reference KB articles for policy verification
- Flag issues requiring finance team review

Your goal is to resolve billing matters with accuracy and professionalism."""
        )
    return _billing_agent


def get_product_agent(model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
    """Get or create the product information agent"""
    global _product_agent
    if _product_agent is None:
        model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.7,
            streaming=False
        )

        _product_agent = Agent(
            model=model,
            tools=[search_product_kb],
            system="""You are a Product Information Specialist. Your role is to:

1. Answer questions about product features and capabilities
2. Guide customers on how to use product features
3. Provide best practices and recommendations
4. Share relevant documentation and resources
5. Help customers discover features that meet their needs

Guidelines:
- Search the product knowledge base thoroughly
- Be enthusiastic but honest about capabilities
- Provide practical examples and use cases
- Reference documentation and guides
- Suggest features that might help the customer
- Clarify any limitations or constraints
- Encourage exploration of advanced features

Your goal is to help customers understand and maximize value from the product."""
        )
    return _product_agent


# Expose specialist agents as tools using @tool decorator
@tool
def technical_support_agent(customer_inquiry: str) -> str:
    """
    Technical Support Agent - Handles technical issues, errors, bugs, and troubleshooting.
    Use this for connection problems, performance issues, error messages, crashes, API issues, etc.

    Args:
        customer_inquiry: The customer's technical problem or question

    Returns:
        Detailed technical support response with troubleshooting steps
    """
    agent = get_technical_agent()
    return agent(customer_inquiry)


@tool
def billing_support_agent(customer_inquiry: str) -> str:
    """
    Billing Support Agent - Handles billing, payments, refunds, and subscription matters.
    Use this for charges, invoices, payment methods, refund requests, subscription changes, etc.

    Args:
        customer_inquiry: The customer's billing-related inquiry

    Returns:
        Detailed billing support response with policy information and resolution steps
    """
    agent = get_billing_agent()
    return agent(customer_inquiry)


@tool
def product_information_agent(customer_inquiry: str) -> str:
    """
    Product Information Agent - Provides information about product features, capabilities, and usage.
    Use this for feature questions, integration inquiries, how-to questions, best practices, etc.

    Args:
        customer_inquiry: The customer's product-related question

    Returns:
        Comprehensive product information with examples and documentation references
    """
    agent = get_product_agent()
    return agent(customer_inquiry)


# List of all specialist agent tools for easy import
SPECIALIST_AGENT_TOOLS = [
    technical_support_agent,
    billing_support_agent,
    product_information_agent
]
