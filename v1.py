from flask import Flask, jsonify, g
from flask_restful import Api, Resource
import json
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

# Global variables
TIME_SUM = 0
COUNT = 0
PATH = r"C:\Users\Gil\PycharmProjects\api\data\input-2.json"


# This function reads the json file and stores each element in the relevant list
def read_and_store():
    with open(PATH) as file:
        json_str = file.read()
        json_dict = json.loads(json_str)
    vms_dict = json_dict['vms']
    fwr_dict = json_dict['fw_rules']

    class Attack(Resource):
        def get(self, vm_id):
            global COUNT
            COUNT += 1
            vm_tags = []
            can_access = []
            src_tag = ""
            # Check if the vm exist in input, there is only one because every ID is unique
            vm = next(filter(lambda x: x['vm_id'] == vm_id, vms_dict), None)
            if vm is not None:
                # vm_tags - all tags that are in the tags section in the input vm
                vm_tags.append(vm['tags'])
            else:
                return "VM not found!"
            for fw in fwr_dict:
                if fw['dest_tag'] in vm_tags[0]:
                    # dest_tag = fw['dest_tag']
                    src_tag = fw['source_tag']
                for vms in vms_dict:
                    if src_tag in vms['tags']:
                        can_access.append(vms['vm_id'])
            # Remove duplicates
            res = []
            [res.append(x) for x in can_access if x not in res]
            return jsonify(res)

    class Stats(Resource):
        def get(self):
            global COUNT
            COUNT += 1
            return jsonify(vm_count=len(vms_dict), request_count=COUNT,
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
