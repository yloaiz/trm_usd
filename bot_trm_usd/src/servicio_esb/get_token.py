import requests
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("MAAJI_USERNAME")
password = os.getenv("MAAJI_PASSWORD")
url_token_api = os.getenv("URL_TOKEN_API")

def get_token():
    url = url_token_api
    payload = {
        "username":username,
        "password":password
    }
 
    response = requests.request("POST", url, data=payload)
 
    token = response.json()['access']
 
    return token
