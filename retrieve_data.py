from sqlalchemy import create_engine
import pandas as pd

from config import POSTGRES_HEROKU_PASSWORD_2

from decimal import *
import os

# POSTGRES_HEROKU_PASSWORD_2=os.environ.get('POSTGRES_HEROKU_PASSWORD_2')
# Create PostgreSQL engine
postgres_heroku_path_2 = f"postgresql://acurubwqqcguqg:{POSTGRES_HEROKU_PASSWORD_2}@ec2-107-20-153-39.compute-1.amazonaws.com:5432/dd87jp2gm4bgdr"
engine = create_engine(postgres_heroku_path_2)

def to_dict(data):
    dicts = []
    for row in list(data):
        row = list(row)
        dictionary = {}
        dictionary["company"] = row[1]
        dictionary["last_updated"] = row[2]
        dictionary["scooter_id"] = row[3]
        dictionary["lat"] = float(row[4]) * 1.0
        dictionary["lon"] = float(row[5]) * 1.0
        dictionary["is_reserved"] = row[6]
        dicts.append(dictionary)
    
    return dicts

def get_all():
    data = engine.execute("SELECT * FROM scooters;")
    return to_dict(data)
    

def get_by_name(name, limit):
    data = engine.execute(f"SELECT * FROM scooters WHERE company = '{name}' LIMIT {limit}")
    return to_dict(data)

def get_latest():
    data = engine.execute("""
        SELECT * FROM scooters AS a
        WHERE last_updated in (
                SELECT min(last_updated) FROM scooters WHERE company = 'spin') 
                AND a.company = 'spin'
            OR last_updated in (
                SELECT min(last_updated) FROM scooters WHERE company = 'razor') 
                AND a.company = 'razor'
            OR last_updated in (
                SELECT min(last_updated) FROM scooters WHERE company = 'helbiz') 
                AND a.company = 'helbiz';
    """)

    return to_dict(data)

def get_last_hours(num):
    sql_query = f"""
        SELECT * FROM scooters
        WHERE 
            company = 'spin' AND last_updated >= (
                SELECT MIN(last_updated) - {num} * 3600 FROM scooters WHERE company = 'spin'
            ) 
            OR 
            company = 'razor' AND last_updated >= (
                SELECT MIN(last_updated) - {num} * 3600 FROM scooters WHERE company = 'razor'
            ) 
            OR 
            company = 'razor' AND last_updated >= (
                SELECT MIN(last_updated) - {num} * 3600 *1000 FROM scooters WHERE company = 'helbiz'
            );
    """

    df = pd.read_sql(sql_query, engine)
    df = df[["company", "bike_id", "last_updated", "lat", "lon"]]

    bike_records = {}
    for i in range(len(df)):
        bike = df.iloc[i]
        bike_id = bike["bike_id"]
        if bike_id not in bike_records:
            bike_records[bike_id] = {
                "coordinates": [
                    [float(bike["lat"])*1.0, float(bike["lon"])*1.0]
                ],
                "timestamps": [ int(bike["last_updated"]) ]
            }
        else:
            bike_records[bike_id]["coordinates"].append([float(bike["lat"])*1.0, float(bike["lon"])*1.0])
            bike_records[bike_id]["timestamps"].append( int(bike["last_updated"]) )
    
    return bike_records


# data = get_last_hours(1)
# print(type(data))