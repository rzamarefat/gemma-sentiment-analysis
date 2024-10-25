from flask import Flask, request, jsonify
from flask_cors import CORS
from GemmaSentiment import GemmaSentiment


app = Flask(__name__)
CORS(app)  

llm = GemmaSentiment(r"C:\Users\ASUS\Desktop\github_projects\gemma-sent-analysis\outputs\checkpoint-224")


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    input_text = data.get('text', '')
    res = llm.infer(input_text) 
    return jsonify({"sentiment": res})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
