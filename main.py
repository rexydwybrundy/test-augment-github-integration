import requests
import os
import re
import datetime
import json
import time
 
def checkLogin(event, context):
    namespace = os.environ['NAMESPACE']
    user_id = os.environ['USER_ID']
     
    if not len(event):
        sendSlack("event is empty")
        return None
 
    if not len(event['data']):
        sendSlack("event data is empty")
        return None
 
    user_data = event['data']
 
    if not len(user_data):
        sendSlack("user data is empty")
        return None
 
    if not len(user_data['userId']):
        sendSlack("user id is mepty")
        return None
 
    if user_data['userId'] != user_id:
        return None
 
    access_token = getToken()
 
    today = datetime.datetime.utcnow()
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
 
    time.sleep(3)
     
    url='https://dev.accelbyte.io/event/v2/admin/namespaces/'+namespace+'/users/'+user_id+'/event?startDate='+today.strftime("%Y")+'-'+today.strftime("%m")+'-'+today.strftime("%d")+'T00%3A00%3A00Z&endDate='+today.strftime("%Y")+'-'+today.strftime("%m")+'-'+tomorrow.strftime("%d")+'T00%3A00%3A00Z&eventName=userLoggedIn'
    headers = {'Authorization' : 'Bearer ' + access_token}
    response = requests.get(url, headers=headers, allow_redirects=False)
 
    item = json.loads(response.content)
     
    url='https://dev.accelbyte.io/platform/admin/namespaces/'+namespace+'/wallets?userId='+user_id+'&offset=0&limit=20'
    headers = {'Authorization' : 'Bearer ' + access_token}
    response = requests.get(url, headers=headers, allow_redirects=False)
 
    item = json.loads(response.content)
     
    if len(item['data']) < 1:
        return None
 
    for x in item['data']:
        if x['currencyCode'] == 'JC':
             
            url='https://dev.accelbyte.io/platform/admin/namespaces/'+namespace+'/users/'+user_id+'/wallets/JC/credit'
            headers = {'Authorization' : 'Bearer ' + access_token, 'content-type':'application/json'}
            data = '''{"amount": 111, "source": "ACHIEVEMENT", "reason": "gift"}'''
            response = requests.put(url, headers=headers, data=data, allow_redirects=False)
 
            sendSlack(event)
             
            break
 
def getToken():
    clientIdAdminPortal='ca49c11efbd04a67afb5bd1c81dc17eb'
 
    url = 'https://dev.accelbyte.io/iam/v3/oauth/authorize?response_type=code&amp;client_id='+clientIdAdminPortal+'&state=99ffaa68e9634b4c9f0529505bab868a&scope=commerce%20account%20social%20publishing%20analytics&code_challenge=99ffaa68e9634b4c9f0529505bab868a99ffaa68e9634b4c9f0529505bab868a&code_challenge_method=plain'
    response = requests.get(url, allow_redirects=False)
    location = response.headers['Location']
    request_id = re.compile('request_id=(.*)').search(location).group(1)
 
    url = 'https://dev.accelbyte.io/iam/v3/authenticate'
    data = {'user_name' : 'adminportal@accelbyte.io', 'password' : 'Eiv2equozai5yiHoy2aipheev6aebe', 'request_id' : request_id}
    response = requests.post(url, data, allow_redirects=False)
    location = response.headers['Location']
    code = re.compile('code=(.*)&state').search(location).group(1)
 
    url = 'https://dev.accelbyte.io/iam/v3/oauth/token'
    data = {'grant_type' : 'authorization_code', 'code' : code, 'code_verifier' : '99ffaa68e9634b4c9f0529505bab868a99ffaa68e9634b4c9f0529505bab868a', 'client_id' : clientIdAdminPortal }
    response = requests.post(url, data, allow_redirects=False)
    access_token = response.json()['access_token']
 
    return access_token
 
def sendSlack(param):
    url='https://hooks.slack.com/services/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'
    headers = {'content-type':'application/json'}
    data = '''{"text" : "'''+str(param)+'''"}'''
    response = requests.post(url, data=data, headers=headers, allow_redirects=False)
