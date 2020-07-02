# Copyright: Ngena USA LLC.,
# Author: Jingyuan He (Mark)
# Date : July 1st 2020
import time
from updatePolicy import updatePolicy  as updatePolicy
vmanage_ip = ''
username = ''
password = ''

client = updatePolicy(vmanage_ip, username, password)


policy = client.find_policy_byName('API_test_policy')

rspd_deact = client.deactive_policy(policy)
id = rspd_deact['id']
i = 0
while i < 10:
    resp = client.check_status(id)
    if len(resp) == 0:
        print(resp)
        time.sleep(2)
        i += 1
        continue
    print(resp[0]['status'])
    if 'Success' == resp[0]['status']:
        break
    i += 1
    time.sleep(10)

time.sleep(30)
# we need some interval between 2 api request or we will get 409 - conflict
rspd_put = client.put_update(policy)
time.sleep(10)
rspd_update = client.commit_modify(policy)
print(rspd_update)
id = rspd_update['id']
print(id)
i = 0
while i < 10:
    resp = client.check_status(id)
    if len(resp) == 0:
        print(resp)
        time.sleep(2)
        i += 1
        continue
    print(resp[0]['status'])
    if 'Success' == resp[0]['status']:
        break
    i += 1
    time.sleep(10)

print(rspd_update)
