# API Key Test Scripts

Simple Python scripts to test whether your API keys are active and can make successful API calls.

## Available Tests

- **OpenAI API** - `test_openai_key.py`
- **Facebook/Meta API** - `test_facebook_key.py`
- **Sentry API** - `test_sentry_key.py`

## Setup

1. **Install required packages:**
   ```bash
   pip install openai python-dotenv requests
   ```

2. **Configure your API keys:**
   - Open the `.env` file in this directory
   - Replace `your-openai-api-key-here` with your actual OpenAI API key
   - Replace `your-facebook-access-token-here` with your actual Facebook/Meta access token
   - Replace `your-sentry-auth-token-here` with your actual Sentry auth token

3. **Run the tests:**
   ```bash
   # Test OpenAI API key
   python test_openai_key.py
   
   # Test Facebook/Meta access token
   python test_facebook_key.py
   
   # Test Sentry auth token
   python test_sentry_key.py
   ```

## What the scripts do

### OpenAI Test Script
Performs the following checks with detailed console logging:
1. Loads environment variables from the `.env` file
2. Checks if the OpenAI package is installed
3. Verifies your API key is configured
4. Initializes the OpenAI client
5. Makes a test API call using GPT-3.5-turbo
6. Displays response details including tokens used
7. Shows "Active Secret" validation status (like GitHub Advanced Security)

### Facebook/Meta Test Script
Performs the following checks with detailed console logging:
1. Loads environment variables from the `.env` file
2. Checks if the requests package is installed
3. Verifies your access token is configured
4. Validates token using Facebook's debug endpoint
5. Displays token metadata (app ID, type, expiration, scopes)
6. Makes a test API call to the /me endpoint
7. Shows "Active Secret" validation status (like GitHub Advanced Security)

### Sentry Test Script
Performs the following checks with detailed console logging:
1. Loads environment variables from the `.env` file
2. Checks if the requests package is installed
3. Verifies your auth token is configured
4. Validates token by fetching organizations
5. Displays organization details (slug, name, ID, status)
6. Makes a test API call to fetch projects
7. Shows "Active Secret" validation status (like GitHub Advanced Security)

## Security Note

The `.env` file keeps your API key secure and separate from your code. Never commit the `.env` file to version control.
