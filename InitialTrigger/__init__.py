
import logging
from urllib import request


import azure.functions as func

import requests
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
        myPostResponse = requests.post(url)

        response = func.HttpResponse(f"Hello, {name}.\rPost response: {str(myPostResponse.text)}")

        return response
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
