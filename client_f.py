from flask import Flask, request, jsonify
import asyncio
from g4f.client import Client

# Create Flask app
app = Flask(__name__)

# Setup event loop for Windows
def setup_event_loop():
    if asyncio.get_event_loop_policy().__class__.__name__ != "WindowsSelectorEventLoopPolicy":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Function to get chat response
def get_chat_response(messages, model="gpt-4o-mini"):
    client = Client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # Add other parameters if needed
    )
    return response.choices[0].message.content

# Flask route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-4o-mini')

        # Ensure setup for event loop
        setup_event_loop()

        # Get response from chat model
        response_content = get_chat_response(messages, model)
        
        # Return JSON response
        return jsonify({"response": response_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
