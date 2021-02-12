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


# FILTERS TESTING:
# @app.route('/process-filters', methods=['POST'])
# def process():
#     title_type = request.form['type']
#     start_year = request.form['start_year']
#     order_by = request.form['order_by']
#     audiosubtitle_andor = request.form['audiosubtitle_andor']
#     start_rating = request.form['start_rating']
#     end_rating = request.form['end_rating']
#     subtitle = request.form['subtitle']
#     country_list = request.form['country_list']
#     audio = request.form['audio']
#     country_andorunique = request.form['country_andorunique']
#     end_year = request.form['end_year']
#     current_list = request.form['current_list']

#     filters = {
#         "type":title_type
#         "start_year":start_year,
#         "orderby":order_by,
#         "audiosubtitle_andor":audiosubtitle_andor,
#         "start_rating":start_rating,
#         "end_rating":end_rating,
#         "subtitle":"english",
#         "countrylist":country_list,
#         "audio":audio,
#         "country_andorunique":country_andorunique,
#         "end_year":end_year
#     }



if __name__ == '__main__':
    app.run(debug=True)