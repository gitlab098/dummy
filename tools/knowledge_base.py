"""
Knowledge Base Tools for Customer Support
"""

from strands import tool
from typing import List, Dict


@tool
def search_technical_kb(query: str) -> List[Dict[str, str]]:
    """
    Search the technical knowledge base for troubleshooting articles.

    Args:
        query: The search query or issue description

    Returns:
        List of relevant knowledge base articles
    """
    # In production, this would query a vector database or search service
    kb_articles = {
        "connection": [
            {
                "id": "KB-001",
                "title": "Common Connection Issues",
                "summary": "Check network settings, firewall rules, and VPN configuration.",
                "steps": [
                    "Verify internet connectivity",
                    "Check firewall allows connections on port 443",
                    "Disable VPN temporarily to test",
                    "Clear DNS cache"
                ]
            }
        ],
        "performance": [
            {
                "id": "KB-002",
                "title": "Performance Optimization Guide",
                "summary": "Steps to improve system performance.",
                "steps": [
                    "Clear browser cache and cookies",
                    "Update to latest software version",
                    "Check system resource usage",
                    "Disable unnecessary browser extensions"
                ]
            }
        ],
        "error": [
            {
                "id": "KB-003",
                "title": "Common Error Messages",
                "summary": "Solutions for frequently encountered errors.",
                "steps": [
                    "Note the exact error code",
                    "Check service status page",
                    "Try logging out and back in",
                    "Contact support if error persists"
                ]
            }
        ]
    }

    # Simple keyword matching (in production, use semantic search)
    query_lower = query.lower()
    results = []

    for category, articles in kb_articles.items():
        if category in query_lower:
            results.extend(articles)

    # Return all if no specific match
    if not results:
        results = [article for articles in kb_articles.values() for article in articles]

    return results[:3]  # Return top 3 results


@tool
def search_billing_kb(query: str) -> List[Dict[str, str]]:
    """
    Search the billing knowledge base for payment and subscription information.

    Args:
        query: The search query related to billing

    Returns:
        List of relevant billing KB articles
    """
    kb_articles = [
        {
            "id": "KB-101",
            "title": "Billing Cycle Information",
            "content": "Billing occurs on the 1st of each month. Charges reflect previous month usage.",
            "details": "Invoices are sent via email. You can view past invoices in your account dashboard."
        },
        {
            "id": "KB-102",
            "title": "Refund Policy",
            "content": "Refunds available within 30 days of charge with valid reason.",
            "process": [
                "Submit refund request through support portal",
                "Provide reason and transaction ID",
                "Processing takes 5-7 business days",
                "Refund issued to original payment method"
            ]
        },
        {
            "id": "KB-103",
            "title": "Payment Methods",
            "content": "We accept credit cards, debit cards, PayPal, and wire transfers for enterprise accounts.",
            "details": "Payment information can be updated anytime in account settings."
        }
    ]

    query_lower = query.lower()
    if "refund" in query_lower or "cancel" in query_lower:
        return [kb_articles[1]]
    elif "payment" in query_lower or "method" in query_lower:
        return [kb_articles[2]]
    else:
        return kb_articles


@tool
def search_product_kb(query: str) -> List[Dict[str, str]]:
    """
    Search the product knowledge base for features and capabilities.

    Args:
        query: The search query about product features

    Returns:
        List of relevant product KB articles
    """
    kb_articles = [
        {
            "id": "KB-201",
            "title": "Feature Overview",
            "content": "Our platform offers AI-powered analytics, real-time monitoring, and automated workflows.",
            "features": [
                "AI-driven insights and recommendations",
                "Real-time data visualization",
                "Custom workflow automation",
                "Advanced reporting and analytics"
            ]
        },
        {
            "id": "KB-202",
            "title": "Integration Guide",
            "content": "Supports REST API, webhooks, and native integrations with major platforms.",
            "integrations": [
                "Salesforce, HubSpot, Zendesk",
                "Slack, Microsoft Teams",
                "GitHub, Jira, Asana",
                "Custom API integrations"
            ]
        },
        {
            "id": "KB-203",
            "title": "Getting Started Guide",
            "content": "Step-by-step guide to set up your account and start using the platform.",
            "steps": [
                "Create account and verify email",
                "Complete onboarding tutorial",
                "Connect your data sources",
                "Set up your first workflow"
            ]
        }
    ]

    query_lower = query.lower()
    if "integration" in query_lower or "connect" in query_lower:
        return [kb_articles[1]]
    elif "start" in query_lower or "setup" in query_lower:
        return [kb_articles[2]]
    else:
        return kb_articles
