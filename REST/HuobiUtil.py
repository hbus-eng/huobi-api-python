# @Author  : Xinzhou Zhao
# @github  : https://github.com/xinzhou5

import base64
import hmac
import hashlib
import json
import urllib
import datetime
import requests

from urllib.parse import urlparse, urlencode

# Use your own APIKEY
ACCESS_KEY = "YOUR_ACCESS_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"

# timeout in 5 seconds:
TIMEOUT = 5

# API request utl
MARKET_URL = TRADE_URL = "https://api.huobi.com"

def publicReq(url, method, data=None, params=None, headers=None):
    if method not in ['GET', 'POST']:
        raise Exception('method can only be GET or POST')

    # default values
    if data is None:
        data = {}
    if params is None:
        params = {}
    if headers is None:
        headers = {}

    # need to parse them to string before calling
    params = urlencode(params)
    data = json.dumps(data)

    response = ""

    if method == 'POST':
        headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        })
        try:
            res = requests.post(url, params=params, data=data, headers=headers, timeout=TIMEOUT)
            response = res.text
        except Exception as e:
            print("httpPost failed, detail is: ", e)
            return json.dumps({"status":"fail","msg":e})
    elif method == 'GET':
        headers.update({
            "Content-type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        })
        try:
            res = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
            response = res.text
        except Exception as e:
            print("httpGet failed, detail is:", e)
            return json.dumps({"status":"fail","msg":e})

    return response

def privateReq(url, method, data=None, params=None, ACCESS_KEY=ACCESS_KEY, SECRET_KEY=SECRET_KEY):
    if method not in ['GET', 'POST']:
        raise Exception('method can only be GET or POST')

    if not ACCESS_KEY or not SECRET_KEY:
        raise Exception('ACCESS_KEY and SECRET_KEY must not be empty')

    # default values
    if data is None:
        data = {}
    if params is None:
        params = {}

    createSig(params, method, url, ACCESS_KEY, SECRET_KEY)
    return publicReq(url, method, data, params)

def createSig(params, method, url, ACCESS_KEY=ACCESS_KEY, SECRET_KEY=SECRET_KEY):
    # Add mandatory authentication parameters to the query string
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp})

    # Sort all the parameters by name in ascend order
    sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)

    # put them into a url encoded string
    encode_params = urlencode(sorted_params)

    # struct the signature payload
    parsedURL = urlparse(url)
    payload = [method, parsedURL.hostname, parsedURL.path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    sec = SECRET_KEY.encode(encoding='UTF8')

    # Calculate the Signature and add it to the query
    digest = hmac.new(sec, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    params['Signature'] = signature

    return
