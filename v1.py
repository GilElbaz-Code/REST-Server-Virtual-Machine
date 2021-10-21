from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json

app = Flask(__name__)

api = Api(app)

virtual_machines = []
firewall_rules = []


# This function reads the json file and stores each element in the relevant list
def read_and_store():
    with open(r"C:\Users\Gil\PycharmProjects\api\data\input-0.json") as file:
        json_str = file.read()
        json_dict = json.loads(json_str)
    virtual_machines.append(json_dict['vms'][0])
    firewall_rules.append(json_dict['fw_rules'])

class Attack(Resource):
    def get(self, vm_id):
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
        return {"vm_count:": len(virtual_machines)}


api.add_resource(Attack, '/attack', '/attack/<string:vm_id>')
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    read_and_store()
    # print(virtual_machines)
    # print(firewall_rules)
    app.run(port=5000)
