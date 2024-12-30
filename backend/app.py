from flask import Flask, request, jsonify
from flask_cors import CORS
from config import database_config
from Analysis.Coordinate_plot import Coordinateshow

app = Flask(__name__)
CORS(app)

@app.route('/api/generalSearch', methods=['POST'])
def generalSearch():
    connection = database_config.get_connection()
    cursor = connection.cursor()
    new_entry = request.json
    keyword = new_entry.get("keyword")
    query = """
        select star.star_name, star.origin_system, upper(object.object_type), discovery.telescope_id, discovery.discovery_year 
        from star
        join object on star.object_id = object.object_id
        left join discovery on star.object_id = discovery.object_id 
        where star.star_name LIKE :1
        UNION
        select planet.planet_name, planet.origin_system, upper(object.object_type), discovery.telescope_id, discovery.discovery_year  
        from planet
        join object on planet.object_id = object.object_id
        left join discovery on planet.object_id = discovery.object_id 
        where planet.planet_name LIKE :1
        UNION
        select miscellaneous.misc_name, miscellaneous.origin_system, upper(object.object_type), discovery.telescope_id, discovery.discovery_year  
        from miscellaneous
        join object on miscellaneous.object_id = object.object_id
        left join discovery on miscellaneous.object_id = discovery.object_id 
        where miscellaneous.misc_name like :1
    """
    cursor.execute(query, {'1': keyword + '%'})

    result = cursor.fetchall()
    #print(result)

    data = [{"obj_name": row[0], "obj_type": row[1], "obj_loc": row[2], "telescope": row[3], "discovery": row[4]} for row in result]
    
    cursor.close()
    connection.close()

    return jsonify(data)


@app.route('/api/specifiedSearch', methods=['POST'])
def search_keyword():
    connection = database_config.get_connection()

    try:
        new_entry = request.json
        keyword = new_entry.get("keyword")
        filterWord = new_entry.get("filter")

        if filterWord == "star":
            return searchStar(keyword, connection)
        if filterWord == "planet":
            return searchPlanet(keyword, connection)
        if filterWord == "misc":
            return searchMisc(keyword, connection)

        return {"error": "Invalid filter specified"}, 400

    except Exception as e:
        return {"error": "An error occurred during the search"}, 500

    finally:
        if connection:
            connection.close()

def searchStar(keyword, connection):
    cursor = connection.cursor()
    query = """
        select star_name, stellar_class, solar_radii, solar_mass, system_type, distance
        from star, star_system
        WHERE star.origin_system = star_system.system_name and star_name like :1
    """
    cursor.execute(query, {'1': keyword + '%'})

    result = cursor.fetchall()
    #print(result)

    data = [{"star_name": row[0], "stellar_class": row[1], "solar_radii": row[2], "solar_mass": row[3], "star_type": row[4], "distance": row[5]} for row in result]
    cursor.close()

    return jsonify(data)

def searchPlanet(keyword, connection):
    cursor = connection.cursor()
    query = """
        select planet_name, origin_system, planetary_radii, planetary_mass, orbital_period, atmosphere
        from planet
        WHERE planet_name like :1
    """
    cursor.execute(query, {'1': keyword + '%'})

    result = cursor.fetchall()
    #print(result)

    data = [{"planet_name": row[0], "parent_system": row[1], "planet_radius": row[2], "planet_mass": row[3], "orbit": row[4], "atmosphere": row[5]} for row in result]
    cursor.close()

    return jsonify(data)

def searchMisc(keyword, connection):
    cursor = connection.cursor()
    query = """
        select misc_name, origin_system, REPLACE(UPPER(SUBSTR(misc_category, 1, 1)) || LOWER(SUBSTR(REPLACE(misc_category, '_', ' '), 2)), ' ', ''), distance
        from miscellaneous
        join star_system on miscellaneous.origin_system = star_system.system_name
        where misc_name like :1
        UNION
        select satellite_name, planet.origin_system, 'Satellite', star_system.system_age
        from satellite
        join planet on satellite.parent_planet = planet.object_id
        join star_system on planet.origin_system = star_system.system_name
        where satellite_name like :1
    """
    cursor.execute(query, {'1': keyword + '%'})

    result = cursor.fetchall()
    #print(result)

    data = [{"misc_name": row[0], "parent_system": row[1], "misc_category": row[2], "distance": row[3]} for row in result]
    cursor.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
