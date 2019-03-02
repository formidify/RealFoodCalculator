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
    print("Rendering Entry Session")
    labels = ['category','vendor', 'brand','description','notes','productCode', 'cost','local','localDescription', 'fair', 'fairDescription','ecological','ecologicalDescription','humane','humaneDescription','disqualifier','disqualifierDescription']
    api_url = 'http://cmc307-06.mathcs.carleton.edu:5001/add_entry?'
    if request.method == 'POST':
        print("in post")
        result = request.form
        for key, value in result.items():
            if (key == 'entrySessionData') and (value != '[]') and (value != ''):
                value = json.loads(value)
                for item in value:
                     api_url_item = api_url
                     index = 0
                     for category in item:
                         #index = item.index(category)
                         print("Index", index)
                         if category == '':
                             category = 'NONE'
                         print("labels[index]", labels[index], category)
                         print("type of category: ", type(category))
                         if isinstance(category, str):
                             category=category.replace("#","%23")
                             print("Replaced pound:", category)
                         api_url_item += (labels[index] + '=' + str(category) + '&')
                         index += 1
                     api_url_item += ('month='+result['month']+'&')
                     api_url_item += ('year='+result['year']+'&')
                     api_url_item += ('rating_version='+result['rating_version'])
                     r = requests.get(api_url_item)
                     print("API URL IN WEBSITE:", api_url_item)
                     print(r)

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
    result =[{}]
    formData = {"category": "dairy"}
    api_url = 'http://cmc307-06.mathcs.carleton.edu:5001/test_data_large?'

    if request.method == 'POST':
        result = request.form
        #result = request.form.get('description', 'default_description')
        # print("This is request.form.get: ")
        #print(result)
        for key, value in result.items():
            #print('Key:', key)
            #print('Value:', value)
            if (value):
                api_url += (key + '=' + value + '&')
        api_url += 'year=year&orderBy=reverse,year,month'
        #print(api_url)
        r = requests.get(api_url).json()
        #print(r)
        # print(json.loads(r.text))
        return render_template("data_entry.html",result = r, formData = result)
    return render_template("data_entry.html", result = result, clear = True, disqualifier="on", formData = formData)


@app.route('/visualization')
def visualization():
    return render_template('visualization.html')


if __name__ == '__main__':
#    if len(sys.argv) != 3:
#        print('Usage: {0} host port'.format(sys.argv[0]))
#        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
#        exit()
#
#    host = 'cmc307-06.mathcs.carleton.edu'
#    port = int(sys.argv[2])
    host='realfoodnetwork.carleton.edu'
    app.run(host="localhost", port=2019, debug=True)
