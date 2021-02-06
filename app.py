import os
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from filters import filter_list

load_dotenv()

app = Flask(__name__)

API_info = {
    'x-rapidapi-key': "SIGN-UP-FOR-KEY",
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }

@app.route('/')
def main():
    pass


if __name__ == '__main__':
    app.run(debug=True)