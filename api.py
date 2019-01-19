'''
    api.py
    Chae Kim
'''
from flask import Flask, render_template
import sys
import flask
import simplejson as json
import psycopg2


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

@app.route('/test_data')
def get_products():

    month = flask.request.args.get('month', default='-1').lower()
    year = flask.request.args.get('year', default='-1').lower()
    description = flask.request.args.get('description', default='%').lower()
    category = flask.request.args.get('category', default='%').lower()
    productCode = flask.request.args.get('product_code', default='%').lower()
    brand = flask.request.args.get('label_brand', default='%').lower()
    vendor = flask.request.args.get('vendor', default='%').lower()
    notes = flask.request.args.get('notes', default='%').lower()
    cost  = flask.request.args.get('cost', type=float)

    if month == "-1" and year == "-1":
        month = " "
    elif month == "-1":
        month = "test_data.year = " + year + " AND "
    elif year == "-1":
        month = "test_data.month =  " + month + " AND "
    else:
        month = "test_data.month = " + month + " AND test_data.year = " + year + " AND "

    query = """
            SELECT  test_data.month,
                    test_data.year,
                    test_data.description,
                    test_data.category,
                    test_data.product_code,
                    test_data.product_code_type,
                    test_data.label_brand,
                    test_data.vendor,
                    test_data.rating_version,
                    test_data.local,
                    test_data.local_description,
                    test_data.fair,
                    test_data.fair_description,
                    test_data.ecological,
                    test_data.ecological_description,
                    test_data.humane,
                    test_data.humane_description,
                    test_data.disqualifier,
                    test_data.disqualifier_description,
                    test_data.cost,
                    test_data.notes,
                    test_data.facility
            FROM test_data
            WHERE   {0}
                    lower(test_data.description) LIKE '%{1}%'
                    AND lower(test_data.category) LIKE '%{2}%'
                    AND lower(test_data.product_code) LIKE '%{3}%'
                    AND lower(test_data.label_brand) LIKE '%{4}%'
                    AND lower(test_data.vendor) LIKE '%{5}%'
                    AND lower(test_data.notes) LIKE '%{6}%'
            ORDER BY test_data.label_brand
            """.format(month, description, category, productCode, brand, vendor, notes)

    products_list = []
    connection = get_connection()
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                product = {'month':row[0],
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
                products_list.append(product)
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
    port= 5001
    print('Using Port: '+ sys.argv[0])
    app.run(host=host,port=port, debug=True)
