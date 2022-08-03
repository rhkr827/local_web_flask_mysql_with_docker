import json
import pymysql
from my_modules.query import *


def run():
    with open('./settings.json', 'r') as f:
        config = json.load(f)

    host = config['host']
    port = config['port']
    database = config['database']
    username = config['username']
    password = config['password']

    conn = pymysql.connect(host=host,
                           user=username,
                           password=password,
                           db=database,
                           port=port,
                           charset='utf8')
    cursor = conn.cursor
    # insert to db after encoding data
    count_executed = insert_data_from_file(cursor)

    if count_executed > 0:
        conn.commit()

    # select from db after decoding data
    data_list = get_data_from_db(cursor)

    conn.close()

    return data_list
