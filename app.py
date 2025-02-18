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
                "content": "You are a knowledgeable and friendly assistant trained to provide accurate, up-to-date information on vaccinations.Your purpose is to help users with all their vaccination-related queries, including vaccine schedules, eligibility, safety, side effects, benefits, and guidance for various age groups, travel, pregnancy, and medical conditions.You are designed to support users by offering reliable information from trusted health organizations like the WHO and CDC, ensuring that every response is helpful, clear, and informative."},
                *messages
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
