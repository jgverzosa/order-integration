import json

from aws_lambda_powertools import Logger
from marshmallow import ValidationError

from mapper.ubereats_to_common_order import CommonOrderMapper
from entities.ubereats_order_notification import OrderNotification
from api.ubereats import UberEatsService

logger = Logger(service="MenuFeed")


class Order:
    def __init__(self, app) -> None:
        self.response = None
        uber_service = UberEatsService()
        order_notification = OrderNotification()
        try:
            payload = order_notification.load(app.current_event.json_body)
            # file = open("./payloads/order-DELIVERY_BY_RESTAURANT-with-google.json", "r")
            # uber_order = json.load(file)
            uber_order = uber_service.get_order(
                payload.get('meta', {}).get('resource_id', None))
            order_mapper = CommonOrderMapper(uber_order)
            order_mapper.common_order_format
            self.response = uber_service.response
            self.response = {"statusCode": 200, "body": json.dumps(order_mapper.common_order_format)}

        except ValidationError as error:
            error_response = error.messages_dict
            logger.error(error_response)
            self.response = {"statusCode": 400, "body": error.messages_dict}
