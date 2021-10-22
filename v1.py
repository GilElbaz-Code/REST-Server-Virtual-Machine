from flask import Flask, request, jsonify, g
from flask_restful import Api, Resource
from flask_profiler import Profiler, flask_profiler
import json
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

virtual_machines = []
firewall_rules = []
diffs = []
COUNT = 0


# This function reads the json file and stores each element in the relevant list
def read_and_store():
    with open(r"C:\Users\Gil\PycharmProjects\api\data\input-0.json") as file:
        json_str = file.read()
        json_dict = json.loads(json_str)
    virtual_machines.append(json_dict['vms'][0])
    firewall_rules.append(json_dict['fw_rules'])


class Attack(Resource):
    def get(self, vm_id):
        global COUNT
        COUNT += 1
        vm_tags = []
        fw_tags = []
        vm = next(filter(lambda x: x['vm_id'] == vm_id, virtual_machines), None)
        for fw in firewall_rules:
            pass
        if vm is not None:
            vm_tags.append(vm['tags'])
            return vm_tags
        else:
            return "VM not found!"


class Stats(Resource):
    def get(self):
        global COUNT
        COUNT += 1
        return jsonify(vm_count=len(virtual_machines), request_count=COUNT,
                       average_request_time=(sum(diffs) / len(diffs)))


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = time.time() - g.start
    diffs.append(diff)
    return response



api.add_resource(Attack, '/attack', '/attack/<string:vm_id>')
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    read_and_store()
    app.run(port=5000)
