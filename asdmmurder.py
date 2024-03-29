import cx_Oracle
from flask import Flask, jsonify, render_template  # Import render_template
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and domains

def fetch_geojson(query):
    conn = cx_Oracle.connect(dsn="geoslearn", user="s2606314", password="fudge")
    c = conn.cursor()

    # Execute the query 
    c.execute(query)
    
    # Construct GeoJSON features including the DESCRIPTION
    geojson_features = []
    for geojson, description in c:
        feature = {
            'type': 'Feature',
            'geometry': json.loads(geojson.read()),
            'properties': {
                'description': description
            }
        }
        geojson_features.append(feature)
    
    geojson_collection = {
        'type': 'FeatureCollection',
        'features': geojson_features
    }

    c.close()
    conn.close()

    return geojson_collection

def update_current_location(player_id, geometry_id):
    try:
        # 查询获取指定 geometry_id 的 SDO_GEOMETRY 数据
        select_query = """
        SELECT LOCATION
        FROM GEOMETRIES
        WHERE GEOMETRY_ID = :geometry_id
        """

        # connect
        conn = cx_Oracle.connect(dsn="geoslearn", user="s2606314", password="fudge")
        c = conn.cursor()

        c.execute(select_query, geometry_id=geometry_id)
        result = c.fetchone()

        if result:
            # 获取 SDO_GEOMETRY 数据
            location_data = result[0]

            # 更新查询
            update_query = """
            UPDATE players 
            SET current_location = :location_data
            WHERE player_id = :player_id
            """

            # 执行更新查询
            c.execute(update_query, location_data=location_data, player_id=player_id)
            conn.commit()

            get_query="""
            SELECT SDO_UTIL.TO_GEOJSON(CURRENT_LOCATION) AS geojson, 'you are here' AS DESCRIPTION
            FROM PLAYERS 
            WHERE PLAYER_ID= :player_id
            """
            cldata=fetch_geojson(get_query)
            return jsonify(cldata)
        
        else:
            return jsonify({'error': 'could not find the specific geometry_id'})

    except Exception as e:
        # 如果发生异常，则返回错误消息
        return jsonify({'error': str(e)})

    finally:
        # 关闭游标和连接
        c.close()
        conn.close()
    

@app.route('/enterPuzzle1')
def puzzle1json():
    puzzle1query="""
    SELECT SDO_UTIL.TO_GEOJSON(LOCATION) AS geojson, DESCRIPTION 
    FROM GEOMETRIES WHERE description='Puzzle 1 Polygon'
    """
    puzzle1json_data=fetch_geojson(puzzle1query)
    #return jsonify(puzzle1json_data)

    #get coordinates of polygon
    coordinates = puzzle1json_data['features'][0]['geometry']['coordinates'][0]
    # get the coordinates of the second point
    second_point = coordinates[1]
    x, y = second_point

    srid = 8307 

    #update current location
    update_query = """
    UPDATE players 
    SET current_location = SDO_GEOMETRY('POINT (' || :x || ' ' || :y || ')', :srid)
    WHERE player_id = :player_id
    """

    conn = cx_Oracle.connect(dsn="geoslearn", user="s2606314", password="fudge")
    c = conn.cursor()

    try:
        # update
        c.execute(update_query, x=x, y=y, srid=srid, player_id=1)
        conn.commit()

        # add update result
        #response_data = {'message': 'Update successful', 'geojson_data': puzzle1json_data}
        return jsonify(puzzle1json_data)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        c.close()
        conn.close()


@app.route('/path/p1',endpoint='pathp1')
def pathp1():
    viquery="""
    SELECT SDO_UTIL.TO_GEOJSON(LOCATION) AS geojson, DESCRIPTION 
    FROM GEOMETRIES WHERE geometry_id=33
    """
    pathdata=fetch_geojson(viquery)

    distancequery="""
    SELECT SDO_GEOM.SDO_DISTANCE(p.current_location,g.location,0.005)
    FROM players p
    JOIN geometries g ON g.geometry_id = 1
    WHERE p.player_id = 1
    """
    conn = cx_Oracle.connect(dsn="geoslearn", user="s2606314", password="fudge")
    c = conn.cursor()

    try:
        c.execute(distancequery)
        distance_result = c.fetchone()[0]  

        # 将距离添加到 pathdata 中的第一个 feature 的 properties 中
        if pathdata['features']:
            pathdata['features'][0]['properties']['distance'] = distance_result

        return jsonify(pathdata)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        c.close()
        conn.close()

    #return jsonify(pathdata)
        
@app.route('/path/p2',endpoint='pathp2')
def pathp2():
    viquery="""
    SELECT SDO_UTIL.TO_GEOJSON(LOCATION) AS geojson, DESCRIPTION 
    FROM GEOMETRIES WHERE geometry_id=35
    """
    pathdata=fetch_geojson(viquery)

    distancequery="""
    SELECT SDO_GEOM.SDO_DISTANCE(p.current_location,g.location,0.005)
    FROM players p
    JOIN geometries g ON g.geometry_id = 2
    WHERE p.player_id = 1
    """
    conn = cx_Oracle.connect(dsn="geoslearn", user="s2606314", password="fudge")
    c = conn.cursor()

    try:
        c.execute(distancequery)
        distance_result = c.fetchone()[0]  

        # 将距离添加到 pathdata 中的第一个 feature 的 properties 中
        if pathdata['features']:
            pathdata['features'][0]['properties']['distance'] = distance_result

        return jsonify(pathdata)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        c.close()
        conn.close()

    #return jsonify(pathdata)
        
@app.route('/path/p3',endpoint='pathp3')
def pathp3():
    viquery="""
    SELECT SDO_UTIL.TO_GEOJSON(LOCATION) AS geojson, DESCRIPTION 
    FROM GEOMETRIES WHERE geometry_id=34
    """
    pathdata=fetch_geojson(viquery)

    distancequery="""
    SELECT SDO_GEOM.SDO_DISTANCE(p.current_location,g.location,0.005)
    FROM players p
    JOIN geometries g ON g.geometry_id = 3
    WHERE p.player_id = 1
    """
    conn = cx_Oracle.connect(dsn="geoslearn", user="s2606314", password="fudge")
    c = conn.cursor()

    try:
        c.execute(distancequery)
        distance_result = c.fetchone()[0]  

        # 将距离添加到 pathdata 中的第一个 feature 的 properties 中
        if pathdata['features']:
            pathdata['features'][0]['properties']['distance'] = distance_result

        return jsonify(pathdata)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        c.close()
        conn.close()

    #return jsonify(pathdata)

@app.route('/move/11')
def move11():
    return update_current_location(1,1)
    

@app.route('/geojson')
def geojson():
    allquery="""
    SELECT SDO_UTIL.TO_GEOJSON(LOCATION) AS geojson, DESCRIPTION
    FROM GEOMETRIES
    """
    geojson_data = fetch_geojson(allquery)
    return jsonify(geojson_data)

@app.route('/')
def home():
    # Render the index.html file
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=50001,debug=True)
