import os, json, requests

from aws_lambda_powertools import Logger

logger = Logger(service="MenuFeed")


class UberEatsService:
    def __init__(self) -> None:
        self.config = {
            'ubereats_url': os.environ.get('UBEREATS_API'),
            'access_key': os.environ.get('UBEREATS_ACCESS_KEY'),
            'secret_key': os.environ.get('UBEREATS_SECRET_KEY'),
        }
        self.response = {}

    def generate_uber_eats_token(self, access_key, secret_key):

        #add redis call uber_key_cache (string)

        login_url = os.environ.get('UBEREATS_LOGIN_API')
        data = {
            'client_id': access_key,
            'client_secret': secret_key,
            'grant_type': 'client_credentials',
            'scope': 'eats.store eats.order'
        }
        response = requests.post(login_url, data=data)
        if response.status_code >= 200 and response.status_code < 300:
            logger.info(response.text)
            json_response = json.loads(response.text)
            return json_response            
        else:
            logger.warning(self.response)
            return None

    def send_menu_to_uber(self, store_id, body):
        menu_endpoint = f"{self.config.get('ubereats_url')}/stores/{store_id}/menus"
        token = self.generate_uber_eats_token(
                self.config.get('access_key'), 
                self.config.get('secret_key'))
        self.headersAuth = {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'Authorization': f"Bearer {token.get('access_token')}",
        }
        response = requests.request("PUT", menu_endpoint, headers=self.headersAuth, data=body)
        if response.status_code == 204:
            logger.info(self.response)
            self.response['statusCode'] = response.status_code
            self.response['body'] = json.dumps({"message": "success"})
            return True
        else:
            self.response['statusCode'] = response.status_code
            self.response['body'] = response.text
            logger.warning(self.response)
            return False

    def get_order(self, order_id):
        endpoint = f"{self.config.get('ubereats_url')}/order/{order_id}"
        token = self.generate_uber_eats_token(
                self.config.get('access_key'), 
                self.config.get('secret_key'))
        self.headersAuth = {
            'Content-type': 'application/json', 'Accept': 'text/plain',
            'Authorization': f"Bearer {token.get('access_token')}",
        }
        response = requests.request("GET", endpoint, headers=self.headersAuth)
        if 200 <= response.status_code < 300:
            logger.info(self.response)
            return response.json()
        else:
            logger.warning(self.response)
            return False

