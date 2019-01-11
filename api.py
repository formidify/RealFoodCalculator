'''
    api.py
    Chae Kim
'''
from flask import Flask, render_template
import sys
import flask
import json
import psycopg2
#
#from config import password
#from config import database
#from config import user


app = flask.Flask(__name__, static_folder='static', template_folder='templates')

def get_connection():
    '''
    Returns a connection to the database described
    in the config module. Returns None if the
    connection attempt fails.
    '''
    connection = None
    try:
        connection = psycopg2.connect(dbname='RealFood',
                                      user='RealFood',
                                      password='L00kB4uL3@p',
					host='localhost')
    except Exception as e:
        print(e)
    return connection

def get_select_query_results(connection, query, parameters=None):
    '''
    Executes the specified query with the specified tuple of
    parameters. Returns a cursor for the query results.
    Raises an exception if the query fails for any reason.
    '''
    cursor = connection.cursor()
    if parameters is not None:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    return cursor

#~~~~~~~~APP ROUTES~~~~~~~~~#

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/entry_session')

@app.route('/table')
def get_products():

    month = flask.request.args.get('month', default='%').lower()
    year = flask.request.args.get('year', default='%').lower()
    description = flask.request.args.get('description', default='%').lower()
    category = flask.request.args.get('category', default='%').lower()
    productCode = flask.request.args.get('productCode', default='%').lower()
    brand = flask.request.args.get('brand', default='%').lower()
    vendor = flask.request.args.get('vendor', default='points').lower()
    notes = flask.request.args.get('notes', default='%').lower()
    #points = flask.request.args.get('points', type=int)
    #price = flask.request.args.get('price', type=int)

    query = """
            SELECT  table.month,
                    table.year,
                    table.description,
                    table.category,
                    table.productCode,
                    table.productCodeType,
                    table.brand,
                    table.vendor,
                    table.rating,
                    table.local,
                    table.localDescription,
                    table.fair,
                    table.fairDescription,
                    table.ecological,
                    table.ecologicalDescription,
                    table.humane,
                    table.humaneDescription,
                    table.disqualifier,
                    table.disqualifierDescription,
                    table.cost,
                    table.notes
            FROM table
            WHERE   lower(table.month) LIKE '%{0}%'
                    AND lower(table.year) LIKE '%{1}%'
                    AND lower(table.description) LIKE '%{2}%'
                    AND lower(table.category) LIKE '%{3}%'
                    AND lower(table.productCode) LIKE '%{4}%'
                    AND lower(table.brand) LIKE '%{5}%'
                    AND lower(table.vendor) LIKE '%{6}%'
                    AND lower(table.notes) LIKE '%{7}%'
            ORDER BY table.brand
            """.format(month, year, description, category, productCode, brand, vendor, notes)

    products_list = []
    connection = get_connection()
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                wine = {'month':row[0],
                        'year':row[1],
                        'description':row[2],
                        'category':row[3],
                        'productCode':row[4],
                        'productCodeType':row[5],
                        'brand':row[6],
                        'vendor':row[7],
                        'rating':row[8],
                        'local':row[9],
                        'localDescription':row[10],
                        'fair':row[11],
                        'fairDescription':row[12],
                        'ecological':row[13],
                        'ecologicalDescription':row[14],
                        'humane':row[15],
                        'humaneDescription':row[16],
                        'disqualifier':row[17],
                        'disqualifierDescription':row[18],
                        'cost':row[19],
                        'notes':row[20]}
                products_list.append(wine)
        except Exception as e:
            print(e)
        connection.close()
    return json.dumps(products_list)


if __name__ == '__main__':
    """if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
        exit()
    """
#    host = sys.argv[1]
    host = 'cmc307-06.mathcs.carleton.edu'
#   port = int(sys.argv[2])
#   host=host
#   port=5000
    app.run(host=host, debug=True)
