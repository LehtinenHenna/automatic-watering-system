import app.store_deprecated as store_deprecated
import pytest
from unittest.mock import patch
from unittest.mock import Mock
from socket import gethostname
import json
import os
from dotenv import load_dotenv

client = Mock()
userdata = Mock()
msg = Mock()
load_dotenv()
store_deprecated.USER = os.getenv('USER')
store_deprecated.PASSWORD = os.getenv('PASSWORD')

@patch('store.create_insert_query')
@patch('store.psycopg2.connect')
def test_osError(mock_connect, mock_insert_query):
    mock_insert_query.side_effect = OSError
    msg.topic = gethostname() + '/database/write'
    msg.payload = json.dumps({
        "table": "water_world_waterpump",
        "columns": ["pump_activated", "pump_stopped"],
        "values": ["2012-03-19T07:22Z", "2012-03-19T07:23Z"]
    }).encode()
    with pytest.raises(OSError):
        store_deprecated.on_message(client=client, userdata=userdata, msg=msg)