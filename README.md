# Backend Developer Assignment - Growthzi

## Project Overview

This project is a modular Flask backend system implementing the following features:

- Resume to Portfolio JSON API using PDF/DOC parsing and Groq AI API
- Multilingual Website Content Translation API using Groq AI API
- Currency Conversion API with hardcoded rates
- Facebook Growth AI Agent with content idea generation, content planner, post preview/edit, and simulated publishing

A simple HTML + CSS + JavaScript frontend is included for testing the APIs.

## Tech Stack

- Python 3.11+
- Flask, Flask-CORS
- google-generativeai (replaced with Groq API)
- pdfminer.six, python-docx
- python-dotenv
- Simple HTML + CSS + JS frontend for testing

## Setup Instructions

1. Clone the repository.

2. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/macOS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_real_groq_api_key_here
```

5. Run the Flask app:

```bash
python run.py
```

6. Open your browser and navigate to `http://localhost:5000` to access the frontend testing page.

## API Endpoints

- `POST /api/parse-resume` - Upload PDF/DOC resume to extract portfolio JSON.
- `POST /api/translate-content` - Translate JSON content to target language.
- `GET /api/price?country=US` - Get product price in local currency.
- Facebook Growth AI Agent:
  - `POST /api/facebook/ideas` - Generate business tips, promotions, industry insights.
  - `POST /api/facebook/planner` - Generate Facebook post calendar.
  - `GET /api/facebook/posts` - Get generated posts.
  - `PUT /api/facebook/posts/{id}` - Update a post.
  - `POST /api/facebook/publish` - Simulate publishing a post.

## Testing

- Use the included `static/index.html` frontend to test API calls.
- Postman collection is provided in `postman_collection.json` for API testing.

## Notes

- The Groq API is used for AI content generation.
- JSON extraction from Groq responses is robust to handle extra formatting.
- Posts are stored in-memory for simplicity.
- Error handling is implemented for missing or invalid inputs.
