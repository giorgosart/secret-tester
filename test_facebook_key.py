#!/usr/bin/env python3
"""
Facebook/Meta API Key Test Script
Tests whether your Facebook/Meta API access token is active and can make successful API calls.
"""

import os
import sys
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings if verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 60)
print("Facebook/Meta API Key Test Script")
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
    print("  pip install python-dotenv requests")
    sys.exit(1)

# Check if requests package is installed
print("\n[Step 2] Checking if 'requests' package is installed...")
try:
    import requests
    print(f"✓ Requests package found (version: {requests.__version__})")
except ImportError:
    print("✗ Requests package not found!")
    print("\nPlease install it using:")
    print("  pip install requests")
    sys.exit(1)

# Check for API key
print("\n[Step 3] Checking for Facebook/Meta access token...")
access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

if not access_token or access_token == "your-facebook-access-token-here":
    print("✗ FACEBOOK_ACCESS_TOKEN not set or still has default value!")
    print("\nPlease update the .env file with your actual access token:")
    print("  1. Open the .env file in this directory")
    print("  2. Replace 'your-facebook-access-token-here' with your actual Facebook access token")
    sys.exit(1)

print(f"✓ Access token found (starts with: {access_token[:15]}...)")

# Test 1: Debug token to get token info
print("\n[Step 4] Validating access token with Facebook's debug endpoint...")
print("Checking token validity and metadata...")

# Try with SSL verification first, fall back to without if needed
verify_ssl = True
ssl_error_occurred = False

try:
    debug_url = "https://graph.facebook.com/debug_token"
    params = {
        "input_token": access_token,
        "access_token": access_token
    }
    
    try:
        response = requests.get(debug_url, params=params, verify=verify_ssl, timeout=10)
    except requests.exceptions.SSLError as ssl_err:
        print(f"⚠ SSL certificate verification failed, retrying without verification...")
        ssl_error_occurred = True
        verify_ssl = False
        response = requests.get(debug_url, params=params, verify=verify_ssl, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        if "data" in data:
            token_data = data["data"]
            is_valid = token_data.get("is_valid", False)
            
            print("✓ Token debug successful!")
            print(f"\n[Token Details]")
            print(f"  App ID: {token_data.get('app_id', 'N/A')}")
            print(f"  Type: {token_data.get('type', 'N/A')}")
            print(f"  User ID: {token_data.get('user_id', 'N/A')}")
            
            if "expires_at" in token_data and token_data["expires_at"] > 0:
                expiry_timestamp = token_data["expires_at"]
                expiry_date = datetime.fromtimestamp(expiry_timestamp)
                print(f"  Expires at: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"  Expires at: Never (long-lived token)")
            
            if "scopes" in token_data:
                print(f"  Scopes: {', '.join(token_data['scopes'])}")
            
            if is_valid:
                print(f"  Valid: Yes")
            else:
                print(f"  Valid: No")
                print("\n" + "=" * 60)
                print("🔑 KEY VALIDATION STATUS")
                print("=" * 60)
                print("✗ Invalid Secret - Facebook rejected this access token")
                print(f"  Token prefix: {access_token[:15]}...")
                print(f"  Status: INVALID or EXPIRED")
                print("=" * 60)
                sys.exit(1)
        else:
            print("✗ Unexpected response format from debug endpoint")
            sys.exit(1)
    else:
        print(f"✗ Token debug failed with status code: {response.status_code}")
        error_data = response.json()
        if "error" in error_data:
            print(f"  Error: {error_data['error'].get('message', 'Unknown error')}")
        
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✗ Invalid Secret - Facebook rejected this access token")
        print(f"  Token prefix: {access_token[:15]}...")
        print(f"  Status: INVALID or EXPIRED")
        print("=" * 60)
        sys.exit(1)
        
except requests.exceptions.SSLError as e:
    print(f"✗ SSL certificate error: {e}")
    print("\n⚠ SSL Certificate Issue Detected!")
    print("To fix this on macOS, run:")
    print("  /Applications/Python\\ 3.*/Install\\ Certificates.command")
    print("\nOr install certifi:")
    print("  pip install --upgrade certifi")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"✗ Network error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)

if ssl_error_occurred:
    print("\n⚠ Note: SSL verification was bypassed due to certificate issues.")
    print("For security, please fix SSL certificates:")
    print("  /Applications/Python\\ 3.*/Install\\ Certificates.command")

# Test 2: Make a simple API call to /me endpoint
print("\n[Step 5] Making a test API call to /me endpoint...")
print("Fetching basic user/page information...")

try:
    me_url = "https://graph.facebook.com/v18.0/me"
    params = {
        "access_token": access_token,
        "fields": "id,name"
    }
    
    response = requests.get(me_url, params=params, verify=verify_ssl, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print("✓ API call successful!")
        print(f"\n[Response Details]")
        print(f"  ID: {data.get('id', 'N/A')}")
        print(f"  Name: {data.get('name', 'N/A')}")
        
        # Key validation confirmation
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✓ Active Secret - Facebook confirmed this access token is active")
        print(f"  Token prefix: {access_token[:15]}...")
        print(f"  Status: ACTIVE and operational")
        print(f"  Entity: {data.get('name', 'N/A')} (ID: {data.get('id', 'N/A')})")
        print("=" * 60)
    else:
        error_data = response.json()
        print(f"✗ API call failed with status code: {response.status_code}")
        if "error" in error_data:
            print(f"  Error: {error_data['error'].get('message', 'Unknown error')}")
            print(f"  Code: {error_data['error'].get('code', 'N/A')}")
            print(f"  Type: {error_data['error'].get('type', 'N/A')}")
        sys.exit(1)
        
except requests.exceptions.SSLError as e:
    print(f"✗ SSL certificate error: {e}")
    print("\n⚠ SSL Certificate Issue Detected!")
    print("To fix this on macOS, run:")
    print("  /Applications/Python\\ 3.*/Install\\ Certificates.command")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"✗ Network error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)

print("\n✓ All tests passed! Your Facebook/Meta access token is active and working.")

if ssl_error_occurred:
    print("\n⚠ Warning: SSL verification was bypassed. Please install certificates for security.")

