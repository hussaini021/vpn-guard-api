from flask import Flask, jsonify
import vpn2
app = Flask(__name__)

@app.route("/")
def home():
    return "Server OK"

@app.route("/analyze")
def analyze():
    return jsonify({"status": "started"})
