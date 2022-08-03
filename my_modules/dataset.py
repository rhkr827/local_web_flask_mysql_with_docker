import json
import base64
from datetime import datetime
# company name, role , location , start_date, resignation_date


class jobhist(object):
    def __init__(self, job=None):
        if job is None:
            self.company_name = None
            self.position = None
            self.role = None
            self.location = None
            self.start_date = None
            self.resignation_date = None
            self.remark = None
        else:
            self.company_name = job[0]
            self.position = job[1]
            self.role = job[2]
            self.location = job[3]
            self.start_date = str(job[4])
            self.resignation_date = str(job[5])
            self.remark = job[6]

    def to_encode_from_json(self):
        return base64.b64encode(json.dumps(self.__dict__).encode('ascii'))

    def to_decode_to_jobhist(self, data):
        return json.loads(base64.b64decode(data).decode('ascii'))
