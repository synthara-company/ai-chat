## Tech Specs

This application utilizes the following core technologies:

*   **Backend Framework:** [Flask](https://flask.palletsprojects.com/) - A lightweight WSGI web application framework in Python used to build the web server and API endpoints.
*   **Programming Language:** [Python 3](https://www.python.org/)
*   **AI Model Integration:** [Google Generative AI SDK for Python](https://github.com/google/generative-ai-python) (`google-generativeai`) - Used to interact with Google's Generative AI models (specifically configured for a Gemini model like `gemini-1.5-pro-latest` in the example).
*   **Environment Variable Management:** [python-dotenv](https://github.com/theskumar/python-dotenv) - Used to load environment variables (like API keys) from a `.env` file into the application's environment.
*   **API Endpoint:**
    *   `/generate` (POST): Accepts a JSON payload with a `prompt` key and returns a JSON response containing the AI-generated text or a predefined response.
*   **Frontend Serving:** Flask's built-in static file serving (`send_from_directory`) is used to serve the main `index.html` file (expected to be in the parent directory `../`).
*   **Data Format:** JSON is used for communication between the frontend and the backend API endpoint (`/generate`).
*   **Standard Libraries:** Uses Python's built-in `os` (for environment variables/paths) and `logging` modules.
