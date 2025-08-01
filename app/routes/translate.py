from flask import Blueprint, request, jsonify
from app.services.groq_service import GroqService
import json

translate_bp = Blueprint('translate', __name__)
groq = GroqService()

@translate_bp.route('/translate-content', methods=['POST'])
def translate_content():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON input"}), 400
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400
    content = data.get('content')
    target_lang = data.get('target_lang')
    if not content or not target_lang:
        return jsonify({"error": "Both 'content' and 'target_lang' are required"}), 400

    try:
        prompt = (
            f"Translate this JSON content into {target_lang}. Keep keys intact and only translate values.\n\n"
            f"Content:\n{json.dumps(content, ensure_ascii=False)}\n\n"
            "Output the translated JSON."
        )
        messages = [{"role": "user", "content": prompt}]
        response_text = groq.generate_content(model="llama3-8b-8192", messages=messages)

        import re
        # Extract JSON part from response_text by finding the first {...} block
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            return jsonify({"error": "Failed to extract JSON from Groq API response", "raw_response": response_text}), 500
        json_str = json_match.group(0)
        try:
            translated_json = json.loads(json_str)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse Groq API response as JSON", "raw_response": response_text}), 500

        return jsonify(translated_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
