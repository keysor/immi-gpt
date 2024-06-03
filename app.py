from flask import Flask, request
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

# Define the AI's personality
PERSONALITY = "You are responding through Nightbot the twitch moderator. The questions will be asked from users. Your job is to make people enjoy their stay so try to be a little quirky."

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question')
    if not question:
        return "No question provided", 400

    # Append "Using only 400 characters" to the question
    question_with_limit = f"{question} Using only 400 characters."

    try:
        response = openai.ChatCompletion.create(
            engine="gpt-3.5-turbo-instruct",
            messages=[
                {"role": "system", "content": PERSONALITY},
                {"role": "user", "content": question_with_limit},
            ],
            max_tokens=100,
        )
        # Extract the response content
        answer = response.choices[0].message['content'].strip()[:MAX_RESPONSE_CHARS]
        return answer
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Use Gunicorn as the production server
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
