"""
Simple test script to verify the setup

Run this first to ensure everything is configured correctly
"""

import sys
import os

print("Testing AWS Strands Agents Customer Support Workflow Setup...")
print("-" * 60)

# Test 1: Check Python version
print("\n1. Checking Python version...")
print(f"   Python {sys.version}")
if sys.version_info < (3, 10):
    print("   ❌ ERROR: Python 3.10+ required")
    sys.exit(1)
print("   ✓ Python version OK")

# Test 2: Check imports
print("\n2. Checking required packages...")
try:
    import boto3
    print("   ✓ boto3 installed")
except ImportError:
    print("   ❌ boto3 not found. Run: pip install boto3")

try:
    from strands import Agent, tool
    print("   ✓ strands-agents installed")
except ImportError:
    print("   ❌ strands-agents not found. Run: pip install strands-agents")

try:
    from strands.models import BedrockModel
    print("   ✓ strands models available")
except ImportError:
    print("   ❌ strands models not available")

try:
    import pydantic
    print("   ✓ pydantic installed")
except ImportError:
    print("   ❌ pydantic not found. Run: pip install pydantic")

# Test 3: Check AWS credentials
print("\n3. Checking AWS credentials...")
try:
    import boto3
    session = boto3.Session()
    credentials = session.get_credentials()
    if credentials:
        print("   ✓ AWS credentials found")
    else:
        print("   ❌ AWS credentials not configured")
        print("   Configure with: aws configure")
except Exception as e:
    print(f"   ❌ Error checking credentials: {e}")

# Test 4: Check Bedrock access
print("\n4. Checking Bedrock access...")
try:
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    print("   ✓ Bedrock client created successfully")
    print("   Note: Actual model access will be verified on first use")
except Exception as e:
    print(f"   ⚠ Warning: Could not create Bedrock client: {e}")

# Test 5: Check project structure
print("\n5. Checking project structure...")
required_files = [
    'tools/knowledge_base.py',
    'tools/customer_analysis.py',
    'agents/intake_agent.py',
    'agents/specialist_agents.py',
    'orchestrator.py',
]

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for file in required_files:
    file_path = os.path.join(project_root, file)
    if os.path.exists(file_path):
        print(f"   ✓ {file}")
    else:
        print(f"   ❌ {file} not found")

# Test 6: Try importing project modules
print("\n6. Testing project imports...")
sys.path.append(project_root)

try:
    from tools.customer_analysis import analyze_sentiment
    print("   ✓ customer_analysis tools")
except ImportError as e:
    print(f"   ❌ customer_analysis tools: {e}")

try:
    from tools.knowledge_base import search_technical_kb
    print("   ✓ knowledge_base tools")
except ImportError as e:
    print(f"   ❌ knowledge_base tools: {e}")

try:
    from agents.intake_agent import IntakeAgent
    print("   ✓ intake_agent")
except ImportError as e:
    print(f"   ❌ intake_agent: {e}")

try:
    from agents.specialist_agents import TechnicalSupportAgent
    print("   ✓ specialist_agents")
except ImportError as e:
    print(f"   ❌ specialist_agents: {e}")

try:
    from orchestrator import CustomerSupportOrchestrator
    print("   ✓ orchestrator")
except ImportError as e:
    print(f"   ❌ orchestrator: {e}")

# Final summary
print("\n" + "=" * 60)
print("Setup verification complete!")
print("=" * 60)
print("\nNext steps:")
print("1. Ensure AWS credentials are configured: aws configure")
print("2. Verify Bedrock model access in AWS console")
print("3. Run examples: python examples/basic_usage.py")
print("\n")
