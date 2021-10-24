from flask import Flask, jsonify, g
from flask_restful import Api, Resource
import json
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

virtual_machines = []
firewall_rules = []
vm_dict = {}
TIME_SUM = 0
COUNT = 0


# This function reads the json file and stores each element in the relevant list
def read_and_store():
    with open(r"C:\Users\Gil\PycharmProjects\api\data\input-0.json") as file:
        json_str = file.read()
        json_dict = json.loads(json_str)
    virtual_machines.append(json_dict['vms'])
    firewall_rules.append(json_dict['fw_rules'])
    print(json_dict['vms'])


    class Attack(Resource):
        def get(self, vm_id):
            global COUNT
            COUNT += 1
            vm_tags = []
            can_access = []
            dest_tag = ""
            src_tag = ""
            # Check if the vm exist in input
            vm = next(filter(lambda x: x['vm_id'] == vm_id, virtual_machines), None)
            if vm is not None:
                # Append all tags of found vm in a list
                vm_tags.append(vm['tags'])
            else:
                return "VM not found!"
            for fw in firewall_rules[0]:
                if fw['dest_tag'] in vm_tags[0]:
                    dest_tag = fw['dest_tag']
                    src_tag = fw['source_tag']
            for vm_acc in virtual_machines:
                if src_tag in vm_acc['tags']:
                    can_access.append(vm_acc['vm_id'])
                return jsonify(can_access)

    class Stats(Resource):
        def get(self):
            global COUNT
            COUNT += 1
            return jsonify(vm_count=len(virtual_machines), request_count=COUNT,
                           average_request_time=(TIME_SUM / COUNT))

    @app.before_request
    def before_request():
        g.start = time.time()

    @app.after_request
    def after_request(response):
        global TIME_SUM
        diff = time.time() - g.start
        TIME_SUM += diff
        return response

    api.add_resource(Attack, '/attack', '/attack/<string:vm_id>')
    api.add_resource(Stats, '/stats')

    if __name__ == '__main__':
        read_and_store()
        app.run(port=5000)
