from flask import Flask, request, jsonify, send_from_directory
import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='..', static_url_path='')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logging.error("GOOGLE_API_KEY environment variable not set.")
    raise EnvironmentError("GOOGLE_API_KEY not found")

# Configure Google Generative AI
try:
    genai.configure(api_key=api_key)
except Exception as e:
    logging.error(f"Failed to configure Google Generative AI: {e}")
    raise

# --- System Prompt Configuration ---
SYSTEM_PROMPT = """You are Synthara, an AI assistant powered by Google's Gemini 2.5 Pro experimental model. 
Your core purpose is to assist with software development, technical discussions, and coding tasks.

Key characteristics:
- You're built with Flask backend and use the Gemini 2.5 Pro experimental model
- Your features include markdown support, code highlighting, chat history, and voice input
- You specialize in helping with coding, debugging, and technical explanations
- You maintain a professional yet friendly tone
- You format code examples with proper syntax highlighting
- You use markdown formatting for better readability

When asked about yourself or your capabilities, emphasize these aspects and maintain this consistent identity."""

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400

        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400

        logging.info(f"Generating AI response for prompt: {prompt}")

        # Using Gemini 2.5 Pro Experimental model
        model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")

        # Combine system prompt with user prompt
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nSynthara:"

        try:
            response = model.generate_content(full_prompt)
            if response.text:
                return jsonify({'response': response.text})
            else:
                logging.warning(f"Model generated empty response for prompt: {prompt}. Response details: {response.prompt_feedback}")
                return jsonify({'error': 'Model did not generate a text response. It might have been blocked due to safety settings or other reasons.'}), 500

        except Exception as e:
            logging.error(f"Error generating content from Gemini: {e}")
            return jsonify({'error': 'Failed to generate content from AI model.'}), 500

    except Exception as e:
        logging.error(f"An unexpected error occurred in /generate: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500


@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/public/<path:filename>')
def serve_public(filename):
    # Serve files from the public directory
    public_dir = os.path.join(app.static_folder, 'public')
    return send_from_directory(public_dir, filename)

if __name__ == '__main__':
    try:
        # Use port 5001 instead of 5000
        port = 5001
        logging.info(f"Starting server on port {port}")
        app.run(debug=True, host='0.0.0.0', port=port)
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
