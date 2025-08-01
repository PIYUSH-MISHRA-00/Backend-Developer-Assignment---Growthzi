import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Read the API key
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("❌ GROQ_API_KEY not found. Check your .env file.")
    exit()

# GROQ API endpoint for OpenAI-compatible models (like llama3)
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# A simple test prompt
payload = {
    "model": "llama3-8b-8192",  # or llama3-70b-8192
    "messages": [
        {"role": "user", "content": "Hello! Can you confirm you're responding correctly?"}
    ],
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)

try:
    data = response.json()
    if response.status_code == 200:
        print("✅ API key is valid! Response:")
        print(data['choices'][0]['message']['content'])
    elif response.status_code == 401:
        print("❌ Unauthorized – likely due to an invalid or expired API key.")
    else:
        print("⚠️ Unexpected response:", data)
except Exception as e:
    print("❌ Failed to parse JSON:", response.text)
