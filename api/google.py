import os, json, requests

from aws_lambda_powertools import Logger

logger = Logger(service="GoogleMaps")


class GoogleMapsService:
    def __init__(self) -> None:
        self.config = {
            'google_place_url': os.environ.get('GOOGLE_PLACE_API'),
            'access_key': os.environ.get('GOOGLE_PLACE_ACCESS_KEY'),
        }
        self.response = {}

    def get_address(self, place_id):
        query_params = {
            'place_id': place_id,
            'key': self.config['access_key'],
            'fields': 'address_component',
        }
        response = requests.post(
            self.config['google_place_url'],
            params=query_params)
        if response.status_code >= 200 and response.status_code < 300:
            logger.info(response.text)
            json_response = json.loads(response.text)
            return json_response
        else:
            logger.warning(self.response)
            return None
