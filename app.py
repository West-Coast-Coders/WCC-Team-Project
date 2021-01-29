import os
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def main():
    pass

if __name__ == '__main__':
    app.run(debug=True)