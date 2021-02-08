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

@app.route('/process-filters', methods=['POST'])
def process():
    title_type = request.form['type']
    start_year = request.form['start+year']
    order_by = request.form['order_by']
    audiosubtitle_andor = request.form['audiosubtitle_andor']
    start_rating = request.form['start_rating']
    end_rating = request.form['end_rating']
    subtitle = request.form['subtitle']
    country_list = request.form['country_list']
    audio = request.form['audio']
    country_andorunique = request.form['country_andorunique']
    end_year = request.form['end_year']
    current_list = request.form['current_list']



if __name__ == '__main__':
    app.run(debug=True)