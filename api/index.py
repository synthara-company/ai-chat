from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging # Added for better error logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='../')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logging.error("GOOGLE_API_KEY environment variable not set.")
    # Depending on your deployment, you might want to exit or handle this differently
    # For now, we'll let it potentially fail later during genai.configure
    pass # Or raise EnvironmentError("GOOGLE_API_KEY not found")

try:
    genai.configure(api_key=api_key)
except Exception as e:
    logging.error(f"Failed to configure Google Generative AI: {e}")
    # Handle configuration error appropriately

# --- Predefined Responses ---
# Using a dictionary for cleaner management of predefined responses
predefined_responses = {
    "Who are you?": "I'm an AI assistant created by Synthara. How can I help you today?",
    "Can you help me?": "That's an interesting question. Let me think about it...\n\nThere are several ways to approach this problem:\n\n1. First, you could consider...\n2. Alternatively, you might want to...\n3. Many experts recommend...",
    "What is your purpose?": "My purpose is to assist you with information and tasks to the best of my ability.",
    "Tell me a joke.": "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Show me a code example.": "Here's a code example that might help:\n\n```javascript\nfunction calculateTotal(items) {\n  return items.reduce((sum, item) => sum + item.price, 0);\n}\n```",
    "Can you break this down?": "Let me break this down into steps:\n\n## Step 1: Understand the problem\nBefore diving into solutions, it's important to fully understand what we're trying to solve.\n\n## Step 2: Consider the options\nThere are multiple approaches we could take here..."
}

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json() # Use get_json() for better error handling
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400

        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400

        # Check if the prompt matches any predefined response (case-sensitive)
        if prompt in predefined_responses:
            logging.info(f"Serving predefined response for prompt: {prompt}")
            return jsonify({'response': predefined_responses[prompt]})

        # --- If not predefined, call the Generative AI model ---
        logging.info(f"Generating AI response for prompt: {prompt}")

        # Consider using a more standard or available model if needed, e.g., "gemini-1.5-pro-latest"
        # The model name "gemini-2.5-pro-exp-03-25" might be experimental or require specific access.
        model = genai.GenerativeModel("gemini-1.5-pro-latest") # Changed to a more common model, adjust if needed

        # Add error handling for the API call
        try:
            response = model.generate_content(prompt)
            # Check if the response has text content
            if response.text:
                 return jsonify({'response': response.text})
            else:
                 # Handle cases where the model might return no text (e.g., safety blocks)
                 logging.warning(f"Model generated empty response for prompt: {prompt}. Response details: {response.prompt_feedback}")
                 # You might want to return a generic message or details about why content wasn't generated
                 return jsonify({'error': 'Model did not generate a text response. It might have been blocked due to safety settings or other reasons.'}), 500

        except Exception as e:
            logging.error(f"Error generating content from Gemini: {e}")
            return jsonify({'error': 'Failed to generate content from AI model.'}), 500

    except Exception as e:
        logging.error(f"An unexpected error occurred in /generate: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500


@app.route('/')
def serve_frontend():
    # Ensure the static folder and index.html exist relative to the script's location
    static_dir = os.path.abspath(app.static_folder)
    index_path = os.path.join(static_dir, 'index.html')
    logging.info(f"Serving static folder: {static_dir}")
    logging.info(f"Attempting to serve index.html from: {index_path}")

    if not os.path.isdir(static_dir):
         logging.error(f"Static folder not found: {static_dir}")
         return "Error: Static folder not found.", 500
    if not os.path.isfile(index_path):
         logging.error(f"index.html not found in static folder: {index_path}")
         return "Error: index.html not found.", 404

    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    try:
        # Use port 5001 instead of 5000
        port = 5001
        logging.info(f"Starting server on port {port}")
        app.run(debug=True, host='0.0.0.0', port=port)
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
