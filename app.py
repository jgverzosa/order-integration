import json

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import ApiGatewayResolver, Response, content_types
from marshmallow import ValidationError

from events.ubereats.menu_upload import Menu as UberEatsMenu
from entities.common_menu import CommonMenuSchema
from events.ubereats.order import Order

logger = Logger(service="MenuFeed")
app = ApiGatewayResolver()


@app.post("/menu")
def menu_upload():
    app.current_event.json_body
    common_menu = CommonMenuSchema()
    try:
        common_menu.load(app.current_event.json_body)
        uber_eats = UberEatsMenu(app)
        return Response(
                    status_code=uber_eats.response.get("statusCode"),
                    content_type=content_types.APPLICATION_JSON,
                    body=json.dumps(uber_eats.response.get("body"))
                )
    except ValidationError as error:
        return Response(
                    status_code=400,
                    content_type=content_types.APPLICATION_JSON,
                    body=error.messages_dict
                )


@app.post("/ubereats/order")
def order():
    app.current_event.json_body
    Order(app)
    # try:
    #     common_menu.load(app.current_event.json_body)
    #     uber_eats = UberEatsMenu(app)
    return Response(
                status_code=200,
                content_type=content_types.APPLICATION_JSON,
                body=json.dumps({"message": "success"})
            )
    # except ValidationError as error:
    #     return Response(
    #                 status_code=400,
    #                 content_type=content_types.APPLICATION_JSON,
    #                 body=error.messages_dict
    #             )


# @logger.inject_lambda_context(log_event=True)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
