"""
Basic usage examples for Customer Support Agentic AI Workflow

Using AWS Strands Agents SDK
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import CustomerSupportOrchestrator, handle_customer_inquiry
import json


def example_1_technical_issue():
    """Example: Technical support inquiry"""
    print("=" * 80)
    print("EXAMPLE 1: Technical Support Issue")
    print("=" * 80)

    message = """
    I'm having trouble connecting to the API. I keep getting a 401 error
    even though I'm using the correct API key. This is blocking our production
    deployment. Can you help?
    """

    result = handle_customer_inquiry(
        message=message.strip(),
        customer_id="CUST-12345"
    )

    print(f"\nWorkflow ID: {result['workflow_id']}")
    print(f"Status: {result['status']}")
    print(f"Intent: {result['classification']['intent']}")
    print(f"Urgency: {result['classification']['urgency']}")
    print(f"Sentiment: {result['classification']['sentiment']}")
    print(f"\n--- Resolution ---")
    print(result['resolution'])
    print("\n")


def example_2_billing_inquiry():
    """Example: Billing support inquiry"""
    print("=" * 80)
    print("EXAMPLE 2: Billing Inquiry")
    print("=" * 80)

    message = """
    I was charged $150 last month but I thought my subscription was only $99.
    Can you explain what the extra charges are for? I'd like to request a
    refund if this was an error.
    """

    result = handle_customer_inquiry(
        message=message.strip(),
        customer_id="CUST-67890"
    )

    print(f"\nWorkflow ID: {result['workflow_id']}")
    print(f"Status: {result['status']}")
    print(f"Intent: {result['classification']['intent']}")
    print(f"Urgency: {result['classification']['urgency']}")
    print(f"\n--- Resolution ---")
    print(result['resolution'])
    print("\n")


def example_3_product_question():
    """Example: Product information inquiry"""
    print("=" * 80)
    print("EXAMPLE 3: Product Information Question")
    print("=" * 80)

    message = """
    Does your platform support integration with Salesforce? We're looking to
    automatically sync our customer data and I want to know if this is possible
    and how to set it up.
    """

    result = handle_customer_inquiry(
        message=message.strip(),
        customer_id="CUST-11111"
    )

    print(f"\nWorkflow ID: {result['workflow_id']}")
    print(f"Status: {result['status']}")
    print(f"Intent: {result['classification']['intent']}")
    print(f"\n--- Resolution ---")
    print(result['resolution'])
    print("\n")


def example_4_escalation():
    """Example: Inquiry requiring escalation"""
    print("=" * 80)
    print("EXAMPLE 4: Escalation Scenario")
    print("=" * 80)

    message = """
    This is absolutely unacceptable! Your service has been down for 3 hours
    during our busiest time. We're losing thousands of dollars. I need to
    speak with your legal team about compensation immediately!
    """

    result = handle_customer_inquiry(
        message=message.strip(),
        customer_id="CUST-99999"
    )

    print(f"\nWorkflow ID: {result['workflow_id']}")
    print(f"Status: {result['status']}")
    print(f"Intent: {result['classification']['intent']}")
    print(f"Urgency: {result['classification']['urgency']}")
    print(f"Sentiment: {result['classification']['sentiment']}")
    print(f"Requires Escalation: {result['classification']['requires_escalation']}")

    if result['status'] == 'ESCALATED':
        print(f"\n--- Escalation Message ---")
        print(result['escalation_message'])
    print("\n")


def example_5_orchestrator_with_streaming():
    """Example: Using orchestrator with streaming"""
    print("=" * 80)
    print("EXAMPLE 5: Streaming Workflow")
    print("=" * 80)

    message = "How can I reset my password? I can't log into my account."

    orchestrator = CustomerSupportOrchestrator()

    print("\nStreaming workflow updates:")
    for update in orchestrator.process_inquiry_streaming(message, "CUST-22222"):
        print(f"  [{update['type']}] {json.dumps(update, indent=2)}")

    print("\n")


def example_6_multiple_inquiries():
    """Example: Processing multiple inquiries"""
    print("=" * 80)
    print("EXAMPLE 6: Batch Processing Multiple Inquiries")
    print("=" * 80)

    inquiries = [
        ("How do I export my data?", "CUST-001"),
        ("My credit card was declined", "CUST-002"),
        ("The app keeps crashing on iOS", "CUST-003"),
        ("What's included in the enterprise plan?", "CUST-004"),
    ]

    # Create orchestrator once and reuse (more efficient)
    orchestrator = CustomerSupportOrchestrator(enable_logging=False)

    results = []
    for message, customer_id in inquiries:
        result = orchestrator.process_inquiry(message, customer_id)
        results.append({
            "customer_id": customer_id,
            "intent": result['classification']['intent'],
            "urgency": result['classification']['urgency'],
            "status": result['status']
        })

    print("\nProcessed Inquiries Summary:")
    print(json.dumps(results, indent=2))
    print("\n")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "AWS STRANDS AGENTS - CUSTOMER SUPPORT DEMO" + " " * 20 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    try:
        # Run examples
        example_1_technical_issue()
        input("Press Enter to continue to next example...")

        example_2_billing_inquiry()
        input("Press Enter to continue to next example...")

        example_3_product_question()
        input("Press Enter to continue to next example...")

        example_4_escalation()
        input("Press Enter to continue to next example...")

        example_5_orchestrator_with_streaming()
        input("Press Enter to continue to next example...")

        example_6_multiple_inquiries()

        print("=" * 80)
        print("All examples completed!")
        print("=" * 80)

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nError running examples: {str(e)}")
        import traceback
        traceback.print_exc()
