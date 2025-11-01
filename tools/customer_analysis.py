"""
Customer Analysis Tools
"""

from strands import tool
from typing import Dict, Any
import re


@tool
def analyze_sentiment(message: str) -> Dict[str, Any]:
    """
    Analyze the sentiment and emotional tone of a customer message.

    Args:
        message: The customer's message text

    Returns:
        Dictionary containing sentiment analysis results
    """
    message_lower = message.lower()

    # Frustrated indicators
    frustrated_keywords = [
        "frustrated", "angry", "terrible", "awful", "horrible",
        "worst", "unacceptable", "disappointed", "!!!",
        "furious", "ridiculous", "pathetic"
    ]

    # Negative indicators
    negative_keywords = [
        "problem", "issue", "error", "broken", "not working",
        "failed", "can't", "unable", "doesn't work", "help"
    ]

    # Positive indicators
    positive_keywords = [
        "great", "excellent", "love", "perfect", "amazing",
        "wonderful", "fantastic", "thank", "appreciate"
    ]

    frustrated_count = sum(1 for keyword in frustrated_keywords if keyword in message_lower)
    negative_count = sum(1 for keyword in negative_keywords if keyword in message_lower)
    positive_count = sum(1 for keyword in positive_keywords if keyword in message_lower)

    # Determine sentiment
    if frustrated_count >= 2 or "!!!" in message:
        sentiment = "FRUSTRATED"
        emotion = "angry or very upset"
    elif frustrated_count >= 1 or negative_count >= 3:
        sentiment = "NEGATIVE"
        emotion = "dissatisfied or concerned"
    elif positive_count >= 2:
        sentiment = "POSITIVE"
        emotion = "happy and satisfied"
    elif positive_count >= 1:
        sentiment = "NEUTRAL"
        emotion = "calm and neutral"
    elif negative_count >= 1:
        sentiment = "NEGATIVE"
        emotion = "experiencing issues"
    else:
        sentiment = "NEUTRAL"
        emotion = "neutral"

    return {
        "sentiment": sentiment,
        "emotion": emotion,
        "confidence": 0.85,
        "indicators": {
            "frustrated": frustrated_count,
            "negative": negative_count,
            "positive": positive_count
        }
    }


@tool
def determine_urgency(message: str) -> Dict[str, Any]:
    """
    Determine the urgency level of a customer inquiry.

    Args:
        message: The customer's message text

    Returns:
        Dictionary containing urgency assessment
    """
    message_lower = message.lower()

    # Critical urgency
    critical_keywords = [
        "emergency", "critical", "urgent", "asap", "immediately",
        "data breach", "security", "down", "outage", "can't access"
    ]

    # High urgency
    high_keywords = [
        "important", "soon", "quickly", "blocked", "stuck",
        "production", "business impact", "losing money"
    ]

    # Check for critical
    if any(keyword in message_lower for keyword in critical_keywords):
        return {
            "urgency": "CRITICAL",
            "priority": 1,
            "sla_hours": 1,
            "reason": "Contains critical urgency indicators"
        }

    # Check for high
    if any(keyword in message_lower for keyword in high_keywords):
        return {
            "urgency": "HIGH",
            "priority": 2,
            "sla_hours": 4,
            "reason": "Contains high urgency indicators"
        }

    # Check for medium (questions, problems)
    if any(word in message_lower for word in ["problem", "issue", "error", "help"]):
        return {
            "urgency": "MEDIUM",
            "priority": 3,
            "sla_hours": 24,
            "reason": "General problem or question"
        }

    # Default to low
    return {
        "urgency": "LOW",
        "priority": 4,
        "sla_hours": 72,
        "reason": "General inquiry or information request"
    }


@tool
def classify_intent(message: str) -> Dict[str, Any]:
    """
    Classify the intent category of a customer inquiry.

    Args:
        message: The customer's message text

    Returns:
        Dictionary containing intent classification
    """
    message_lower = message.lower()

    # Technical keywords
    technical_keywords = [
        "error", "bug", "broken", "not working", "crash", "performance",
        "slow", "connection", "login", "install", "setup", "configure",
        "api", "integration", "code", "technical"
    ]

    # Billing keywords
    billing_keywords = [
        "charge", "bill", "invoice", "payment", "refund", "subscription",
        "cancel", "upgrade", "downgrade", "price", "cost", "fee",
        "credit card", "transaction"
    ]

    # Product info keywords
    product_keywords = [
        "feature", "how to", "can i", "does it", "support", "capability",
        "functionality", "use", "work", "documentation", "guide", "tutorial"
    ]

    technical_score = sum(1 for keyword in technical_keywords if keyword in message_lower)
    billing_score = sum(1 for keyword in billing_keywords if keyword in message_lower)
    product_score = sum(1 for keyword in product_keywords if keyword in message_lower)

    scores = {
        "TECHNICAL": technical_score,
        "BILLING": billing_score,
        "PRODUCT_INFO": product_score
    }

    # Determine primary intent
    if max(scores.values()) == 0:
        intent = "GENERAL"
        confidence = 0.6
    else:
        intent = max(scores, key=scores.get)
        total = sum(scores.values())
        confidence = scores[intent] / total if total > 0 else 0.5

    return {
        "intent": intent,
        "confidence": round(confidence, 2),
        "scores": scores,
        "category_description": {
            "TECHNICAL": "Technical support or troubleshooting",
            "BILLING": "Billing, payments, or subscriptions",
            "PRODUCT_INFO": "Product features and information",
            "GENERAL": "General inquiry"
        }.get(intent)
    }


@tool
def check_escalation_needed(message: str, sentiment: str, urgency: str) -> Dict[str, Any]:
    """
    Determine if the inquiry requires human escalation.

    Args:
        message: The customer's message text
        sentiment: The detected sentiment
        urgency: The detected urgency level

    Returns:
        Dictionary indicating if escalation is needed and why
    """
    message_lower = message.lower()

    # Auto-escalation keywords
    escalation_keywords = [
        "lawsuit", "lawyer", "legal", "attorney", "sue",
        "fraud", "scam", "steal", "data breach", "security incident",
        "gdpr", "compliance", "regulation", "executive", "manager"
    ]

    # Check for escalation triggers
    escalation_reasons = []

    for keyword in escalation_keywords:
        if keyword in message_lower:
            escalation_reasons.append(f"Contains critical keyword: {keyword}")

    if sentiment == "FRUSTRATED" and urgency in ["CRITICAL", "HIGH"]:
        escalation_reasons.append("Combination of frustrated sentiment and high urgency")

    if urgency == "CRITICAL":
        escalation_reasons.append("Critical urgency level detected")

    requires_escalation = len(escalation_reasons) > 0

    return {
        "requires_escalation": requires_escalation,
        "escalation_reasons": escalation_reasons,
        "suggested_team": "Legal" if any(k in message_lower for k in ["lawsuit", "legal", "lawyer"])
                         else "Security" if any(k in message_lower for k in ["breach", "security"])
                         else "Management" if requires_escalation
                         else None,
        "escalation_priority": "IMMEDIATE" if len(escalation_reasons) >= 2 else "HIGH" if requires_escalation else "NONE"
    }
