"""
Multi-Agent Orchestrator for Customer Support Workflow

Built using AWS Strands Agents SDK - Coordinates multiple specialized agents
"""

from agents.intake_agent import IntakeAgent
from agents.specialist_agents import get_specialist_agent
from typing import Dict, Any, Optional
import json
import re
from datetime import datetime


class CustomerSupportOrchestrator:
    """
    Orchestrates the multi-agent customer support workflow

    Workflow:
    1. Intake Agent analyzes the inquiry
    2. Routes to appropriate Specialist Agent
    3. Specialist provides resolution
    4. Returns complete support response
    """

    def __init__(
        self,
        model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
        region: str = "us-west-2",
        enable_logging: bool = True
    ):
        """
        Initialize the orchestrator

        Args:
            model_id: Bedrock model ID to use for all agents
            region: AWS region for Bedrock
            enable_logging: Enable detailed logging
        """
        self.model_id = model_id
        self.region = region
        self.enable_logging = enable_logging

        # Initialize intake agent
        self.intake_agent = IntakeAgent(model_id=model_id, region=region)

        # Cache for specialist agents (lazy initialization)
        self._specialist_cache = {}

    def _log(self, message: str, level: str = "INFO"):
        """Internal logging method"""
        if self.enable_logging:
            timestamp = datetime.utcnow().isoformat()
            print(f"[{timestamp}] [{level}] {message}")

    def _extract_classification(self, analysis_text: str) -> Dict[str, Any]:
        """
        Extract structured classification from agent analysis

        Args:
            analysis_text: Raw analysis text from intake agent

        Returns:
            Dictionary with extracted classifications
        """
        result = {
            "intent": "GENERAL",
            "urgency": "MEDIUM",
            "sentiment": "NEUTRAL",
            "requires_escalation": False,
            "key_points": []
        }

        text_lower = analysis_text.lower()

        # Extract intent
        if "technical" in text_lower:
            result["intent"] = "TECHNICAL"
        elif "billing" in text_lower or "payment" in text_lower:
            result["intent"] = "BILLING"
        elif "product" in text_lower or "feature" in text_lower:
            result["intent"] = "PRODUCT_INFO"

        # Extract urgency
        if "critical" in text_lower or "emergency" in text_lower:
            result["urgency"] = "CRITICAL"
        elif "high" in text_lower and "urgency" in text_lower:
            result["urgency"] = "HIGH"
        elif "low" in text_lower and "urgency" in text_lower:
            result["urgency"] = "LOW"

        # Extract sentiment
        if "frustrated" in text_lower or "angry" in text_lower:
            result["sentiment"] = "FRUSTRATED"
        elif "negative" in text_lower or "dissatisfied" in text_lower:
            result["sentiment"] = "NEGATIVE"
        elif "positive" in text_lower or "happy" in text_lower:
            result["sentiment"] = "POSITIVE"

        # Check escalation
        if "escalation" in text_lower or "escalate" in text_lower:
            result["requires_escalation"] = True

        return result

    def _get_specialist(self, intent: str):
        """
        Get or create specialist agent for given intent

        Args:
            intent: The intent type

        Returns:
            Specialist agent instance
        """
        if intent not in self._specialist_cache:
            self._log(f"Initializing specialist agent for intent: {intent}")
            self._specialist_cache[intent] = get_specialist_agent(
                intent,
                model_id=self.model_id,
                region=self.region
            )
        return self._specialist_cache[intent]

    def process_inquiry(
        self,
        customer_message: str,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a customer inquiry through the multi-agent workflow

        Args:
            customer_message: The customer's message
            customer_id: Optional customer identifier

        Returns:
            Complete support workflow results
        """
        workflow_id = f"WF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self._log(f"Starting workflow {workflow_id} for customer: {customer_id or 'unknown'}")

        # Step 1: Intake Analysis
        self._log("Step 1: Running intake analysis")
        intake_result = self.intake_agent.analyze(customer_message, customer_id)
        intake_analysis = intake_result["agent_response"]

        self._log(f"Intake analysis complete. Length: {len(str(intake_analysis))} chars")

        # Step 2: Extract Classification
        classification = self._extract_classification(str(intake_analysis))
        self._log(f"Classification: Intent={classification['intent']}, "
                 f"Urgency={classification['urgency']}, "
                 f"Sentiment={classification['sentiment']}")

        # Check for immediate escalation
        if classification["requires_escalation"]:
            self._log("ESCALATION REQUIRED - Flagging for human agent", level="WARNING")
            return {
                "workflow_id": workflow_id,
                "customer_id": customer_id,
                "status": "ESCALATED",
                "intake_analysis": intake_analysis,
                "classification": classification,
                "escalation_message": "This inquiry has been flagged for immediate human review.",
                "timestamp": datetime.utcnow().isoformat()
            }

        # Step 3: Route to Specialist
        intent = classification["intent"]
        self._log(f"Step 2: Routing to {intent} specialist")

        specialist = self._get_specialist(intent)
        specialist_response = specialist.resolve(
            customer_message,
            context=classification
        )

        self._log(f"Specialist response complete. Length: {len(str(specialist_response))} chars")

        # Step 4: Compile Final Response
        return {
            "workflow_id": workflow_id,
            "customer_id": customer_id,
            "status": "RESOLVED",
            "intake_analysis": intake_analysis,
            "classification": classification,
            "specialist_type": intent,
            "resolution": specialist_response,
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
            Streaming workflow updates
        """
        workflow_id = f"WF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        yield {
            "type": "workflow_start",
            "workflow_id": workflow_id,
            "customer_id": customer_id
        }

        # Intake analysis with streaming
        yield {"type": "stage", "stage": "intake_analysis", "status": "started"}

        intake_result = self.intake_agent.analyze(customer_message, customer_id)
        classification = self._extract_classification(str(intake_result["agent_response"]))

        yield {
            "type": "stage",
            "stage": "intake_analysis",
            "status": "completed",
            "classification": classification
        }

        # Check escalation
        if classification["requires_escalation"]:
            yield {
                "type": "escalation",
                "message": "Inquiry requires human agent review"
            }
            return

        # Specialist resolution
        yield {
            "type": "stage",
            "stage": "specialist_resolution",
            "status": "started",
            "specialist_type": classification["intent"]
        }

        specialist = self._get_specialist(classification["intent"])
        resolution = specialist.resolve(customer_message, context=classification)

        yield {
            "type": "stage",
            "stage": "specialist_resolution",
            "status": "completed",
            "resolution": resolution
        }

        yield {
            "type": "workflow_complete",
            "workflow_id": workflow_id,
            "status": "RESOLVED"
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

    Args:
        message: Customer's message
        customer_id: Optional customer ID
        model_id: Bedrock model to use
        region: AWS region

    Returns:
        Complete workflow result
    """
    orchestrator = CustomerSupportOrchestrator(
        model_id=model_id,
        region=region
    )

    return orchestrator.process_inquiry(message, customer_id)
