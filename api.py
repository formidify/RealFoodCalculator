'''
    api.py
    Chae Kim, Syd Botz, Claudia Naughton, Bryce Barton, James Yang

TO DO:
- make a separate config.py file for password security
- change table from "test_data" to other name
'''
from flask import Flask, render_template, session
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
        print("This is exception")
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
    cost  = flask.request.args.get('cost', default='0')
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
    orderBy = flask.request.args.get('orderBy', default='label_brand').lower()

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

    if orderBy=="year,month":
        orderBy="year, test_data_large.month DESC"

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
            ORDER BY test_data_large.{17}
            """.format(month, description, category, productCode, brand, vendor, notes,local, fair, ecological, humane, disqualifier, localDescription, fairDescription, ecologicalDescription,humaneDescription, disqualifierDescription,orderBy)

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
    
    month = flask.request.args.get('month', default='')
    year = flask.request.args.get('year', default='')
    description = flask.request.args.get('description', default='')
    category = flask.request.args.get('category', default='')
    productCode = flask.request.args.get('productCode', default='')
    if productCode == 'NONE': 
        productCode = ''
    brand = flask.request.args.get('brand', default='')
    if brand  == 'NONE': 
        brand = ''
    vendor = flask.request.args.get('vendor', default='')
    notes = flask.request.args.get('notes', default='')
    if notes  == 'NONE': 
        notes = ''
    cost  = flask.request.args.get('cost', type=float)
    local = flask.request.args.get('local', default='')
    localDescription = flask.request.args.get('localDescription', default='')
    if localDescription  == 'NONE': 
        localDescription = ''    
    fair = flask.request.args.get('fair', default='')
    fairDescription = flask.request.args.get('fairDescription', default='')
    if fairDescription  == 'NONE': 
        fairDescription = ''    
    ecological = flask.request.args.get('ecological', default='')
    ecologicalDescription = flask.request.args.get('ecologicalDescription', default='')
    if ecologicalDescription  == 'NONE': 
        ecologicalDescription = ''
    humane = flask.request.args.get('humane', default='')
    if (humane ==('N/A')):
        humane = None
    humaneDescription = flask.request.args.get('humaneDescription', default='')
    if humaneDescription  == 'NONE': 
        humaneDescription = ''
    disqualifier = flask.request.args.get('disqualifier', default='')
    disqualifierDescription = flask.request.args.get('disqualifierDescription', default ='')
    if disqualifierDescription  == 'NONE': 
        disqualifierDescription = ''
    productCodeType = ''
    ratingVersion = flask.request.args.get('rating_version', default='2.0')
    facility = ''
     
    """
    query = '''
             INSERT INTO test_data_large VALUES ({0},{1},'{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}',{19},'{20}','{21}');
            '''.format(month, year, description, category, productCode, productCodeType, brand, vendor, ratingVersion, local, localDescription, fair, fairDescription, ecological, ecologicalDescription, humane, humaneDescription, disqualifier, disqualifierDescription, cost, notes, facility)
    print("Entry: ", query)
    """
    query = """INSERT INTO test_data_large VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    parameters = (month, year, description, category, productCode, productCodeType, brand, vendor, ratingVersion, local, localDescription, fair, fairDescription, ecological, ecologicalDescription, humane, humaneDescription, disqualifier, disqualifierDescription, cost, notes, facility)
    if connection is not None:
        get_select_query_results(connection, query, parameters)
        connection.commit()
        connection.close()
        return "Stub Function: Inserted Entry"
    else:
        return "Stub Function: Could not get connection"

# get all years in reverse order
def get_all_years():
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

    return [2018, 2017, 2016]

# get data for quick charts
@app.route("/visualization/quick_data")
def get_quick_data():
    dic = {}
    curr_query = """SELECT MAX(year) AS maxyear FROM test_data_large;"""
    connection = get_connection()
    # (but what if we have 2019 but we want to look at 2018? have a button on top saying Not quite the year you are looking for? Go back or move front by 1 year)
    if connection is not None:
        try:
            for row in get_select_query_results(connection, curr_query):
                curr_year = row[0]
        except Exception as e:
            print(e)
        connection.close()

    curr_year = 2018 # just as initialization 
    groups = ['category', 'description', 'vendor', 'label_brand']
    type = ['real', 'nonreal']


    for g in groups:
        for t in type:
            labels = []
            cost = []
            if t == 'real':
                query = """SELECT trim({g}), SUM(cost) AS sum FROM test_data_large WHERE year = {c} AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') 
                AND COALESCE(trim({g}), '') <> '' GROUP BY trim({g}) ORDER BY sum DESC;""".format(g = g, c = curr_year)
            else:
                query = """SELECT trim({g}), SUM(cost) AS sum 
                FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') AS ecological, COALESCE(humane, 'f') AS humane, 
                {g}, cost, year FROM test_data_large WHERE COALESCE(trim({g}), '') <> '') X WHERE year = {c} AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' 
                GROUP BY trim({g}) ORDER BY sum DESC;""".format(g = g, c = curr_year)
            
            connection = get_connection()
            if connection is not None:
                try:
                    for row in get_select_query_results(connection, query):
                        labels.append(row[0])
                        cost.append(row[1])
                except Exception as e:
                    print(e)
                connection.close()

            key = g + ":" + t
            dic[key] = {"labels": labels[:5], "cost": cost[:5]}

    dic['year'] = curr_year

    return flask.jsonify(dic)

# get pie chart data for vis page (for 3 most recent years plus in total)
@app.route("/visualization/pie_data")
def get_pie_data():
    dic = {}

    data = []
    labels = []

    yrs = get_all_years()

    query = """SELECT trim(category), SUM(cost) AS c_cost FROM test_data_large GROUP BY trim(category) ORDER BY trim(category) DESC;"""

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
    dic['labels'] = yrs[:3] + ['total'] # add labels to the dictionary

    print(data)
    print(labels)

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
                FROM (SELECT description, (SELECT SUM(cost) AS sum FROM test_data_large WHERE {y} 
                (local IS NOT NULL OR fair IS NOT NULL OR ecological IS NOT NULL OR humane IS NOT NULL)) 
                AS sum FROM test_data_large WHERE {y} category = '{c}' GROUP BY description) A 
                RIGHT JOIN (SELECT COALESCE(B.description, C.description) AS description, COALESCE(B.dollars, 0) AS dollars, C.total_dollars as total_dollars FROM 
                (SELECT description, sum(cost) AS dollars FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') 
                AS ecological, COALESCE(humane, 'f') AS humane, description, cost, year, category FROM test_data_large) X 
                WHERE {y} category = '{c}' AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' 
                GROUP BY description) B FULL OUTER JOIN (SELECT description, sum(cost) AS total_dollars FROM test_data_large 
                WHERE {y} category = '{c}' GROUP BY description) C ON B.description = C.description) D ON A.description = D.description) Y 
                ORDER BY (1.00 * (totalp - mintotalp) * CASE WHEN rangetotalp = 0 THEN 0 ELSE (1 / rangetotalp) END 
                -  CASE WHEN rangeindp = 0 OR indp = minindp THEN 1.00 * (minindp + rangeindp) ELSE (1.00 * (indp - minindp) / rangeindp) END) 
                DESC;""".format(y = y, c = cat)


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

    # default ranking order is by a * norm(% in all) - b * norm(% in one) for a = b = 1, but the coefficients can be up to change
    return flask.jsonify({"items": items[:8], "total_percent": total_percent[:8], "ind_percent": ind_percent[:8], "dollars": dollars[:8]})



# get time series data for vis page (by category)
# NOTE: items where all four categories (local, ecological, fair, humane) are null will not be included in the calculation
@app.route("/visualization/time_data", defaults = {'cat': 'produce'})
@app.route("/visualization/time_data/<cat>")
def get_time_data(cat):

    # default ranking order is by a * norm(% in all) + b * norm(% in one) - c * norm($ spent) for a = b = c = 1, but the coefficients can be up to change
    return flask.jsonify({"items": items[:8], "total_percent": total_percent[:8], "ind_percent": ind_percent[:8], "dollars": dollars[:8]})

def get_item_time(yrs, item):
    query_real = """SELECT s, year FROM (SELECT {y0} AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE year = {y0} AND trim(description) = '{i}' 
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') UNION
        SELECT {y1} AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE year = {y1} AND trim(description) = '{i}' 
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') UNION
        SELECT {y2} AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE year = {y2} AND trim(description) = '{i}'
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't')) AS X ORDER BY year;
        """.format(y0 = yrs[0], y1 = yrs[1], y2 = yrs[2], i = item)

    query_total = """SELECT s, year FROM (SELECT {y0} AS year, COALESCE(SUM(cost),0) AS s FROM 
        test_data_large WHERE year = {y0} AND trim(description) = '{i}' UNION
        SELECT {y1} AS year, COALESCE(SUM(cost),0) AS s FROM 
        test_data_large WHERE year = {y1} AND trim(description) = '{i}' UNION
        SELECT {y2} AS year, COALESCE(SUM(cost),0) AS s FROM 
        test_data_large WHERE year = {y2} AND trim(description) = '{i}') AS X ORDER BY year;
        """.format(y0 = yrs[0], y1 = yrs[1], y2 = yrs[2], i = item)

    real = []
    total = []
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row1 in get_select_query_results(connection, query_real):
                real.append(row1[0])
            for row2 in get_select_query_results(connection, query_total):
                total.append(row2[0])
        except Exception as e:
            print(e)
        connection.close()

    return total, real

# get time series data for vis page (by category)
# NOTE: items where all four categories (local, ecological, fair, humane) are null will not be included in the calculation
@app.route("/visualization/item_data", defaults = {'item': '', 'type': ''})
@app.route("/visualization/item_data/<path:item>+<path:type>")
def get_item_data(item, type):

    # add item for percent chart
    if type == 'percent':
        query = """SELECT SUM(cost) AS sum FROM test_data_large WHERE description = {d} AND (""".format(d = item)
        return 

    # add item for hypothetical increase chart
    if type == 'increase':
        return

    # add item for item/label/vendor chart
    if type == 'liv':
        return

    # add single item for one year
    if type == 'year':
        yrs = get_all_years()
        print(item)

        total, real = get_item_time(yrs, item)

        yrs = yrs[:3]
        yrs.reverse()
        return flask.jsonify({"cost": [total, real], "yrs": yrs})


@app.route("/visualization/get_categories/")
def get_categories():
    cats = []
    query = """SELECT DISTINCT ON (trim(category)) category FROM test_data_large;"""

    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                cats.append(row[0])
        except Exception as e:
            print(e)
        connection.close()

    print(cats)
    return flask.jsonify({"cats": cats})

@app.route("/visualization/get_categories_time/", defaults = {'cat': ''})
@app.route("/visualization/get_categories_time/<cat>")
def get_categories_time(cat):
    items = [] # all of the distinct item in the category
    query = """SELECT trim(description), SUM(cost) AS s FROM test_data_large WHERE trim(category) = '{p}' GROUP BY description ORDER BY s DESC;""".format(p = cat)
    yrs = get_all_years()

    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                items.append(row[0])
        except Exception as e:
            print(e)
        connection.close()

    total = []
    real = []

    for item in items:
        t, r = get_item_time(yrs, item)
        total.append(t)
        real.append(r)

    yrs = yrs[:3]
    yrs.reverse()
    return flask.jsonify({"cost": [total, real], "yrs": yrs, "items": items})

## combine the below 3 methods into one

# return results that match the input item
@app.route("/visualization/get_item", defaults = {'search': ''})
@app.route("/visualization/get_item/<search>")
def get_item(search):
    results = []
    query = """SELECT DISTINCT ON (trim(description)) description FROM test_data_large WHERE lower(trim(description)) LIKE lower('%{s}%');""".format(s = search)
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                results.append(row[0])
        except Exception as e:
            print(e)
        connection.close()
    print(results)
    return flask.jsonify({"search": results})

# return results that match the input vendor
@app.route("/visualization/get_vendor", defaults = {'search': ''})
@app.route("/visualization/get_vendor/<search>")
def get_vendor(search):
    results = []
    query = """SELECT DISTINCT ON (trim(vendor)) vendor FROM test_data_large WHERE lower(trim(vendor)) LIKE lower('%{s}%');""".format(s = search)
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                results.append(row[0])
        except Exception as e:
            print(e)
        connection.close()
    print(results)
    return flask.jsonify({"search": results})

# return results that match the input label/brand
@app.route("/visualization/get_label", defaults = {'search': ''})
@app.route("/visualization/get_label/<search>")
def get_label(search):
    results = []
    query = """SELECT DISTINCT ON (trim(label_brand)) label_brand FROM test_data_large WHERE lower(trim(label_brand)) LIKE lower('%{s}%');""".format(s = search)
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query):
                results.append(row[0])
        except Exception as e:
            print(e)
        connection.close()
    print(results)
    return flask.jsonify({"search": results})


# get data for brand, label, item trio visualization
@app.route("/visualization/brand_vendor_data", defaults = {'item': '', 'type': ''})
@app.route("/visualization/brand_vendor_data/<path:item>+<path:type>")
def get_brand_vendor_data(item, type):
    yrs = get_all_years()


    if "'" in item:
        item = item.replace("'", "''")
    item = item.strip()

    # add individual items
    if type == 'item':
        # query for all labels
        query1 = """SELECT DISTINCT ON (trim(label_brand)) label_brand FROM test_data_large WHERE trim(description) = '{i}';""".format(i = item)
        # query for all brands
        query2 = """SELECT DISTINCT ON (trim(vendor)) vendor FROM test_data_large WHERE trim(description) = '{i}';""".format(i = item)
        # query for all years for the specific item per brand real

        # query for all years for the specific item per brand nonreal

        key = 'description'
        key_a = 'label_brand'
        key_b = 'vendor'

    # add brand/label
    if type == 'brand':
        # query for all labels
        query1 = """SELECT DISTINCT ON (trim(description)) description FROM test_data_large WHERE trim(label_brand) = '{i}';""".format(i = item)
        # query for all brands
        query2 = """SELECT DISTINCT ON (trim(vendor)) vendor FROM test_data_large WHERE trim(label_brand) = '{i}';""".format(i = item)

        key = 'label_brand'
        key_a = 'description'
        key_b = 'vendor'
    # add vendor
    if type == 'vendor':
        # query for all labels
        query1 = """SELECT DISTINCT ON (trim(description)) description FROM test_data_large WHERE trim(vendor) = '{i}';""".format(i = item)
        # query for all brands
        query2 = """SELECT DISTINCT ON (trim(label_brand)) label_brand FROM test_data_large WHERE trim(vendor) = '{i}';""".format(i = item)

        key = 'vendor'
        key_a = 'description'
        key_b = 'label_brand'

    l1, l2, R1, R2, N1, N2 = [], [], [], [], [], []
    connection = get_connection()
    if connection is not None:
        try:
            # either this or minimum items allowed to show
            for row in get_select_query_results(connection, query1):
                l1.append(row[0])
            for row in get_select_query_results(connection, query2):
                l2.append(row[0])

            query_real = """SELECT s, year FROM (SELECT {y0} AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE year = {y0} AND trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') UNION
        SELECT {y1} AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE year = {y1} AND trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') UNION
        SELECT {y2} AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE year = {y2} AND trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't') UNION
        SELECT 9999 AS year, COALESCE(SUM(cost),0) AS s FROM test_data_large WHERE trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND (local = 't' OR fair = 't' OR ecological = 't' OR humane = 't')) AS X ORDER BY year;
        """
            query_nonreal = """SELECT s, year FROM (SELECT {y0} AS year, COALESCE(SUM(cost),0) AS s 
            FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') 
            AS ecological, COALESCE(humane, 'f') AS humane, cost, year, {k}, {a} FROM test_data_large) A WHERE year = {y0} AND trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' UNION
        SELECT {y1} AS year, COALESCE(SUM(cost),0) AS s FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') 
            AS ecological, COALESCE(humane, 'f') AS humane, cost, year, {k}, {a} FROM test_data_large) B WHERE year = {y1} AND trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' UNION
        SELECT {y2} AS year, COALESCE(SUM(cost),0) AS s FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') 
            AS ecological, COALESCE(humane, 'f') AS humane, cost, year, {k}, {a} FROM test_data_large) C WHERE year = {y2} AND trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't' UNION
        SELECT 9999 AS year, COALESCE(SUM(cost),0) AS s FROM (SELECT COALESCE(local, 'f') AS local, COALESCE(fair, 'f') AS fair, COALESCE(ecological, 'f') 
            AS ecological, COALESCE(humane, 'f') AS humane, cost, year, {k}, {a} FROM test_data_large) D WHERE trim({k}) = '{i}' AND trim({a}) = '{l}'
        AND local <> 't' AND fair <> 't' AND ecological <> 't' AND humane <> 't') AS X ORDER BY year;
        """


            for l in l1:

                if "'" in l:
                    l = l.replace("'", "''")
                # 9999 is for all years
                r1 = []
                r2 = []
                query_a = query_real.format(y0 = yrs[0], y1 = yrs[1], y2 = yrs[2], i = item, k = key, a = key_a, l = l)

                query_a_nonreal = query_nonreal.format(y0 = yrs[0], y1 = yrs[1], y2 = yrs[2], i = item, k = key, a = key_a, l = l)

                for row in get_select_query_results(connection, query_a):
                    r1.append(row[0])
                for row in get_select_query_results(connection, query_a_nonreal):
                    r2.append(row[0])

                R1.append(r1)
                R2.append(r2)

            for l in l2:
                # check for apostrophes before inputting into database for queries
                if "'" in l:
                    l = l.replace("'", "''")
                n1 = []
                n2 = []
                query_b = query_real.format(y0 = yrs[0], y1 = yrs[1], y2 = yrs[2], i = item, k = key, a = key_b, l = l)

                query_b_nonreal = query_nonreal.format(y0 = yrs[0], y1 = yrs[1], y2 = yrs[2], i = item, k = key, a = key_b, l = l)

                for row in get_select_query_results(connection, query_b):
                    n1.append(row[0])
                for row in get_select_query_results(connection, query_b_nonreal):
                    n2.append(row[0])

                N1.append(n1)
                N2.append(n2)

            print(R1)
            print(R2)
            print(N1)
            print(N2)
            print(l1)
            print(l2)




        except Exception as e:
            print(e)
        connection.close()

    yrs = yrs[:3]
    yrs.reverse()
    return flask.jsonify({"yrs": yrs, key_a: l1, key_b: l2, key_a + " real": R1, key_a + " nonreal": R2, key_b + " real": N1, key_b + " nonreal": N2})


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
