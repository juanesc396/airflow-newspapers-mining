from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

IP_LOCAL = os.environ.get('IPPC')
CLIENT = MongoClient(f"mongodb://{IP_LOCAL}:27017/")

def mongodb_check():
    """
    Function that verify the connection status, it's used as a sensor
    """
    IP_LOCAL = os.environ.get('IPPC')
    CLIENT = MongoClient(f"mongodb://{IP_LOCAL}:27017/")

    try:
        CLIENT.admin.command('ping')
        return True
    except ConnectionFailure:
        print("Server not available")

def clean_duplicates():
    newspapers_db = CLIENT['Newspapers']

    for coll in newspapers_db.list_collection_names():
        # Cursor with all duplicated documents
        replic = newspapers_db[coll].aggregate([
            {'$group': {'_id': {'title': '$title'},
                        'uniqueID': {'$addToSet': '$_id'},
                        'total': {'$sum': 1}
                    }
            },
        # Holds how many duplicates for each group, if you need it.
            {'$match': {'total': {'$gt': 1}
                    }
            }
        ])
                                # Result is a list of lists of ObjectsIds
        for i in replic:
            for idx, j in enumerate(i['uniqueID']):             # It holds the ids of all duplicates 
                if idx != 0:                                    # Jump over first element to keep it
                    newspapers_db[coll].delete_one({'_id': j})   # Remove the rest