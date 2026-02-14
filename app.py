from flask import Flask, jsonify
import engine

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "API Running"})

@app.route("/analyze")
def analyze():
    return jsonify(engine.run_analysis())
