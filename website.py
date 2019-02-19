'''
   Connects python and RFC html using flask
'''
import flask
#from flask import Flask, render_template, jsonify
from flask import *
import sys
import simplejson as json
import psycopg2
import requests

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/entry_session', methods=['POST','GET'])
def entrySession():
    api_url = 'http://cmc307-06.mathcs.carleton.edu:5001/test_data_large?'
    if request.method == 'POST':
        result = request.form
        print(result)
    return render_template('entry_session.html')

@app.route('/view_download') #, methods = ['POST', 'GET'])
def viewDownload():

    """
    if request.method == 'POST':
        result = request.form
        result = api.get_products()
        description = "Showing all information"

        return render_template('view_download_data.html', result = result, description = description)
    """
    return render_template("view_download.html")

@app.route('/data_entry', methods = ['POST', 'GET'])
def result():
    result =[ {"description": "test description"}]
    api_url = 'http://cmc307-06.mathcs.carleton.edu:5001/test_data_large?'

    if request.method == 'POST':
        result = request.form
        #result = request.form.get('description', 'default_description')
        print("This is request.form.get: ")
        print(result)
        for key, value in result.items():
            print('Key:', key)
            print('Value:', value)
            if (value):
                api_url += (key + '=' + value + '&')
        api_url += 'year=year'
        print(api_url)
        r = requests.get(api_url).json()
        print(r)
        # print(json.loads(r.text))
        return render_template("data_entry.html",result = r)

    return render_template("data_entry.html", result = result, clear = True, disqualifier="on")


@app.route('/visualization')
def visualization():
    return render_template('visualization.html')


if __name__ == '__main__':
#    if len(sys.argv) != 3:
#        print('Usage: {0} host port'.format(sys.argv[0]))
#        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
#        exit()
#
    host = 'cmc307-06.mathcs.carleton.edu'
#    port = int(sys.argv[2])
#   PUT LOCALHOST HERE FOR TESTING - CHAE
    app.run(host="localhost", port=2019, debug=True)
