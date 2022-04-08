'''
A program that receives messages from MQTT broker and writes data and makes queries to Postgresql.
A query should be published to topic <hostname>/database/query and the payload should be a json
that contains the query as a string and variables that replace the %s instances as a list, e.g.
{ 
    "query": 
        "SELECT *
        FROM %s
        ORDER BY timestamp DESC 
        LIMIT 1", 
    "variables": 
        ["configuration"]
}
When writing data to Postgresql it should be published to topic <hostname>/database/write and the payload
should be a json that contains a query string, a list of columns and a list of values 
that replace the %s instances in the query, e.g.
{
    "query": "INSERT INTO numbers {} VALUES (%s, %s)", 
    "columns": ["liters_per_minute", "hours_between_sensor_reads"],
    "values": [10, 2]
}
'''
#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import datetime
import psycopg2 # postgresql
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
    global publishTopic

    connection = psycopg2.connect("dbname=waterworld user=jorma")
    cursor = connection.cursor()
    
    receiveTime=datetime.datetime.now()
    data = json.loads(msg.payload.decode("utf-8"))

    if 'write' in msg.topic:
        try:
            query = data['query']



            cursor.execute(insertion)
            client.publish(topic = publishTopic + '/event/success', payload = 'point written to database: ' + str(insertion))

            connection.commit()
        except:
            print('Error occurred:', format_exc())

    elif 'query' in msg.topic:
        try:
            query = data['query']
            queryVariables = data['variables']


        except:
            print('Error occurred:', format_exc())

    connection.close()

        

if __name__ == '__main__':
    '''
    # loading environment variables from .env and fetching MONGODB_URI
    load_dotenv()
    MONGODB_URI = os.getenv('MONGODB_URI')

    
    # Set up client for MongoDB
    mongoClient = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    try:
        print('mongoClient server info:', mongoClient.server_info())
    except Exception:
        print("Unable to connect to the server.")
    db = mongoClient.waterworld
    collection = db.wateringSystem
    '''
    


    # Initialize the MQTT client
    subscribeTopic = gethostname() + '/database/#'
    publishTopic = gethostname() + '/store'
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    # Looping MQTT callback functions
    client.loop_forever()