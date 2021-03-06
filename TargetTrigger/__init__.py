import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')

    headers = req.headers
    auth = req.headers['Authorization']

    logging.info(headers)

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"HELLO FROM INNER FUNC, {name}!")
    else:
        return func.HttpResponse(
             "Inner func. triggered automatically, but without param Name!",
             status_code=200
        )
