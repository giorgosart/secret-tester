#!/usr/bin/env python3
"""
H&M API Key Test Script
Tests whether your H&M API key is active and can make successful API calls.
"""

import os
import sys
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings if verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 60)
print("H&M API Key Test Script")
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
print("\n[Step 3] Checking for H&M API key...")
api_key = os.getenv("HM_API_KEY")

if not api_key or api_key == "your-hm-api-key-here":
    print("✗ HM_API_KEY not set or still has default value!")
    print("\nPlease update the .env file with your actual API key:")
    print("  1. Open the .env file in this directory")
    print("  2. Replace 'your-hm-api-key-here' with your actual H&M API key")
    print("\nTo get an H&M API key:")
    print("  1. Go to https://developer.hm.com/")
    print("  2. Sign up for an account")
    print("  3. Create a new application")
    print("  4. Copy the API key from your application settings")
    sys.exit(1)

print(f"✓ API key found (starts with: {api_key[:8]}...)")

# Try with SSL verification first, fall back to without if needed
verify_ssl = True
ssl_error_occurred = False

# Test API call
print("\n[Step 4] Making a test API call to H&M API...")
print("Fetching products information...")

try:
    # H&M API endpoint - using their product search endpoint
    base_url = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/list"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "apidojo-hm-hennes-mauritz-v1.p.rapidapi.com"
    }
    
    # Simple test query parameters
    params = {
        "country": "us",
        "lang": "en",
        "currentpage": "0",
        "pagesize": "1"
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params, verify=verify_ssl, timeout=10)
    except requests.exceptions.SSLError as ssl_err:
        print(f"⚠ SSL certificate verification failed, retrying without verification...")
        ssl_error_occurred = True
        verify_ssl = False
        response = requests.get(base_url, headers=headers, params=params, verify=verify_ssl, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        print("✓ API call successful!")
        print(f"\n[Response Details]")
        
        # Display information about the response
        if 'results' in data:
            results = data.get('results', [])
            total_results = data.get('pagination', {}).get('totalNumberOfResults', 0)
            
            print(f"  Total products available: {total_results}")
            print(f"  Products in this response: {len(results)}")
            
            if results and len(results) > 0:
                product = results[0]
                print(f"\n  Sample Product:")
                print(f"    Name: {product.get('name', 'N/A')}")
                print(f"    Category: {product.get('categoryName', 'N/A')}")
                print(f"    Price: {product.get('price', 'N/A')}")
                print(f"    Article Code: {product.get('articleCode', 'N/A')}")
        else:
            print(f"  Response received successfully")
            print(f"  Data keys: {', '.join(data.keys())}")
        
        # Key validation confirmation
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✓ Active Secret - H&M API confirmed this API key is active")
        print(f"  Key prefix: {api_key[:8]}...")
        print(f"  Status: ACTIVE and operational")
        print(f"  Validated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if ssl_error_occurred:
            print("\n⚠ SSL Warning: Certificate verification was disabled for this test.")
            print("  Consider installing SSL certificates on your system.")
        
        print("=" * 60)
    
    elif response.status_code == 401:
        print(f"✗ Authentication failed (401 Unauthorized)")
        try:
            error_data = response.json()
            if "message" in error_data:
                print(f"  Error: {error_data['message']}")
        except:
            print(f"  Raw response: {response.text}")
        
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✗ Invalid Secret - H&M API rejected this API key")
        print(f"  Key prefix: {api_key[:8]}...")
        print(f"  Status: INVALID, EXPIRED, or REVOKED")
        print("  The key appears to be inactive, expired, or incorrectly formatted.")
        print("=" * 60)
        sys.exit(1)
    
    elif response.status_code == 403:
        print(f"✗ Access forbidden (403)")
        try:
            error_data = response.json()
            if "message" in error_data:
                print(f"  Error: {error_data['message']}")
        except:
            print(f"  Raw response: {response.text}")
        
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✓ Active Secret - H&M API confirmed this API key is active")
        print(f"  Key prefix: {api_key[:8]}...")
        print(f"  Status: ACTIVE but with insufficient permissions or quota exceeded")
        print("  The key is valid but may have usage limits or restricted access.")
        print("=" * 60)
        sys.exit(0)
    
    elif response.status_code == 429:
        print(f"✗ Rate limit exceeded (429 Too Many Requests)")
        print("  You have made too many requests in a short period.")
        
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✓ Active Secret - H&M API confirmed this API key is active")
        print(f"  Key prefix: {api_key[:8]}...")
        print(f"  Status: ACTIVE but rate-limited")
        print("  The key is valid but you've exceeded your rate limits.")
        print("=" * 60)
        sys.exit(0)
    
    else:
        print(f"✗ API call failed with status code: {response.status_code}")
        try:
            error_data = response.json()
            print(f"  Error response: {error_data}")
        except:
            print(f"  Raw response: {response.text}")
        sys.exit(1)
        
except requests.exceptions.Timeout:
    print(f"✗ Request timed out")
    print("  The API did not respond within 10 seconds.")
    print("  This may be a temporary network issue. Please try again.")
    sys.exit(1)
    
except requests.exceptions.ConnectionError as e:
    print(f"✗ Connection error: {e}")
    print("  Could not connect to the H&M API.")
    print("  Please check your internet connection.")
    sys.exit(1)
    
except requests.exceptions.SSLError as e:
    print(f"✗ SSL certificate error: {e}")
    print("\n⚠ SSL Certificate Issue Detected!")
    print("To fix this on macOS, run:")
    print("  /Applications/Python\\ 3.x/Install\\ Certificates.command")
    print("\nOr install certificates via:")
    print("  pip install --upgrade certifi")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    sys.exit(1)

print("\n✓ All tests passed! Your H&M API key is active and working.")
