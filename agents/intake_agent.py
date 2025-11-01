"""
Intake Agent - Analyzes customer inquiries and routes to appropriate specialist

Built using AWS Strands Agents SDK
"""

from strands import Agent
from strands.models import BedrockModel
from tools.customer_analysis import (
    analyze_sentiment,
    determine_urgency,
    classify_intent,
    check_escalation_needed
)
from typing import Dict, Any


class IntakeAgent:
    """
    Intake Agent analyzes customer inquiries and determines routing
    """

    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", region: str = "us-west-2"):
        """
        Initialize the Intake Agent

        Args:
            model_id: The Bedrock model ID to use
            region: AWS region for Bedrock
        """
        # Configure Bedrock model
        self.model = BedrockModel(
            model_id=model_id,
            region=region,
            temperature=0.3,  # Lower temperature for consistent classification
            streaming=True
        )

        # Create agent with analysis tools
        self.agent = Agent(
            model=self.model,
            tools=[
                analyze_sentiment,
                determine_urgency,
                classify_intent,
                check_escalation_needed
            ],
            system="""You are an Intake Agent for customer support. Your role is to:

1. Analyze the customer's inquiry comprehensively
2. Use your tools to:
   - Classify the intent (TECHNICAL, BILLING, PRODUCT_INFO, or GENERAL)
   - Determine urgency level (CRITICAL, HIGH, MEDIUM, LOW)
   - Analyze customer sentiment (POSITIVE, NEUTRAL, NEGATIVE, FRUSTRATED)
   - Check if escalation to human agent is needed

3. Provide a structured analysis with:
   - Clear classification of the inquiry
   - Key points extracted from the message
   - Recommended next steps
   - Escalation flag if needed

Be thorough but concise. Use all available tools to provide accurate analysis.
Extract specific details like product names, error messages, or account issues."""
        )

    def analyze(self, customer_message: str, customer_id: str = None) -> Dict[str, Any]:
        """
        Analyze a customer inquiry

        Args:
            customer_message: The customer's message
            customer_id: Optional customer ID

        Returns:
            Dictionary containing complete analysis
        """
        # Construct the prompt for the agent
        prompt = f"""Analyze this customer inquiry:

Customer Message: "{customer_message}"
{f"Customer ID: {customer_id}" if customer_id else ""}

Please:
1. Use classify_intent to determine the inquiry type
2. Use determine_urgency to assess urgency
3. Use analyze_sentiment to understand customer emotion
4. Extract key points and specific details from the message
5. Use check_escalation_needed to determine if human escalation is required
6. Provide a comprehensive analysis summary

Provide your analysis in a clear, structured format."""

        # Invoke the agent
        response = self.agent(prompt)

        return {
            "analysis_complete": True,
            "customer_id": customer_id,
            "original_message": customer_message,
            "agent_response": response
        }

    def analyze_streaming(self, customer_message: str, customer_id: str = None):
        """
        Analyze with streaming response

        Args:
            customer_message: The customer's message
            customer_id: Optional customer ID

        Yields:
            Streaming response chunks
        """
        prompt = f"""Analyze this customer inquiry:

Customer Message: "{customer_message}"
{f"Customer ID: {customer_id}" if customer_id else ""}

Use your tools to analyze intent, urgency, sentiment, and escalation needs.
Provide a comprehensive analysis."""

        # Stream the response
        for chunk in self.agent.stream(prompt):
            yield chunk
