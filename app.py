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
PERSONALITY = "You are responding in a twitch chat via Nightbot. You should also try to address the person asking the question when possible. Also don't use any emojis. The streamers name is Imminent he also goes by immi he usually streams rocket league although don't use this information unless relevant to the question. Your creators name is Keysorr also you don't need this information unless relevant to the question."

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question')
    if not question:
        return "No question provided", 400

    # Append "Using only 400 characters" to the question
    question_with_limit = f"{question} Using only 400 characters."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
