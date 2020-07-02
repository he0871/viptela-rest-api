# Copyright: Ngena USA LLC.,
# Author: Jingyuan He (Mark)
# Date : July 1st 2020
from vmanage import rest_api_lib;
from NewPolicy import  newpolicy

class updatePolicy:

    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.username = username
        self.password = password
        self.obj = rest_api_lib(self.vmanage_ip, self.username, self.password)

    #This function will return a policy id of the active policy
    #If no policy is active, will return a None
    def find_active_policy(self):
        mount_point = "template/policy/vsmart"
        respond = self.obj.get_request(mount_point)
        if respond.status_code != 200:
            print(respond)
            return None
        records = respond.json()['data']
        print(len(records))
        for item in records:
            if item['isPolicyActivated'] == True:
                return item
        return None

    def find_policy_byName(self, pName):
        mount_point = "template/policy/vsmart"
        respond = self.obj.get_request(mount_point)
        if respond.status_code != 200:
            print(respond)
            return None
        records = respond.json()['data']
        print(len(records))
        for item in records:
            if item['policyName'] == pName:
                return item
        return None

    def deactive_policy(self, policy):
        policyId = policy['policyId']
        mount_point = 'template/policy/vsmart/deactivate/' + policyId
        payload = {}
        respond = self.obj.post_request(mount_point, payload)
        print(respond)
        if respond.status_code == 403:
            print(respond)
            return None
        records = respond.json()
        print(len(records))
        return records

    def put_update(self, policy):
        policyId = policy['policyId']
        policyName = policy['policyName']
        policyVersion = policy['policyVersion']
        mount_point = "template/policy/vsmart/" + policyId
        payload = {
            "policyId": policyId,
            "policyState": 'edit',
            "policyName": policyName,
            "policyDefinition": newpolicy,
            "isPolicyActivated": True,
            "policyDescription": "API test & encode test",
            "policyType": "cli",
            "isEdited": True,
            "policyVersion": policyVersion
        }

        respond = self.obj.put_request(mount_point, payload)
        if respond.status_code != 200:
            print(respond)
            return None
        records = respond.json()
        print(len(records))
        return records

    def commit_modify(self, policy):
        policyId = policy['policyId']
        print(policy['policyName'])
        mount_point = "template/policy/vsmart/activate/" + policyId
        payload = {"isEdited": False}
        respond = self.obj.post_request(mount_point,payload)
        if respond.status_code != 200:
            print(respond)
            return None
        records = respond.json()
        print(len(records))
        return records

    def check_status(self, procssId):
        mount_point = 'device/action/status/' + procssId
        print(mount_point)
        respond = self.obj.get_request(mount_point)
        print(respond)
        if respond.status_code != 200:
            print(respond)
            return None
        records = respond.json()['data']
        print(len(records))
        return records