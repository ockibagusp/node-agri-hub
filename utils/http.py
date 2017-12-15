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
            "label": self.settings.get('supernode')['label'],
            "secretkey": self.settings.get('supernode')['secretkey']
        })
        conn.request('POST', '/node-auth/', data, self.headers)
        res = conn.getresponse()
        if 200 == res.status:
            print 'AUTH: ok'
            res_data = json.loads(res.read())
            conn.close()
            self.credential_model.set(res_data.get('token'))
        else:  # 400
            conn.close()
            # TODO simpan error di log
            exit('AUTH: failure')

    def publish(self, testing=True):
        # konfigurasi diambil dari settings.json
        credential = self.credential_model.get()
        conn = self.createconnection()
        nodes = self.settings.get('supernode')['nodes']
        data_raw = {
            "label": self.settings.get('supernode')['label'],
            "nodes": [],
            "testing": testing
        }

        for node in nodes:
            # TODO data should captured with sensor module
            _node = {
                "id": node.get('id'),
                "format": self.settings.get('format'),
                "sensors": []
            }

            for sensor in node.get('sensors'):
                _sensor = {
                    "label": sensor,
                    "value": []
                }

                for i in range(3):
                    _sensor.get("value").append([
                        random.randint(100, 999), #  random data
                        1509426290
                    ])

                _node.get('sensors').append(_sensor)

            data_raw.get('nodes').append(_node)

        print "---- data yang dikirim ---"
        print json.dumps(data_raw)
        self.headers.update({'Authorization': "JWT %s" % (credential[0])})
        conn.request('POST', '/sensordatas/', json.dumps(data_raw), self.headers)
        res = conn.getresponse()

        # sent new auth() when token is expired
        if 401 == res.status:
            print "Subs status: 401"
            print res.read()
            print "Renew token..."
            self.auth()
            self.publish()
        else:
            print "Subs status: 200 (ok)"
