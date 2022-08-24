import json
import pymysql
from .query import *
import traceback


def run():
    joblist = None
    jobsummary = None
    try:
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

        # crete jobhist table if not exist
        # sql = open('create_jobhist_table.sql').read()
        # cursor.execute(sql)

        # insert to db after encoding data
        count_executed = insert_data_from_file(cursor)

        if count_executed > 0:
            conn.commit()

        # select from db after decoding data
        joblist, jobsummary = get_data_from_db(cursor)

        cursor.fetch()
        conn.close()
    except:
        print(traceback.format_exc())

    return joblist, jobsummary
