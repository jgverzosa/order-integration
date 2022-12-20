import os, json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import ApiGatewayResolver, Response, content_types
from marshmallow import ValidationError

from services.ubereats_mapper import UberEatsMapper
from services.entities.ubereats import UberEatsMenuSchema

logger = Logger(service="MenuFeed")

app = ApiGatewayResolver()


@app.post("/menu")
def menu_upload():
    uber_menu_schema = UberEatsMenuSchema()
    uber_payload = UberEatsMapper(app.current_event.json_body)
    try:
        payload = uber_menu_schema.load(uber_payload.uber_eats_menu_format)
        logger.info(payload)
        return Response(
            status_code=202,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({"message": "Success"})
        ) 
    except ValidationError as error:
        logger.error(uber_payload.uber_eats_menu_format)
        error_response = error.messages_dict
        return Response(
            status_code=400,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(error_response)
        )

# @logger.inject_lambda_context(log_event=True)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)