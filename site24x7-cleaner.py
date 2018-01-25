#!/usr/bin/python
import json
import requests

print('Please get your token by visiting this link in a browser :\n')
print('https://accounts.zoho.com/apiauthtoken/create?SCOPE=Site24x7/site24x7api')

token = raw_input('Enter you token: \n')

auth_token = 'Zoho-authtoken ' + token
headers = {'Authorization': auth_token}
api = 'https://www.site24x7.com/api/'
status_url = api + 'current_status'

r = requests.get(status_url, headers = headers)
result = json.loads(r.text)
monitors = result['data']['monitors']
monitor_groups = result['data']['monitor_groups']

nb_downs = 0
to_delete = []

for monitor in monitors:
    if monitor[u'status'] == 0:
        nb_downs += 1
        to_delete.append(monitor[u'monitor_id'])

for group in monitor_groups:
    for monitor in group[u'monitors']:
        if monitor[u'status'] == 0:
            nb_downs += 1
            to_delete.append(monitor[u'monitor_id'])

joined_ids = ','.join(to_delete)
delete_url = api + 'monitors?monitor_ids=' + joined_ids

print('\n' + str(len(to_delete)) + ' monitors to delete : ' + joined_ids)

confirm = raw_input('\nAre you sure you want to delete all the down monitors? (yes to continue)\n')
if confirm == 'yes':
    r = requests.delete(delete_url, headers = headers)
    print(str(len(to_delete)) + ' monitors deleted')
else:
    print('Deletion Cancelled')
