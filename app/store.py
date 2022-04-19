'''
A program that receives messages from MQTT broker and writes data and makes queries to MongoDB.
A query should be published to topic <hostname>/database/query and the payload should be a json
that contains the table name, e.g.
{ 
    "table": "water_world_config"
}
store.py publishes the data received by the query to <hostname>/store/data

When writing data to Postgresql it should be published to topic <hostname>/database/write and the payload
should be a json that contains a table name, a list of columns and a list of values, e.g.
{
    "table": "water_world_waterpump",
    "insert_dict": {
        "pump_activated": "2012-03-19T07:22Z",
        "pump_stopped": "2012-03-19T07:23Z",
    }
}
Note that the number of columns needs to match the number of values.
'''
#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import datetime
import pymongo
import json
from dotenv import load_dotenv
import os
from socket import gethostname
from traceback import format_exc
    

def on_connect(client, userdata, flags, rc):
    global subscribeTopic
    print("Connected to MQTT with result code " + str(rc))
    client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
    print('message received')
    global host, db

    try:
        print('msg.payload.decode()', msg.payload.decode())
        data = json.loads(msg.payload.decode())
        collection = db[data['table']]
        event_collection = db['water_world_event']

        if 'write' in msg.topic:

            insertion = collection.insert_one(data['insert_dict'])
            print(insertion)

            print('Successfully wrote point to database: ' + str(insertion))

            success_event_insertion = event_collection.insert_one({
                'message': 'Successfully wrote point to database: ' + str(insertion),
                'event_type': 'Success',
                'event_time': datetime.datetime.now()
            })

        elif 'query' in msg.topic:

            data = collection.find_one()
            
            if '_id' in data:
                del data['_id']
            print('data: ', data)

            client.publish(topic = host + '/store/data', payload = json.dumps(data))

    except OSError as oe:
        event_collection = db['water_world_event']
        os_error_insertion = event_collection.insert_one({
                'message': 'OSError occured: ' + format_exc(),
                'event_type': 'Error',
                'event_time': datetime.datetime.now()
            })
        raise oe

    except Exception:
        event_collection = db['water_world_event']
        os_error_insertion = event_collection.insert_one({
                'message': 'Exception occured: ' + format_exc(),
                'event_type': 'Warning',
                'event_time': datetime.datetime.now()
            })


if __name__ == '__main__':
    print('Running store.py')

    # loading environment variables from .env and fetching db user and password
    # and initializing MongoDB connection
    load_dotenv()
    MONGODB_URI = os.getenv('MONGODB_URI')
    print('MONGODB_URI', MONGODB_URI)
    client = pymongo.MongoClient(MONGODB_URI)
    db = client['waterworld']
    print('db:', db)

    # Initializing the MQTT client
    host = gethostname()
    print('host: ', host)
    subscribeTopic = host + '/database/#'
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('mqtt', 1883, 60)

    # Looping MQTT callback functions
    client.loop_forever()