import json
import requests

from horse import config


def shorten(longurl):
    endpoint = "https://www.googleapis.com/urlshortener/v1/url?key={0}".format(
        config.GAPI_API_TOKEN
    )

    response = requests.post(
        url=endpoint,
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "longUrl": longurl
        })
    )

    return response.json()['id']
