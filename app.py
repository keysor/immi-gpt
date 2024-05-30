from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if running locally

app = Flask(__name__)

# Set your OpenAI API key from an environment variable for security
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=100
        )
        answer = response.choices[0].text.strip()
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)  # Make sure debug is False for production



