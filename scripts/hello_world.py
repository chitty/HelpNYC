import base64
import datetime
import hashlib
import os
import requests
import sha
import uuid

API_KEY = os.environ.get('VM_API_KEY')
USERNAME = os.environ.get('VM_USERNAME')

if not API_KEY:
    API_KEY = 'MyS3cr3TAP1K3Y'
    print('WARNING: VM_API_KEY not set in the environment, using default.')
if not USERNAME:
    USERNAME = 'myusername'
    print('WARNING: VM_USERNAME not set in the environment, using default.')

nonce = base64.b64encode(sha.new(uuid.uuid4().hex).digest())
created = '{:%Y-%m-%dT%H:%M:%SZ}'.format(datetime.datetime.now())
PasswordDigest = base64.b64encode(hashlib.sha256(nonce+created+API_KEY).digest())

x_wsse = 'UsernameToken Username="'+USERNAME+'", PasswordDigest="'+PasswordDigest+'", Nonce="'+nonce+'", Created="'+created+'"'
headers = {'Content-Type': 'application/json', 'Authorization': 'WSSE profile="UsernameToken"', 'X-WSSE': x_wsse}
payload = {'action': 'helloWorld', 'query': '{"name": "john"}'}

r = requests.get('http://www.volunteermatch.org/api/call', params=payload, headers=headers)

print(r)
