"""
Basic usage examples for Customer Support Agentic AI Workflow

Using AWS Strands Agents SDK with "Agents as Tools" pattern
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import CustomerSupportOrchestrator, handle_customer_inquiry
import json


def example_1_technical_issue():
    """Example: Technical support inquiry - Orchestrator routes to technical_support_agent"""
    print("=" * 80)
    print("EXAMPLE 1: Technical Support Issue")
    print("=" * 80)
    print("Pattern: Orchestrator agent uses technical_support_agent as a tool")
    print()

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
    print(f"\n--- Response ---")
    print(result['response'])
    print("\n")


def example_2_billing_inquiry():
    """Example: Billing support inquiry - Orchestrator routes to billing_support_agent"""
    print("=" * 80)
    print("EXAMPLE 2: Billing Inquiry")
    print("=" * 80)
    print("Pattern: Orchestrator agent uses billing_support_agent as a tool")
    print()

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
    print(f"\n--- Response ---")
    print(result['response'])
    print("\n")


def example_3_product_question():
    """Example: Product information inquiry - Orchestrator routes to product_information_agent"""
    print("=" * 80)
    print("EXAMPLE 3: Product Information Question")
    print("=" * 80)
    print("Pattern: Orchestrator agent uses product_information_agent as a tool")
    print()

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
    print(f"\n--- Response ---")
    print(result['response'])
    print("\n")


def example_4_multi_agent():
    """Example: Complex inquiry that might use multiple agents"""
    print("=" * 80)
    print("EXAMPLE 4: Multi-Agent Scenario")
    print("=" * 80)
    print("Pattern: Orchestrator may consult multiple specialist agents")
    print()

    message = """
    I'm having an issue where my API calls are failing with 500 errors, and
    I'm also being charged for API calls that never completed successfully.
    Can you help me understand what's happening and whether I'll get a refund
    for the failed calls?
    """

    result = handle_customer_inquiry(
        message=message.strip(),
        customer_id="CUST-33333"
    )

    print(f"\nWorkflow ID: {result['workflow_id']}")
    print(f"Status: {result['status']}")
    print(f"\n--- Response ---")
    print(result['response'])
    print("\n")


def example_5_orchestrator_with_streaming():
    """Example: Using orchestrator with streaming"""
    print("=" * 80)
    print("EXAMPLE 5: Streaming Workflow")
    print("=" * 80)
    print("Pattern: Real-time streaming of agent tool calls and responses")
    print()

    message = "How can I reset my password? I can't log into my account."

    orchestrator = CustomerSupportOrchestrator()

    print("\nStreaming workflow:")
    print("-" * 40)
    for update in orchestrator.process_inquiry_streaming(message, "CUST-22222"):
        if update['type'] == 'workflow_start':
            print(f"🚀 Started: {update['workflow_id']}")
        elif update['type'] == 'content':
            print(update['content'], end='', flush=True)
        elif update['type'] == 'workflow_complete':
            print(f"\n✓ Completed: {update['workflow_id']}")

    print("\n")


def example_6_intelligent_routing():
    """Example: Demonstrate model-driven routing decision"""
    print("=" * 80)
    print("EXAMPLE 6: Intelligent Model-Driven Routing")
    print("=" * 80)
    print("Pattern: The model decides which specialist agent to invoke")
    print()

    inquiries = [
        ("How do I export my data?", "CUST-001", "→ Expected: product_information_agent"),
        ("My credit card was declined", "CUST-002", "→ Expected: billing_support_agent"),
        ("The app keeps crashing on iOS", "CUST-003", "→ Expected: technical_support_agent"),
        ("What's included in the enterprise plan?", "CUST-004", "→ Expected: product_information_agent"),
    ]

    # Create orchestrator once and reuse (more efficient)
    orchestrator = CustomerSupportOrchestrator(enable_logging=False)

    for message, customer_id, expected in inquiries:
        print(f"\n📝 Inquiry: {message}")
        print(f"   {expected}")

        result = orchestrator.process_inquiry(message, customer_id)
        print(f"   ✓ Status: {result['status']}")
        print(f"   Response preview: {str(result['response'])[:100]}...")

    print("\n")


def example_7_agents_as_tools_explanation():
    """Explain the Agents as Tools pattern"""
    print("=" * 80)
    print("EXPLANATION: Agents as Tools Pattern")
    print("=" * 80)
    print()
    print("What is 'Agents as Tools'?")
    print("-" * 40)
    print("""
The 'Agents as Tools' pattern in AWS Strands Agents SDK allows you to:

1. **Create Specialist Agents**: Build focused agents with domain expertise
   - Each agent has its own tools and system prompt
   - Examples: TechnicalSupportAgent, BillingAgent, ProductAgent

2. **Expose Agents as Tools**: Wrap agents using the @tool decorator
   - The agent becomes a callable tool for another agent
   - Tool descriptions guide when to use each agent

3. **Model-Driven Orchestration**: Let the model decide routing
   - The orchestrator agent has specialist agents in its toolbox
   - The model chooses which specialist to invoke based on the query
   - No manual routing logic required!

4. **Benefits**:
   ✓ Simple, declarative code
   ✓ Model intelligence drives routing decisions
   ✓ Easy to add new specialist agents
   ✓ Agents can collaborate on complex inquiries
   ✓ Production-ready framework from AWS

Example Architecture:
------------------
┌─────────────────────────────┐
│  Orchestrator Agent         │
│  (Has access to tools)      │
└──────────┬──────────────────┘
           │
           ├─ Tool: analyze_sentiment()
           ├─ Tool: determine_urgency()
           ├─ Tool: classify_intent()
           ├─ Tool: technical_support_agent()  ← Agent as Tool!
           ├─ Tool: billing_support_agent()    ← Agent as Tool!
           └─ Tool: product_information_agent() ← Agent as Tool!

The model decides which tools to call based on the customer inquiry.
""")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " AWS STRANDS AGENTS - AGENTS AS TOOLS PATTERN DEMO".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    try:
        # Show explanation first
        example_7_agents_as_tools_explanation()
        input("Press Enter to run examples...")

        # Run examples
        example_1_technical_issue()
        input("Press Enter to continue...")

        example_2_billing_inquiry()
        input("Press Enter to continue...")

        example_3_product_question()
        input("Press Enter to continue...")

        example_4_multi_agent()
        input("Press Enter to continue...")

        example_5_orchestrator_with_streaming()
        input("Press Enter to continue...")

        example_6_intelligent_routing()

        print("=" * 80)
        print("All examples completed!")
        print("=" * 80)
        print("\nKey Takeaway:")
        print("The 'Agents as Tools' pattern enables model-driven multi-agent")
        print("orchestration where the model intelligently routes to specialists.")
        print("\n")

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nError running examples: {str(e)}")
        import traceback
        traceback.print_exc()
