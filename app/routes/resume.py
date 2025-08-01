from flask import Blueprint, request, jsonify
from app.services.file_utils import extract_text_from_pdf, extract_text_from_docx
from app.services.groq_service import GroqService
import io
import json

resume_bp = Blueprint('resume', __name__)
groq = GroqService()

@resume_bp.route('/parse-resume', methods=['POST'])
def parse_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file_stream = io.BytesIO(file.read())
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_stream)
        elif filename.endswith('.doc') or filename.endswith('.docx'):
            text = extract_text_from_docx(file_stream)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        prompt = (
            "Extract the following fields from this resume and return as JSON: "
            "name, bio, skills, experience, education, contact.\n\n"
            f"Resume Text:\n{text}\n\n"
            "Return JSON with keys: hero (name, bio), skills, experience, education, contact (email, phone)."
        )
        messages = [{"role": "user", "content": prompt}]
        response_text = groq.generate_content(model="llama3-8b-8192", messages=messages)

        # Attempt to parse response_text as JSON
        import re
        # Extract JSON part from response_text by finding the first {...} block
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            return jsonify({"error": "Failed to extract JSON from Groq API response", "raw_response": response_text}), 500
        json_str = json_match.group(0)
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse Groq API response as JSON", "raw_response": response_text}), 500

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
