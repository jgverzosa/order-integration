import json
from aws_lambda_powertools import Logger
from marshmallow import ValidationError

from mapper.ubereats import UberEatsMapper
from entities.ubereats_menu import UberEatsMenuSchema
from api.ubereats import UberEatsService

logger = Logger(service="MenuFeed")


class Menu:
    def __init__(self, app) -> None:
        self.response = None
        uber_service = UberEatsService()
        uber_menu_schema = UberEatsMenuSchema()
        uber_payload = UberEatsMapper(app.current_event.json_body)
        # s3
        logger.info(json.dumps(uber_payload.uber_eats_menu_format, indent=4))
        try:
            payload = uber_menu_schema.load(uber_payload.uber_eats_menu_format)
            uber_menu = uber_service.send_menu_to_uber(
                store_id=uber_payload.config.get('store_id'),
                body=json.dumps(payload)
            )
            if not uber_menu:
                self.response = uber_service.response
            self.response = uber_service.response
        except ValidationError as error:
            error_response = error.messages_dict
            logger.error(error_response)
            self.response = {"statusCode": 400, "body": error.messages_dict}
