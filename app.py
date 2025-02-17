from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key and model ID from .env
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("MODEL_ID")


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})


@app.route('/get_vaccine_info', methods=['POST'])
def get_vaccine_info():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages or not isinstance(messages, list):
        return jsonify({
            "error": "Missing or invalid 'messages' array in request body"}), 400

    try:
        response = openai.chat.completions.create(
            model=model_id,
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant providing vaccination information."},
                *messages
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
