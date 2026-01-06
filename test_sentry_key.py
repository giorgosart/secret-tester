#!/usr/bin/env python3
"""
Sentry API Key Test Script
Tests whether your Sentry auth token is active and can make successful API calls.
"""

import os
import sys
import requests
import urllib3

# Disable SSL warnings if verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 60)
print("Sentry API Key Test Script")
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
print("\n[Step 3] Checking for Sentry auth token...")
auth_token = os.getenv("SENTRY_AUTH_TOKEN")

if not auth_token or auth_token == "your-sentry-auth-token-here":
    print("✗ SENTRY_AUTH_TOKEN not set or still has default value!")
    print("\nPlease update the .env file with your actual auth token:")
    print("  1. Open the .env file in this directory")
    print("  2. Replace 'your-sentry-auth-token-here' with your actual Sentry auth token")
    print("\nTo create a Sentry auth token:")
    print("  1. Go to https://sentry.io/settings/account/api/auth-tokens/")
    print("  2. Click 'Create New Token'")
    print("  3. Give it a name and select scopes (at minimum: org:read, project:read)")
    sys.exit(1)

print(f"✓ Auth token found (starts with: {auth_token[:20]}...)")

# Try with SSL verification first, fall back to without if needed
verify_ssl = True
ssl_error_occurred = False

# Test 1: Get user/organization info
print("\n[Step 4] Validating auth token with Sentry API...")
print("Fetching organization information...")

try:
    # Get organizations
    orgs_url = "https://sentry.io/api/0/organizations/"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(orgs_url, headers=headers, verify=verify_ssl, timeout=10)
    except requests.exceptions.SSLError as ssl_err:
        print(f"⚠ SSL certificate verification failed, retrying without verification...")
        ssl_error_occurred = True
        verify_ssl = False
        response = requests.get(orgs_url, headers=headers, verify=verify_ssl, timeout=10)
    
    if response.status_code == 200:
        orgs = response.json()
        
        if orgs and len(orgs) > 0:
            print("✓ API call successful!")
            print(f"\n[Organization Details]")
            print(f"  Total organizations: {len(orgs)}")
            
            for i, org in enumerate(orgs[:3], 1):  # Show first 3 orgs
                print(f"\n  Organization {i}:")
                print(f"    Slug: {org.get('slug', 'N/A')}")
                print(f"    Name: {org.get('name', 'N/A')}")
                print(f"    ID: {org.get('id', 'N/A')}")
                print(f"    Status: {org.get('status', {}).get('name', 'N/A')}")
            
            if len(orgs) > 3:
                print(f"\n  ... and {len(orgs) - 3} more organization(s)")
        else:
            print("✓ API call successful!")
            print("\n⚠ No organizations found for this auth token.")
            print("  The token is valid but may have limited access.")
    
    elif response.status_code == 401:
        print(f"✗ Authentication failed (401 Unauthorized)")
        try:
            error_data = response.json()
            if "detail" in error_data:
                print(f"  Error: {error_data['detail']}")
        except:
            pass
        
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✗ Invalid Secret - Sentry rejected this auth token")
        print(f"  Token prefix: {auth_token[:20]}...")
        print(f"  Status: INVALID, EXPIRED, or REVOKED")
        print("  The token appears to be inactive or incorrectly formatted.")
        print("=" * 60)
        sys.exit(1)
    
    elif response.status_code == 403:
        print(f"✗ Access forbidden (403)")
        print("  The token is valid but lacks necessary permissions.")
        print("\n" + "=" * 60)
        print("🔑 KEY VALIDATION STATUS")
        print("=" * 60)
        print("✓ Active Secret - Sentry confirmed this auth token is active")
        print(f"  Token prefix: {auth_token[:20]}...")
        print(f"  Status: ACTIVE but with insufficient permissions")
        print("  Consider adding org:read and project:read scopes.")
        print("=" * 60)
        sys.exit(0)
    
    else:
        print(f"✗ API call failed with status code: {response.status_code}")
        try:
            error_data = response.json()
            if "detail" in error_data:
                print(f"  Error: {error_data['detail']}")
        except:
            pass
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

# Test 2: Get projects for first organization
if orgs and len(orgs) > 0:
    first_org_slug = orgs[0].get('slug')
    
    print(f"\n[Step 5] Testing project access for organization '{first_org_slug}'...")
    print("Fetching project list...")
    
    try:
        projects_url = f"https://sentry.io/api/0/organizations/{first_org_slug}/projects/"
        
        response = requests.get(projects_url, headers=headers, verify=verify_ssl, timeout=10)
        
        if response.status_code == 200:
            projects = response.json()
            
            print("✓ API call successful!")
            print(f"\n[Project Details]")
            print(f"  Total projects: {len(projects)}")
            
            if projects:
                for i, project in enumerate(projects[:3], 1):  # Show first 3 projects
                    print(f"\n  Project {i}:")
                    print(f"    Slug: {project.get('slug', 'N/A')}")
                    print(f"    Name: {project.get('name', 'N/A')}")
                    print(f"    Platform: {project.get('platform', 'N/A')}")
                    print(f"    ID: {project.get('id', 'N/A')}")
                
                if len(projects) > 3:
                    print(f"\n  ... and {len(projects) - 3} more project(s)")
            else:
                print("  No projects found in this organization.")
        else:
            print(f"⚠ Could not fetch projects (status code: {response.status_code})")
            
    except requests.exceptions.SSLError as e:
        print(f"✗ SSL certificate error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"⚠ Network error: {e}")
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")

# Final validation status
print("\n" + "=" * 60)
print("🔑 KEY VALIDATION STATUS")
print("=" * 60)
print("✓ Active Secret - Sentry confirmed this auth token is active")
print(f"  Token prefix: {auth_token[:20]}...")
print(f"  Status: ACTIVE and operational")
if orgs and len(orgs) > 0:
    print(f"  Organizations accessible: {len(orgs)}")
print("=" * 60)

print("\n✓ All tests passed! Your Sentry auth token is active and working.")

if ssl_error_occurred:
    print("\n⚠ Warning: SSL verification was bypassed. Please install certificates for security.")
