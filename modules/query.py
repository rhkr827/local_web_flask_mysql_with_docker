from cmath import isnan
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid
import numpy as np
import pandas as pd
from dateutil import parser
from itertools import groupby

from .dataset import jobhist


def get_job_hist_count(cursor):
    cursor.execute('select count(*) from job_hist')
    return cursor.fetchone()


def initialize(cursor, use_delete=False):
    is_exist = False
    with cursor() as cur:
        job_hist_count, = get_job_hist_count(cur)

        if job_hist_count > 0:
            if use_delete:
                cur.execute('delete from job_hist')
                job_hist_count, = get_job_hist_count(cur)
            else:
                is_exist = True

        if job_hist_count == 0:
            cur.execute('alter table job_hist auto_increment = 0')
            print('myjobhist db is initialized.\n')

    return is_exist


def insert_data_from_file(cursor):

    count_executed = 0
    if initialize(cursor) == True:
        return count_executed

    myjobs = pd.read_excel('./data/MyJobHistory.xlsx', skiprows=1)
    myjobs.fillna('', inplace=True)
    myjobs = myjobs.to_numpy()

    print('Start inserting to DB after encoding from numpy array job list...\n')
    query_job_history = 'insert into job_hist (hist_id, raw_data) values (%s, %s)'

    with cursor() as cur:
        for job in myjobs:
            try:
                encoded = jobhist(job).to_encode_from_json()
                history_id = uuid.uuid4()
                cur.execute(query_job_history, (history_id, encoded))
                # print("[{}] type : {} , data : {}".format(str(index).zfill(2), type(encoded), encoded))
                count_executed += 1
            except Exception as e:
                print(e)
                continue

    print('Finished inserting to DB after encoding from numpy array job list...\n')
    return count_executed


def get_statistics(jobhist):
    summary = []
    pos_period_list = []
    for job in jobhist:
        pos = job['position']
        resign_date = parser.parse(job['resignation_date'])
        start_date = parser.parse(job['start_date'])
        period = relativedelta(resign_date, start_date)
        pos_period_list.append({'position': pos, 'relative_period': period, 'delta_period': resign_date - start_date})

    sorted_list = sorted(pos_period_list, key=lambda k: k['position'])
    for key, values in groupby(sorted_list, key=lambda k: k['position']):
        item = {'position': key, 'period': relativedelta(0), 'delta_period': 0}
        for value in values:
            item['period'] += value['relative_period']
            item['delta_period'] += value['delta_period'].days

        # convert days to year,month and day
        delta = item['period']
        period = ''
        if delta.years > 0:
            period += f'{delta.years}y '

        if delta.months > 0:
            period += f'{delta.months}m '

        period += f'{delta.days}d'

        item['period'] = period
        summary.append(item)

    # sorted
    sorted_summary = sorted(summary, key=lambda k: k['delta_period'], reverse=True)

    # get position and period
    new_list_dict = []
    for l in sorted_summary:
        new_dic = {}
        for k, v in l.items():
            if k in ['position', 'period']:
                new_dic.update({k: v})

        new_list_dict.append(new_dic)

    return new_list_dict


def get_data_from_db(cursor):
    query_history = 'select * from job_hist'

    data_list = []
    with cursor() as cur:
        cur.execute(query_history)
        job_hists = np.array(cur.fetchall())

        for hist in job_hists:
            # index_id = hist[0]
            # hist_id = hist[1]
            job_hist = jobhist().to_decode_to_jobhist(hist[2])
            data_list.append(job_hist)
            # print("[{}] type : {}, hist_id : {} ,data : {}\n".format(
            #     str(int(index_id)).zfill(2), type(job_hist), hist_id, job_hist))

    # get summary
    data_summary = get_statistics(data_list)
    print('Finished decoding from encrypted job list...')
    return data_list, data_summary
