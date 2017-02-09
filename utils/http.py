import json
import httplib
import random

from models.credentials import Credentials


class AgriHubAPI:
    def __init__(self):
        with open('settings.json') as json_settings:
            self.settings = json.load(json_settings)
        self.headers = {'Content-Type': 'application/json'}
        self.credential_model = Credentials()

    def createconnection(self):
        return httplib.HTTPConnection(self.settings.get('api_url'))

    def auth(self):
        conn = self.createconnection()
        data = json.dumps({
            "user": self.settings.get('user'),
            "label": self.settings.get('node')['label'],
            "secretkey": self.settings.get('node')['secretkey']
        })
        conn.request('POST', '/node-auth/', data, self.headers)
        res = conn.getresponse()
        if 200 == res.status:
            res_data = json.loads(res.read())
            self.credential_model.set(res_data.get('token'), res_data.get('node')['subsperdayremain'])
        else:  # 400
            print 'TODO simpan error di log'
        conn.close()

    def subscribe(self):
        credential = self.credential_model.get()
        # if node has no remaining subs, then ignore it
        if 0 == credential[1] or -1 != credential[1]:
            return
        conn = self.createconnection()
        sensors = self.settings.get('node')['sensors']
        data_raw = {
            "user": self.settings.get('user'),
            "node": self.settings.get('node')['label'],
            "sensor": [],
            "testing": True
        }
        for sensor in sensors[0]:
            # TODO data should captured with sensor module
            data_raw.get('sensor').append({
                "label": sensor,
                "data": random.randint(100, 999)
            })
        # TODO sent new auth() when token is expired
        self.headers.update({'Authorization': "JWT %s" % (credential[0])})
        conn.request('POST', '/subscriptions/', json.dumps(data_raw), self.headers)
        res = conn.getresponse()
        print res.read()

