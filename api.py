'''
    api.py
    Chae Kim, Syd Botz, Claudia Naughton, Bryce Barton, James Yang

TO DO: 
- make a separate config.py file for password security 
- change table from "test_data" to other name  
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

@app.route('/test_data_large')
def get_products():

    month = flask.request.args.get('month', default='-1').lower()
    year = flask.request.args.get('year', default='-1').lower()
    description = flask.request.args.get('description', default='%').lower()
    category = flask.request.args.get('category', default='%').lower()
    productCode = flask.request.args.get('productCode', default='%').lower()
    brand = flask.request.args.get('brand', default='%').lower()
    vendor = flask.request.args.get('vendor', default='%').lower()
    notes = flask.request.args.get('notes', default='%').lower()
    cost  = flask.request.args.get('cost', type=float)
    local = flask.request.args.get('local', default='-1')
    localDescription = flask.request.args.get('localDescription', default='%').lower()
    fair = flask.request.args.get('fair', default='-1')
    fairDescription = flask.request.args.get('fairDescription', default='%').lower()
    ecological = flask.request.args.get('ecological', default='-1')
    ecologicalDescription = flask.request.args.get('ecologicalDescription', default='%').lower()
    humane = flask.request.args.get('humane', default='-1')
    humaneDescription = flask.request.args.get('humaneDescription', default='%').lower()
    disqualifier = flask.request.args.get('disqualifier', default='-1')
    disqualifierDescription = flask.request.args.get('disqualifierDescription', default ='%').lower()

    if month == "-1" and year == "-1":
        month = " "
    elif month == "-1":
        month = "test_data_large.year = " + year + " AND "
    elif year == "-1":
        month = "test_data_large.month = " + month + " AND "
    else:
        month = "test_data_large.month = " + month + " AND test_data_large.year = " + year + " AND "
    if local == "on":
        local = "AND test_data_large.local = TRUE"
    else: 
        local = ""
    if fair == "on": 
        fair = "AND test_data_large.fair = TRUE"
    else: 
        fair = ""
    if ecological == "on":
        ecological = "AND test_data_large.ecological = TRUE"
    else: 
        ecological = ""
    if humane == "on":
        humane = "AND test_data_large.humane = TRUE"
    elif humane == "none":
        humane = "AND test_data_large.humane IS NULL"
    else: 
        humane = "AND test_data_large.humane = FALSE"
    if disqualifier == "on":
        disqualifier = "AND test_data_large.disqualifier = TRUE"
    else: 
       disqualifier = "" 


    query = """
            SELECT  test_data_large.month,
                    test_data_large.year,
                    test_data_large.description,
                    test_data_large.category,
                    test_data_large.product_code,
                    test_data_large.product_code_type,
                    test_data_large.label_brand,
                    test_data_large.vendor,
                    test_data_large.rating_version,
                    test_data_large.local,
                    test_data_large.local_description,
                    test_data_large.fair,
                    test_data_large.fair_description,
                    test_data_large.ecological,
                    test_data_large.ecological_description,
                    test_data_large.humane,
                    test_data_large.humane_description,
                    test_data_large.disqualifier,
                    test_data_large.disqualifier_description,
                    test_data_large.cost,
                    test_data_large.notes,
                    test_data_large.facility
            FROM test_data_large
            WHERE   {0}
                    lower(test_data_large.description) LIKE '%{1}%'
                    AND lower(test_data_large.category) LIKE '%{2}%'
                    AND lower(test_data_large.product_code) LIKE '{3}'
                    AND lower(test_data_large.label_brand) LIKE '%{4}%'
                    AND lower(test_data_large.vendor) LIKE '%{5}%'
                    AND lower(test_data_large.notes) LIKE '%{6}%'
                    {7}
                    {8}
                    {9}
                    {10}
                    {11}
                    AND lower(test_data_large.local_description) LIKE lower('%{12}%')
                    AND lower(test_data_large.fair_description) LIKE lower('%{13}%')
                    AND lower(test_data_large.ecological_description) LIKE lower( '%{14}%')
                    AND lower(test_data_large.humane_description) LIKE lower('%{15}%')
                    AND lower(test_data_large.disqualifier_description) LIKE lower('%{16}%')
            ORDER BY test_data_large.label_brand
            """.format(month, description, category, productCode, brand, vendor, notes, local, fair, ecological, humane, disqualifier, localDescription, fairDescription, ecologicalDescription,humaneDescription, disqualifierDescription)

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
                        'notes':row[20],
                        'facility': row[21]}
                products_list.append(product)
        except Exception as e:
            print(e)
        connection.close()
    return json.dumps(products_list)

# get pie chart data for vis page (for 3 most recent years plus in total)
@app.route("/visualization/pie_data")
def get_pie_data():
    data = []
    labels = []
    query = """SELECT trim(category), SUM(cost) AS c_cost FROM test_data_large GROUP BY trim(category) ORDER BY c_cost DESC;"""

    # currently not in use
    query_by_year = """SELECT year, trim(category), SUM(cost) AS c_cost FROM test_data_large GROUP BY trim(category),year ORDER BY c_cost DESC;"""

    # todo: query should also take account of the years
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                labels.append(row[0])
                data.append(row[1])
        except Exception as e:
            print(e)
        connection.close()

    return flask.jsonify({"data": data, "labels": labels})


# get bar data for vis page
@app.route("/visualization/bar_data", defaults = {'cat': 'produce'})
@app.route("/visualization/bar_data/<cat>")
def get_bar_data(cat):
    items = []
    real = []
    nonreal = []
    # not filtered by year
    query = """SELECT COALESCE(Z.description, B.description) AS description, COALESCE(Z.real, 0) AS real, COALESCE(B.nonreal, 0) 
    as nonreal FROM (SELECT description, SUM(cost) AS real FROM test_data_large WHERE category = '%{0}%' AND 
        (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') GROUP BY description) Z 
    FULL OUTER JOIN (SELECT description, SUM(cost) AS nonreal FROM test_data_large WHERE category = '%{1}%' AND 
        local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' GROUP BY description) B 
    ON Z.description = B.description ORDER BY real desc;""".format(cat, cat)

    # todo: query should also take account of the years
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                items.append(row[0])
                real.append(row[1])
                nonreal.append(row[2])
        except Exception as e:
            print(e)
        connection.close()

    return flask.jsonify({"items": items, "real": real, "nonreal": nonreal})



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
