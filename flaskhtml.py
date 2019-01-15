'''
   Connects python and RFC html using flask
'''
import flask
#from flask import Flask, render_template, jsonify
from flask import *
import sys
import simplejson as json
import psycopg2

#import other flask file
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/entrysession')
def entrySession():
    return render_template('entry_session.html')

@app.route('/viewdownload', methods = ['POST', 'GET'])
def viewDownload():

    if request.method == 'POST':
        result = request.form
        result = api.get_products()
        description = "Showing all information"

        return render_template('view_download_data.html', result = result, description = description)

@app.route('/dataentry')
def dataEntry():
    return render_template('data-entry.html')

@app.route('/visualization')
def visualization():
    return render_template('visualization_page.html')


if __name__ == '__main__':
#    if len(sys.argv) != 3:
#        print('Usage: {0} host port'.format(sys.argv[0]))
#        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
#        exit()
#
    host = 'cmc307-06.mathcs.carleton.edu'
#    port = int(sys.argv[2])
    
    app.run(host=host, port=2019,  debug=True)
