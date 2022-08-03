from logging import exception
import uuid
import numpy as np
import pandas as pd
from my_modules.dataset import jobhist


def get_job_hist_count(cursor):
    cursor.execute('select count(*) from job_hist')
    return cursor.fetchone()


def initialize(cursor):
    is_exist = False
    with cursor() as cur:
        job_hist_count, = get_job_hist_count(cur)

        if job_hist_count > 0:
            is_exist = True
            #     cur.execute('delete from job_index')
            #     job_id_count, = get_job_id_count(cur)
            #     job_hist_count, = get_job_hist_count(cur)

        if job_hist_count == 0:
            cur.execute('alter table job_hist auto_increment = 0')
            print('myjobhist db is initialized.\n')

    return is_exist


def insert_data_from_file(cursor):

    count_executed = 0
    if initialize(cursor) == True:
        return count_executed

    myjobs = pd.read_excel('./data/MyJobHistory.xlsx', skiprows=1).to_numpy()

    print('Start inserting to DB after encoding from numpy array job list...\n')
    query_job_history = 'insert into job_hist (hist_id, raw_data) values (%s, %s)'

    with cursor() as cur:
        for index, job in enumerate(myjobs):
            try:
                encoded = jobhist(job).to_encode_from_json()
                history_id = uuid.uuid4()
                cur.execute(query_job_history, (history_id, encoded))
                print("[{}] type : {} , data : {}".format(
                    str(index).zfill(2), type(encoded), encoded))
                count_executed += 1
            except Exception as e:
                print(e)
                continue

    print('Finished inserting to DB after encoding from numpy array job list...\n')
    return count_executed


def get_data_from_db(cursor):
    query_history = 'select * from job_hist'

    data_list = []
    with cursor() as cur:
        cur.execute(query_history)
        job_hists = np.array(cur.fetchall())

        for hist in job_hists:
            index_id = hist[0]
            hist_id = hist[1]
            job_hist = jobhist().to_decode_to_jobhist(hist[2])
            data_list.append([index_id, job_hist])
            print("[{}] type : {}, hist_id : {} ,data : {}\n".format(
                str(int(index_id)).zfill(2), type(job_hist), hist_id, job_hist))

    print('Finished decoding from encrypted job list...')
    return data_list
