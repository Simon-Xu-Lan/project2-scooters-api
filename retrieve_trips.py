import pymongo


ATLAS_PASSWORD = "codeforfun2020"
atlas_conn = f'mongodb+srv://simon:{ATLAS_PASSWORD}@cluster0.23jm7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

def get_all_trips():
    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB
        collection = db.trips
        data = collection.find({},{'_id': False})
    return list(data)

def get_recent_trips_by_hours(num):
    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB 
        collection = db.time_log
        time_log = collection.find({})
        latest_start = list(time_log)[0]["latest_start"]

    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB 
        collection = db.trips
        data = collection.find(
            {'trip_start_at': {"$gte": latest_start - 3600 * int(num) }},
            {'_id': False}
        )
    
    return list(data)

def get_recent_trips_by_hours(num):
    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB 
        collection = db.time_log
        time_log = collection.find({})
        latest_start = list(time_log)[0]["latest_start"]

    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB 
        collection = db.trips
        data = collection.find(
            {'trip_start_at': {"$gte": latest_start - 3600 * int(num) }},
            {'_id': False}
        )
    
    return list(data)

def get_trips_by_company(name, hours):
    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB 
        collection = db.time_log
        time_log = collection.find({})
        latest_start = list(time_log)[0]["latest_start"]
    
    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB 
        collection = db.trips
        if hours == 'all':
            data = collection.find(
                {'company': name},
                {'_id': False}
            )
        else:
            data = collection.find(
                {
                    'trip_start_at': {"$gte": latest_start - int(hours) * 3600},
                    'company':'razor'
                }, 
                {'_id': False}
            )

    return list(data)

def get_summary():
    with pymongo.MongoClient(atlas_conn) as client:
        db = client.scooters_DB
        collection = db.summary
        data = collection.find({}, {'_id': False})

    return list(data)


    