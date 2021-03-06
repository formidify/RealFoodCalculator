'''
    website.py - Python Flask Web Framework
    Code by Real Food Calculator Comps: Bryce Barton, Syd Botz, Chae Kim, Claudia Naughton, James Yang
    Last Updated March 14, 2019

    Code hosts website at http://realfoodnetwork.carleton.edu:2019/rfc_home
    Renders html templates for url endpoints:
        - '/rfc_home' goes renders home.html
        - '/login' renders login.html
        - '/entry_session' renders entry_session.html
        - '/data_entry' renders data_entry.html
        - '/view_download' renders view_download.html
        - '/visualization' renders visualization.html
'''

import flask
from flask import *
import sys
import simplejson as json
import psycopg2
import requests
import config

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

"""
Render html for the home page
"""
@app.route('/rfc_home')
def homepage():
    return render_template('home.html')

"""
Render html for the login page
"""
@app.route('/rfc_login')
def login():
    return render_template("login.html")

"""
Render html for the entry session page
If 'entry-session-form' in entry_session.html is submitted, generate api url to insert items into database.
"""
@app.route('/entry_session', methods=['POST','GET'])
def entrySession():
    labels = ['category','vendor', 'brand','description','notes','productCode', 'cost','local','localDescription', 'fair', 'fairDescription','ecological','ecologicalDescription','humane','humaneDescription','disqualifier','disqualifierDescription']
    api_url = config.api_add_url
    # for each item in entrySessionData, make an API URL to submit item into database
    if request.method == 'POST':
        # result is a dictionary with four items: year, month, rating_version, and entrySessionData
        result = request.form
        for key, value in result.items():
            # entrySessionData is a list of lists where each list is an item with all fields to be inserted
            if (key == 'entrySessionData') and (value != '[]') and (value != ''):
                value = json.loads(value)
                # for each item in entry session, insert into database
                for item in value:
                     api_url_item = api_url
                     index = 0
                     # for each required field of an item, add it to the API URL
                     for category in item:
                         # replace all empty values with keyword "NONE"
                         if category == '':
                             category = 'NONE'
                        # do not allow hash symbols to be put into URL, replace all with %23
                         if isinstance(category, str):
                             category=category.replace("#","%23")
                        # for each label, add its corresponding value for each item
                         api_url_item += (labels[index] + '=' + str(category) + '&')
                         index += 1
                    # add month to URL
                     api_url_item += ('month='+result['month']+'&')
                     # add year to URL
                     api_url_item += ('year='+result['year']+'&')
                     # add rating version to URL
                     api_url_item += ('rating_version='+result['rating_version'])
                     # send URL to API, insert item
                     r = requests.get(api_url_item)
    return render_template('entry_session.html')

"""
Render html for data entry page (this route can only be accessed through entry session)
If 'data-entry-form' in data_entry.html is submitted, generate api url to search for similar items.
Retrieve and display results of api call.
"""
@app.route('/data_entry', methods = ['POST', 'GET'])
def result():
    result =[{}]
    api_url = config.api_q_url
    # create API URL to search for similar items
    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            if (value):
                api_url += (key + '=' + value + '&')
        api_url += 'year=year&orderBy=reverse,year,month'
        # get JSON object from API URL
        r = requests.get(api_url).json()
        # display results to data_entry.html
        return render_template("data_entry.html",result = r)
    return render_template("data_entry.html", result = result)

"""
Render html for the view and download page
NOTE: API URL generation for this page happens in javascript of view_download.html
"""
@app.route('/rfc_view_download')
def viewDownload():
    return render_template("view_download.html")

"""
Render html for the visualization page
NOTE: API URL generation for this page happens in visualization.html
"""
@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

if __name__ == '__main__':
    app.run(host=config.webhost, port=int(config.webport), debug=True)
