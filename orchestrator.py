"""
Multi-Agent Orchestrator for Customer Support Workflow

Built using AWS Strands Agents SDK with "Agents as Tools" pattern
The orchestrator is itself an Agent that uses specialist agents as tools
"""

from strands import Agent
from strands.models import BedrockModel
from agents.specialist_agents import SPECIALIST_AGENT_TOOLS
from tools.customer_analysis import (
    analyze_sentiment,
    determine_urgency,
    classify_intent,
    check_escalation_needed
)
from typing import Dict, Any, Optional
from datetime import datetime


class CustomerSupportOrchestrator:
    """
    Orchestrates the multi-agent customer support workflow using "Agents as Tools" pattern

    The orchestrator itself is an Agent that has access to:
    1. Analysis tools (sentiment, urgency, intent, escalation)
    2. Specialist agents exposed as tools (technical, billing, product)

    The model decides which specialist agent to invoke based on the customer inquiry.
    """

    def __init__(
        self,
        model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
        region: str = "us-west-2",
        enable_logging: bool = True
    ):
        """
        Initialize the orchestrator as an Agent with specialist agents as tools

        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
            enable_logging: Enable detailed logging
        """
        self.model_id = model_id
        self.region = region
        self.enable_logging = enable_logging

        # Configure Bedrock model for orchestrator
        self.model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.7,
            streaming=True
        )

        # Combine analysis tools and specialist agents as tools
        all_tools = [
            analyze_sentiment,
            determine_urgency,
            classify_intent,
            check_escalation_needed,
        ] + SPECIALIST_AGENT_TOOLS

        # Create the orchestrator agent with all tools
        self.agent = Agent(
            model=self.model,
            tools=all_tools,
            system="""You are a Customer Support Orchestrator Agent. Your role is to coordinate customer support by:

1. **Analyzing the Customer Inquiry**: Use your analysis tools to understand:
   - Sentiment (analyze_sentiment)
   - Urgency level (determine_urgency)
   - Intent/category (classify_intent)
   - Whether escalation is needed (check_escalation_needed)

2. **Routing to Specialist Agents**: Based on the inquiry type, delegate to the appropriate specialist agent:
   - **technical_support_agent**: For technical issues, errors, bugs, API problems, performance issues
   - **billing_support_agent**: For billing, payments, refunds, subscriptions, invoices
   - **product_information_agent**: For product features, capabilities, integrations, how-to questions

3. **Decision Making**:
   - You decide which specialist agent to use based on the customer's inquiry
   - You can use multiple tools/agents if needed
   - If escalation is detected, inform the customer immediately
   - Provide a professional, complete response

**Important Guidelines**:
- Always analyze the inquiry first to understand context
- Choose the most appropriate specialist agent for the inquiry
- If an inquiry spans multiple areas, you may consult multiple agents
- Be empathetic and professional
- Provide clear, actionable responses
- Flag any critical escalations

Your goal is to provide excellent customer support by intelligently routing inquiries to the right specialist agents."""
        )

    def _log(self, message: str, level: str = "INFO"):
        """Internal logging method"""
        if self.enable_logging:
            timestamp = datetime.utcnow().isoformat()
            print(f"[{timestamp}] [{level}] {message}")

    def process_inquiry(
        self,
        customer_message: str,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a customer inquiry through the multi-agent workflow

        The orchestrator agent will:
        1. Analyze the inquiry
        2. Decide which specialist agent(s) to invoke
        3. Return the complete response

        Args:
            customer_message: The customer's message
            customer_id: Optional customer identifier

        Returns:
            Complete support workflow results
        """
        workflow_id = f"WF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self._log(f"Starting workflow {workflow_id} for customer: {customer_id or 'unknown'}")

        # Construct the prompt for the orchestrator agent
        prompt = f"""New customer support inquiry:

Customer ID: {customer_id or 'Not provided'}
Customer Message: "{customer_message}"

Please:
1. Analyze this inquiry to understand the customer's needs, sentiment, urgency, and intent
2. Determine if immediate escalation is required
3. Route to the appropriate specialist agent(s) to resolve the inquiry
4. Provide a comprehensive, professional response

Remember to use your analysis tools first, then delegate to the appropriate specialist agent."""

        self._log("Orchestrator agent processing inquiry...")

        # Invoke the orchestrator agent - it will use tools as needed
        response = self.agent(prompt)

        self._log(f"Orchestrator completed. Response length: {len(str(response))} chars")

        # Return structured result
        return {
            "workflow_id": workflow_id,
            "customer_id": customer_id,
            "status": "COMPLETED",
            "original_message": customer_message,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    def process_inquiry_streaming(
        self,
        customer_message: str,
        customer_id: Optional[str] = None
    ):
        """
        Process inquiry with streaming responses

        Args:
            customer_message: The customer's message
            customer_id: Optional customer identifier

        Yields:
            Streaming response chunks
        """
        workflow_id = f"WF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        yield {
            "type": "workflow_start",
            "workflow_id": workflow_id,
            "customer_id": customer_id
        }

        # Construct prompt
        prompt = f"""New customer support inquiry:

Customer ID: {customer_id or 'Not provided'}
Customer Message: "{customer_message}"

Please analyze and resolve this inquiry using the appropriate tools and specialist agents."""

        # Stream the response
        for chunk in self.agent.stream(prompt):
            yield {
                "type": "content",
                "content": chunk
            }

        yield {
            "type": "workflow_complete",
            "workflow_id": workflow_id
        }


# Convenience function for single-call usage
def handle_customer_inquiry(
    message: str,
    customer_id: Optional[str] = None,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    region: str = "us-west-2"
) -> Dict[str, Any]:
    """
    Convenience function to handle a customer inquiry with one call

    Uses the "Agents as Tools" pattern where the orchestrator agent
    intelligently routes to specialist agents based on the inquiry.

    Args:
        message: Customer's message
        customer_id: Optional customer ID
        model_id: Bedrock model to use
        region: AWS region

    Returns:
        Complete workflow result

    Example:
        >>> result = handle_customer_inquiry(
        ...     message="I'm getting a 500 error on the API",
        ...     customer_id="CUST-12345"
        ... )
        >>> print(result['response'])
    """
    orchestrator = CustomerSupportOrchestrator(
        model_id=model_id,
        region=region
    )

    return orchestrator.process_inquiry(message, customer_id)
