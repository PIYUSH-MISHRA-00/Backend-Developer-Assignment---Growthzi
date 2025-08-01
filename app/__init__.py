from flask import Flask, send_from_directory
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))
    CORS(app)

    # Import and register Blueprints
    from app.routes.resume import resume_bp
    from app.routes.translate import translate_bp
    from app.routes.pricing import pricing_bp
    from app.routes.facebook import facebook_bp

    app.register_blueprint(resume_bp, url_prefix='/api')
    app.register_blueprint(translate_bp, url_prefix='/api')
    app.register_blueprint(pricing_bp, url_prefix='/api')
    app.register_blueprint(facebook_bp, url_prefix='/api/facebook')

    # Serve frontend static files
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    return app
