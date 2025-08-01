from flask import Blueprint, request, jsonify
from app.services.groq_service import GroqService
import json, re

facebook_bp = Blueprint('facebook', __name__)
groq = GroqService()

# In-memory posts store
posts_store = {}
post_id_counter = 1

def extract_json_from_response(text: str):
    """
    Strip markdown backticks, then extract the first {...} JSON object.
    Return a Python dict or None if parsing fails.
    """
    # remove triple-backticks
    cleaned = re.sub(r'```(?:json)?', '', text).strip()
    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Fallback: find first {...}
    match = re.search(r'(\{.*\})', cleaned, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

@facebook_bp.route('/ideas', methods=['POST'])
def generate_ideas():
    global post_id_counter
    data = request.get_json() or {}
    website = data.get('website_url')
    industry = data.get('industry', '')

    if not website:
        return jsonify(error="`website_url` is required"), 400

    # Force JSON output
    prompt = (
        f"Generate **only** valid JSON** with keys `business_tips`, `promotions`, "
        f"and `industry_insights` (each a list of objects) for a business with "
        f"website `{website}` and industry `{industry}`."
    )
    messages = [{"role": "user", "content": prompt}]
    resp_text = groq.generate_content(model="llama3-8b-8192", messages=messages)

    ideas = extract_json_from_response(resp_text)
    if ideas is None:
        return jsonify(error="Failed to extract JSON", raw_response=resp_text), 500

    # store each item in posts_store
    for category in ("business_tips", "promotions", "industry_insights"):
        for item in ideas.get(category, []):
            posts_store[post_id_counter] = {
                "id": post_id_counter,
                "category": category,
                "content": item
            }
            post_id_counter += 1

    return jsonify(ideas), 200

@facebook_bp.route('/planner', methods=['POST'])
def content_planner():
    data = request.get_json() or {}
    freq = data.get('frequency')
    tone = data.get('tone')
    mix = data.get('post_mix')

    if not (freq and tone and mix):
        return jsonify(error="`frequency`, `tone`, and `post_mix` are required"), 400

    prompt = (
        f"Generate **only** valid JSON** for a Facebook post calendar of {freq} posts/week. "
        f"Tone: `{tone}`. Types: {', '.join(mix)}. Include dates and content."
    )
    messages = [{"role": "user", "content": prompt}]
    resp_text = groq.generate_content(model="llama3-8b-8192", messages=messages)

    planner = extract_json_from_response(resp_text)
    if planner is None:
        return jsonify(error="Failed to extract JSON", raw_response=resp_text), 500

    return jsonify(planner), 200

@facebook_bp.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(list(posts_store.values())), 200

@facebook_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = posts_store.get(post_id)
    if not post:
        return jsonify(error="Post not found"), 404
    data = request.get_json() or {}
    new_content = data.get('content')
    if not new_content:
        return jsonify(error="`content` is required"), 400
    post['content'] = new_content
    return jsonify(post), 200

@facebook_bp.route('/publish', methods=['POST'])
def publish_post():
    data = request.get_json() or {}
    pid = data.get('id')
    content = data.get('content')

    if pid:
        post = posts_store.get(pid)
        if not post:
            return jsonify(error="Post not found"), 404
        content = post['content']

    if not content:
        return jsonify(error="`content` is required"), 400

    # Simulate publish
    print(f"🔔 Published: {content}")
    return jsonify(message="Post published (simulated)"), 200
