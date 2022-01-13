from flask import Flask
from google.auth import crypt
from google.auth import jwt
import time
import os
import io
import json
import base64
import requests


# https://cloud.google.com/run/docs/securing/service-identity#access_tokens
def generateAccessToken():
    # Request Headers
    headers = {
        'Metadata-Flavor': 'Google'
    }

    url = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token?scopes=https://www.googleapis.com/auth/logging.write'

    # Get response data
    response = requests.get(url, headers=headers)
    print(response.text)
    return response.text

app = Flask(__name__)
@app.route('/hello', methods=['GET', 'POST'])
def welcome():
    return "Hello World!\n"

@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'Welcome to My Watchlist11111!\n'

@app.route('/api', methods=['GET'])
def api():
    # return generate_jwt(sa_keyfile, sa_email, audience)
    return generateAccessToken()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)



