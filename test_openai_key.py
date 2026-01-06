#!/usr/bin/env python3
"""
OpenAI API Key Test Script
Tests whether the OpenAI API key is active and can make successful API calls.
"""

import os
import sys

print("=" * 60)
print("OpenAI API Key Test Script")
print("=" * 60)

# Load environment variables from .env file
print("\n[Step 1] Loading environment variables from .env file...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Environment variables loaded from .env file")
except ImportError:
    print("✗ python-dotenv package not found!")
    print("\nPlease install it using:")
    print("  pip install python-dotenv")
    sys.exit(1)

# Check if openai package is installed
print("\n[Step 2] Checking if 'openai' package is installed...")
try:
    import openai
    print(f"✓ OpenAI package found (version: {openai.__version__})")
except ImportError:
    print("✗ OpenAI package not found!")
    print("\nPlease install it using:")
    print("  pip install openai")
    sys.exit(1)

# Check for API key
print("\n[Step 3] Checking for OpenAI API key...")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your-openai-api-key-here":
    print("✗ OPENAI_API_KEY not set or still has default value!")
    print("\nPlease update the .env file with your actual API key:")
    print("  1. Open the .env file in this directory")
    print("  2. Replace 'your-openai-api-key-here' with your actual OpenAI API key")
    sys.exit(1)

print(f"✓ API key found (starts with: {api_key[:8]}...)")

# Initialize OpenAI client
print("\n[Step 4] Initializing OpenAI client...")
try:
    client = openai.OpenAI(api_key=api_key)
    print("✓ OpenAI client initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize client: {e}")
    sys.exit(1)

# Test API call with a simple completion
print("\n[Step 5] Making a test API call...")
print("Sending a simple chat completion request...")

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Hello! Your API key is working.'"}
        ],
        max_tokens=20
    )
    
    print("✓ API call successful!")
    print(f"\n[Response Details]")
    print(f"  Model used: {response.model}")
    print(f"  Tokens used: {response.usage.total_tokens} (prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens})")
    print(f"  Response: {response.choices[0].message.content}")
    
    # Key validation confirmation
    print("\n" + "=" * 60)
    print("🔑 KEY VALIDATION STATUS")
    print("=" * 60)
    print("✓ Active Secret - OpenAI confirmed this API key is active")
    print(f"  Key prefix: {api_key[:10]}...")
    print(f"  Status: ACTIVE and operational")
    print(f"  Validated at: {response.created}")
    print("=" * 60)
    
except openai.AuthenticationError as e:
    print(f"✗ Authentication failed: {e}")
    print("\n" + "=" * 60)
    print("🔑 KEY VALIDATION STATUS")
    print("=" * 60)
    print("✗ Invalid Secret - OpenAI rejected this API key")
    print(f"  Key prefix: {api_key[:10]}...")
    print(f"  Status: INVALID or REVOKED")
    print("  The key appears to be inactive, expired, or incorrectly formatted.")
    print("=" * 60)
    sys.exit(1)
    
except openai.RateLimitError as e:
    print(f"✗ Rate limit exceeded: {e}")
    print("\n" + "=" * 60)
    print("🔑 KEY VALIDATION STATUS")
    print("=" * 60)
    print("✓ Active Secret - OpenAI confirmed this API key is active")
    print(f"  Key prefix: {api_key[:10]}...")
    print(f"  Status: ACTIVE but rate-limited")
    print("  The key is valid but you've exceeded your usage quota/limits.")
    print("=" * 60)
    sys.exit(1)
    
except openai.APIError as e:
    print(f"✗ API error: {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)

print("\n✓ All tests passed! Your OpenAI API key is active and working.")
