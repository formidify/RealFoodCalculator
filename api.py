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

# insert one item into database
@app.route("/add_entry")
def insert_entry():
    connection = get_connection()
    if connection is not None:
        return "Stub Function: Inserted Entry"
    return "Stub Function: Could not get connection"

# get pie chart data for vis page (for 3 most recent years plus in total)
@app.route("/visualization/pie_data")
def get_pie_data():
    dic = {}

    data = []
    labels = []
    yrs = []

    yr_query = """SELECT DISTINCT ON (year) year FROM test_data_large ORDER BY year DESC;"""

    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, yr_query):
                yrs.append(row[0])
        except Exception as e:
            print(e)
        connection.close()


    query = """SELECT trim(category), SUM(cost) AS c_cost FROM test_data_large GROUP BY trim(category) ORDER BY trim(category) DESC;"""

    # make sure we pick most recent years of ascending order TODO

    # DELETE later!
    if len(yrs) < 3:
        yrs.append('2016')


    for i in range(3): # 3 most recent years

        query_by_year = """SELECT trim(category), SUM(cost) AS c_cost FROM test_data_large WHERE year = {0} GROUP BY trim(category) ORDER BY trim(category) DESC;""".format(yrs[i])
        connection = get_connection()
        if connection is not None:
            try:
                # either this or minimum items allowed to show
                for row in get_select_query_results(connection, query_by_year):
                    labels.append(row[0])
                    data.append(row[1])
            except Exception as e:
                print(e)
            connection.close()
        dic[str(yrs[i])] = {"data": data, "labels": labels}
        # reset for other years
        data = []
        labels = []

    # get data for all years
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
    dic['total'] = {"data": data, "labels": labels}
    dic['labels'] = yrs + ['total'] # add labels to the dictionary

    return flask.jsonify(dic)


# get bar data for vis page
@app.route("/visualization/bar_data", defaults = {'cat': 'produce', 'yr': 'total'})
@app.route("/visualization/bar_data/<cat>+<yr>")
def get_bar_data(cat, yr):
    items = []
    real = []
    nonreal = []

    if yr == 'total':
        y = ''
    else:
        y = 'year = ' + str(yr) + ' AND'
        
    # not filtered by year
    query = """SELECT COALESCE(Z.description, B.description) 
            AS description, COALESCE(Z.real, 0) 
            AS real, COALESCE(B.nonreal, 0) 
            AS nonreal FROM (SELECT description, SUM(cost) 
            AS real FROM test_data_large WHERE {y} category = '{c}' AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') 
            GROUP BY description) Z FULL OUTER JOIN (SELECT description, SUM(cost) AS nonreal FROM 
            (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') AS ecological, COALESCE(humane, 'f') AS humane, 
            description, cost, year, category FROM test_data_large) X
                WHERE {y} category = '{c}' AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' GROUP BY description) B 
                ON Z.description = B.description ORDER BY (COALESCE(real,0) + COALESCE(nonreal,0)) desc;""".format(y = y, c = cat)
    print(query)

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

    print(items)
    print(real)
    print(nonreal)
    return flask.jsonify({"items": items[:8], "real": real[:8], "nonreal": nonreal[:8]})


# get percent data for vis page
# NOTE: items where all four categories (local, ecological, fair, humane) are null will not be included in the calculation
@app.route("/visualization/percent_data", defaults = {'cat': 'produce', 'yr': 'total'})
@app.route("/visualization/percent_data/<cat>+<yr>")
def get_percent_data(cat, yr):
    items = []
    total_percent = []
    ind_percent = []
    dollars = []
    # not filtered by year
    if yr == 'total':
        y = ''
    else:
        y = 'year = ' + str(yr) + ' AND'

    # if we convert all of the current non-real food purchases to real
    query = """SELECT description, 100 * totalp AS totalp, 100 * indp AS indp, dollars FROM 
                (SELECT COALESCE(D.description, A.description) AS description, (dollars / sum) AS totalp, (dollars / total_dollars) AS indp, dollars, 
                MIN(dollars / sum) OVER () AS mintotalp, MAX(dollars / sum) OVER () - MIN(dollars / sum) OVER() AS rangetotalp,
                MIN(dollars / total_dollars) OVER () AS minindp, MAX(dollars / total_dollars) OVER () - MIN(dollars / total_dollars) OVER() AS rangeindp,
                MIN(dollars) OVER () AS mindp, MAX(dollars) OVER () - MIN(dollars) OVER() AS rangedp
                FROM (SELECT description, (SELECT SUM(cost) AS sum FROM test_data_large WHERE {y} category = '{c}' AND 
                (local IS NOT NULL OR fair IS NOT NULL OR ecological IS NOT NULL OR humane IS NOT NULL)) 
                AS sum FROM test_data_large WHERE {y} category = '{c}' GROUP BY description) A 
                RIGHT JOIN (SELECT COALESCE(B.description, C.description) AS description, COALESCE(B.dollars, 0) AS dollars, C.total_dollars as total_dollars FROM 
                (SELECT description, sum(cost) AS dollars FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') 
                AS ecological, COALESCE(humane, 'f') AS humane, description, cost, year, category FROM test_data_large) X 
                WHERE {y} category = '{c}' AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' 
                GROUP BY description) B FULL OUTER JOIN (SELECT description, sum(cost) AS total_dollars FROM test_data_large 
                WHERE {y} category = '{c}' GROUP BY description) C ON B.description = C.description) D ON A.description = D.description) Y 
                ORDER BY (1.00 * (totalp - mintotalp) * CASE WHEN rangetotalp = 0 AND mintotalp = 0 THEN NUMERIC 'NaN' WHEN rangetotalp = 0 THEN 0 ELSE (1 / rangetotalp) END
                    - 1.00 * (indp - minindp) * CASE WHEN rangeindp = 0 AND minindp = 0 THEN NUMERIC 'NaN' WHEN rangeindp = 0 THEN 0 ELSE (1 / rangeindp) END) DESC;""".format(y = y, c = cat)
    print(query)

    # todo: query should also take account of the years
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                items.append(row[0])
                total_percent.append(row[1])
                ind_percent.append(row[2])
                dollars.append(row[3])
        except Exception as e:
            print(e)
        connection.close()

    print(items)
    print(total_percent)
    print(ind_percent)
    # default ranking order is by a * norm(% in all) - b * norm(% in one) for a = b = 1, but the coefficients can be up to change
    return flask.jsonify({"items": items[:8], "total_percent": total_percent[:8], "ind_percent": ind_percent[:8], "dollars": dollars[:8]})



# get time series data for vis page (by category)
# NOTE: items where all four categories (local, ecological, fair, humane) are null will not be included in the calculation
@app.route("/visualization/time_data", defaults = {'cat': 'produce', 'yr': 'total'})
@app.route("/visualization/time_data/<cat>+<yr>")
def get_time_data(cat, yr):
    items = []
    total_percent = []
    ind_percent = []
    dollars = []
    # not filtered by year
    if yr == 'total':
        y = ''
    else:
        y = 'year = ' + str(yr) + ' AND'

    # how do we query this?
    query = """ """
    print(query)

    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                items.append(row[0])
                total_percent.append(row[1])
                ind_percent.append(row[2])
                dollars.append(row[3])
        except Exception as e:
            print(e)
        connection.close()

    print(items)
    print(total_percent)
    print(ind_percent)
    # default ranking order is by a * norm(% in all) + b * norm(% in one) - c * norm($ spent) for a = b = c = 1, but the coefficients can be up to change
    return flask.jsonify({"items": items[:8], "total_percent": total_percent[:8], "ind_percent": ind_percent[:8], "dollars": dollars[:8]})

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
