'''
A program that receives messages from MQTT broker and writes data and makes queries to Postgresql.
A query should be published to topic <hostname>/database/query and the payload should be a json
that contains the query as a string and variables that replace the %s instances as a list, e.g.
{ 
    "table": "water_world_config"
}
When writing data to Postgresql it should be published to topic <hostname>/database/write and the payload
should be a json that contains a query string, a list of columns and a list of values 
that replace the %s instances in the query, e.g.
{
    "table": "water_world_waterpump"
    "columns": ["liters_per_minute", "hours_between_sensor_reads"],
    "values": [10, 2]
}
note: use SQL("INSERT INTO table1 {} VALUES (%s)").format(sql.Identifier('column1')),
    [10, 20])
postgres is running on port 5432
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
from psycopg2 import sql

def create_insert_query(data):
    query = sql.SQL(
        'INSERT INTO {table} {columns} VALUES {values}').format(
            table = sql.Identifier(data['table']), 
            columns = sql.Identifier(data['columns']),
            values = sql.Identifier(data['values'])
        )
    return query

def create_fetch_all_query(data):
    query = sql.SQL(
        'SELECT * FROM {table}').format(
            table = sql.Identifier(data['table'])
    )
    return query
    

def on_connect(client, userdata, flags, rc):
    global subscribeTopic
    print("Connected to MQTT with result code " + str(rc))
    client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
    global host, USER, PASSWORD
    try:
        connection = psycopg2.connect('dbname=postgres user=' + USER + ' password=' + PASSWORD)
        cursor = connection.cursor()

        data = json.loads(msg.payload.decode("utf-8"))

        if 'write' in msg.topic:

            insert_query = create_insert_query(data)

            cursor.execute(insert_query)
            connection.commit()

            success_event_query = create_insert_query({
                'table': 'water_world_event',
                'columns': ['message', 'event_type', 'event_time'],
                'values': [
                    'Successfully wrote point to database: ' + str(insert_query),
                    'Success',
                    datetime.datetime.now()
                    ]
                })
            cursor.execute(success_event_query)
            connection.commit()
            

        elif 'query' in msg.topic:

            select_query = create_fetch_all_query(data)
            cursor.execute(select_query)
            list_of_rows = cursor.fetchall()

            client.publish(topic = host + '/store/query', payload = json.dumps(list_of_rows))

        connection.close()

    except OSError as oe:
        os_error_event_query = create_insert_query({
                'table': 'water_world_event',
                'columns': ['message', 'event_type', 'event_time'],
                'values': [
                    'OSError occured: ' + format_exc,
                    'Error',
                    datetime.datetime.now()
                    ]
                })
        cursor.execute(os_error_event_query)
        connection.commit()
        connection.close()
        raise oe

    except Exception:
        exception_event_query = create_insert_query({
                'table': 'water_world_event',
                'columns': ['message', 'event_type', 'event_time'],
                'values': [
                    'Exception occured: ' + format_exc,
                    'Warning',
                    datetime.datetime.now()
                    ]
                })
        cursor.execute(exception_event_query)
        connection.commit()
        connection.close()
        

if __name__ == '__main__':

    # loading environment variables from .env and fetching db user and password
    load_dotenv()
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')


    # Initializing the MQTT client
    host = gethostname()
    subscribeTopic = host + '/database/#'
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    # Looping MQTT callback functions
    client.loop_forever()