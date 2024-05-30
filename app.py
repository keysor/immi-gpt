from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from an environment variable for security
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Define the maximum number of characters for the response
MAX_RESPONSE_CHARS = 400

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        response =openai.ChatCompletion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=question,
            max_tokens=100,
        )
        # Truncate the response to the maximum number of characters
        answer = response.choices[0].text.strip()[:MAX_RESPONSE_CHARS]
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use Gunicorn as the production server
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
