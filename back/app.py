# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow requests from React frontend

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    input_text = data.get('text', '')
    # Process the input_text as needed
    print(f"Received input text: {input_text}")
    return jsonify({"message": "Text received!", "received_text": input_text})

if __name__ == '__main__':
    app.run(debug=True)
