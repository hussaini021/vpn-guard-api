from flask import Flask, jsonify
import engine

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "name": "VPN Guard Pro",
        "status": "API Running"
    })

@app.route("/analyze")
def analyze():
    return jsonify(engine.run_analysis())
