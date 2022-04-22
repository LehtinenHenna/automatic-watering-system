'''
A program that receives messages from MQTT broker and writes data and makes queries to Postgresql.
A query should be published to topic <hostname>/database/query and the payload should be a json
that contains the table name, e.g.
{ 
    "table": "water_world_config"
}
store.py publishes the data received by the query to <hostname>/store/data

When writing data to Postgresql it should be published to topic <hostname>/database/write and the payload
should be a json that contains a table name, a list of columns and a list of values, e.g.
{
    "table": "water_world_waterpump"
    "columns": ["pump_activated", "pump_stopped"],
    "values": ["2012-03-19T07:22Z", "2012-03-19T07:23Z"]
}
Note that the number of columns needs to match the number of values.
'''
#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import datetime
import psycopg2 # postgresql
from psycopg2 import sql
import json
from dotenv import load_dotenv
import os
from socket import gethostname
from traceback import format_exc


def create_insert_query(data):
    # create (col1, col2...)
    columns = ",".join(data['columns'])
    # create VALUES("%s", "%s"...) one %s per value
    values = "VALUES({})".format(",".join("%s" for values in data['values']))
    # create "INSERT INTO table (col1, col2...) VALUES(%s, %s...)"
    query = "INSERT INTO {} ({}) {}".format(data['table'], columns, values)
    return query

def create_fetch_all_query(data):
    query = sql.SQL(
        "SELECT * FROM {table}").format(
            table = sql.Identifier(data['table'])
    )
    return query
    

def on_connect(client, userdata, flags, rc):
    global subscribeTopic
    print("Connected to MQTT with result code " + str(rc))
    client.subscribe(subscribeTopic)


def on_message(client, userdata, msg):
    print('message received')
    global host, USER, PASSWORD

    connection = psycopg2.connect(user=USER,
        password=PASSWORD,
        port="5432",
        host='water_world_db',
        database="postgres")

    cursor = connection.cursor()

    try:
        data = json.loads(msg.payload.decode("utf-8"))

        if 'write' in msg.topic:

            insert_query = create_insert_query(data)
            print(insert_query)

            cursor.execute(insert_query, data['values'])
            connection.commit()

            print('Successfully wrote point to database: ' + str(insert_query))
            success_values = [
                    'Successfully wrote point to database: ' + str(insert_query) + str(data['values']),
                    'Success',
                    datetime.datetime.now()
                    ]
            success_event_query = create_insert_query({
                'table': 'water_world_event',
                'columns': ['message', 'event_type', 'event_time'],
                'values': success_values
                })
            cursor.execute(success_event_query, success_values)
            connection.commit()
            

        elif 'query' in msg.topic:

            select_query = create_fetch_all_query(data)
            print('select_query: ', select_query)
            cursor.execute(select_query)
            row_tuple = cursor.fetchone()
            print('row_tuple: ', row_tuple)

            client.publish(topic = host + '/store/data', payload = json.dumps(row_tuple[1:]))

        connection.close()

    except OSError as oe:
        os_error_values = [
                    'OSError occured: ' + format_exc(),
                    'Error',
                    datetime.datetime.now()
                    ]
        os_error_event_query = create_insert_query({
                'table': 'water_world_event',
                'columns': ['message', 'event_type', 'event_time'],
                'values': os_error_values
                })
        cursor.execute(os_error_event_query, os_error_values)
        connection.commit()
        connection.close()
        raise oe

    except Exception:
        exception_values = [
                    'Exception occured: ' + format_exc(),
                    'Warning',
                    str(datetime.datetime.now())
                    ]
        exception_event_query = create_insert_query({
                'table': 'water_world_event',
                'columns': ['message', 'event_type', 'event_time'],
                'values': exception_values
                })
        cursor.execute(exception_event_query, exception_values)
        connection.commit()
        connection.close()
        

if __name__ == '__main__':
    print('Running store.py')

    # loading environment variables from .env and fetching db user and password
    load_dotenv()
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')


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