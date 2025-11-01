"""
Specialist Agents - Handle specific types of customer inquiries

Built using AWS Strands Agents SDK
"""

from strands import Agent
from strands.models import BedrockModel
from tools.knowledge_base import (
    search_technical_kb,
    search_billing_kb,
    search_product_kb
)
from typing import Dict, Any


class TechnicalSupportAgent:
    """
    Technical Support Agent - Handles technical issues and troubleshooting
    """

    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
        self.model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.7,
            streaming=True
        )

        self.agent = Agent(
            model=self.model,
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

    def resolve(self, customer_message: str, context: Dict[str, Any] = None) -> str:
        """
        Provide technical support resolution

        Args:
            customer_message: The customer's technical issue
            context: Additional context from intake analysis

        Returns:
            Technical support response
        """
        context_str = ""
        if context:
            context_str = f"""
Context from intake analysis:
- Urgency: {context.get('urgency', 'N/A')}
- Sentiment: {context.get('sentiment', 'N/A')}
"""

        prompt = f"""{context_str}

Customer's Technical Issue:
"{customer_message}"

Please:
1. Search the technical knowledge base for relevant solutions
2. Analyze the issue and provide diagnostic steps
3. Offer a clear, step-by-step resolution
4. Include relevant KB article references
5. Indicate if engineering escalation is needed

Provide a comprehensive technical support response."""

        return self.agent(prompt)


class BillingSupportAgent:
    """
    Billing Support Agent - Handles billing, payments, and subscriptions
    """

    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
        self.model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.5,  # Lower temperature for accuracy with financial matters
            streaming=True
        )

        self.agent = Agent(
            model=self.model,
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

    def resolve(self, customer_message: str, context: Dict[str, Any] = None) -> str:
        """
        Provide billing support resolution

        Args:
            customer_message: The customer's billing inquiry
            context: Additional context from intake analysis

        Returns:
            Billing support response
        """
        context_str = ""
        if context:
            context_str = f"""
Context from intake analysis:
- Urgency: {context.get('urgency', 'N/A')}
- Sentiment: {context.get('sentiment', 'N/A')}
"""

        prompt = f"""{context_str}

Customer's Billing Inquiry:
"{customer_message}"

Please:
1. Search the billing knowledge base for relevant policies
2. Address the customer's billing concern clearly
3. Explain any charges or processes
4. Provide steps for resolution (refunds, payment updates, etc.)
5. Include relevant policy references from KB
6. Indicate if finance team escalation is needed

Provide a clear and accurate billing support response."""

        return self.agent(prompt)


class ProductInformationAgent:
    """
    Product Information Agent - Provides information about features and capabilities
    """

    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
        self.model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.7,
            streaming=True
        )

        self.agent = Agent(
            model=self.model,
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

    def resolve(self, customer_message: str, context: Dict[str, Any] = None) -> str:
        """
        Provide product information response

        Args:
            customer_message: The customer's product question
            context: Additional context from intake analysis

        Returns:
            Product information response
        """
        context_str = ""
        if context:
            context_str = f"""
Context from intake analysis:
- Urgency: {context.get('urgency', 'N/A')}
- Sentiment: {context.get('sentiment', 'N/A')}
"""

        prompt = f"""{context_str}

Customer's Product Question:
"{customer_message}"

Please:
1. Search the product knowledge base for relevant information
2. Answer the customer's question comprehensively
3. Provide practical examples or use cases
4. Share relevant documentation links from KB
5. Suggest related features that might interest them
6. Include getting started steps if applicable

Provide a helpful and informative product response."""

        return self.agent(prompt)


# Agent routing function
def get_specialist_agent(intent: str, **kwargs):
    """
    Get the appropriate specialist agent based on intent

    Args:
        intent: The classified intent type
        **kwargs: Additional arguments for agent initialization

    Returns:
        Appropriate specialist agent instance
    """
    agent_map = {
        "TECHNICAL": TechnicalSupportAgent,
        "BILLING": BillingSupportAgent,
        "PRODUCT_INFO": ProductInformationAgent,
        "GENERAL": ProductInformationAgent  # Default to product info
    }

    agent_class = agent_map.get(intent, ProductInformationAgent)
    return agent_class(**kwargs)
