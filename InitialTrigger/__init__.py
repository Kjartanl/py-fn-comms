
import logging
from urllib import request

import azure.functions as func

import requests
import msal
import TargetTrigger

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        url = f"http://localhost:7071/api/TargetTrigger?name={name}"
        
        config = load_config()

        app = msal.ConfidentialClientApplication(
                config["client_id"], 
                authority=config["authority"],
                client_credential=config["secret"])

        result = app.acquire_token_for_client(scopes=config["scope"])

        graph_data = requests.get(  
                        config["endpoint"],
                        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()

        myPostResponse = requests.post(url, headers={'Authorization': result['access_token']})

        response = func.HttpResponse(f"Hello, {name}.\rPost response: {str(myPostResponse.text)}")

        return response
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200)

def load_config():
    return {
        "authority": "https://login.microsoftonline.com/01a2e6e1-38a9-49ec-bdd5-c2e1016a76c8", 
        "client_id": "1e36af8e-1a74-4581-9d5d-862ca9b17c45", 
        "scope": [ "https://graph.microsoft.com/.default" ], 
        "secret": "QcAOr9/1shIaNT3m75SxiMseH94KnjYFIAvxXNOPvNM=", 
        "endpoint": "https://graph.microsoft.com/v1.0/users"
        }