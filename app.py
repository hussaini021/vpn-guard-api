from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Server OK"

@app.route("/analyze")
def analyze():
    return jsonify({"status": "started"})
