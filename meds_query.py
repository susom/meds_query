import requests
import json
import sys


class MedsQuery:
    def __init__(self, ace_url):
        self.pid_arr = None
        self.pos = -1
        self.url = ace_url

    def query(self, tql):
        request_object = {"query": tql}
        print(request_object)
        response = requests.get(self.url + "/query", data=json.dumps(request_object))
        pids = response.json().get("patientIds")
        self.pid_arr = []
        for (i, pid) in enumerate(pids):
            self.pid_arr.append(pid[0])
        self.pos = -1

    def has_next(self):
        return len(self.pid_arr) > 0 and self.pos < len(self.pid_arr) - 1

    def next(self):
        self.pos = self.pos + 1
        request_object = {"pids": [self.pid_arr[self.pos]]}
        return requests.get(self.url + "/meds", data=json.dumps(request_object)).json()

print("Usage: URL TQL")
iterator = MedsQuery(sys.argv[1])
iterator.query(sys.argv[2])
while iterator.has_next():
    meds_object = iterator.next()
    print(meds_object)
