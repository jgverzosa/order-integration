import uuid
from aws_lambda_powertools import Logger

from api.google import GoogleMapsService

logger = Logger(service="OrderFeed")


class CommonOrderMapper:

    def __init__(self, common_json) -> None:
        self.ubereats_order_json = common_json
        self.common_order_format = {
            "partner": "ubereats",
            "id": "",
            "externalOrderRef": "",
            "deliveryOrderId": "",
            "locationId": "",
            "status": "",
            "type": "",
            "notes": "",
            "requiredAt": "",
            "availableEta": "",
            "items": [],
            "consumer": {},
            "surcounts": [],
            "taxes": [],
            "delivery": {},
            "transactions": [],
            "posCreatedAt": "",
            "updatedAt": "",
            "createdAt": "",
        }

        self.UBER_ORDER_STATUS = {
            'CREATED': 'created',
            'DENIED': 'rejected',
            'ACCEPTED': 'accepted',
            'FINISHED': 'complete',
            'CANCELED': 'cancelled',
            'UNKNOWN': 'unknown',
        }
        self.UBER_ORDER_TYPES = {
            'PICK_UP': 'pick_up',
            'DINE_IN': 'dine_in',
            'DELIVERY_BY_UBER': 'pick_up',
            'DELIVERY_BY_RESTAURANT': 'delivery',
            }
        self.transform()

    def transform(self):
        self.common_order_format['id'] = uuid.uuid4()
        self.common_order_format['externalOrderRef'] \
            = self.ubereats_order_json.get('id')
        self.common_order_format['deliveryOrderId'] \
            = self.ubereats_order_json.get('display_id')
        self.common_order_format['locationId'] \
            = self.ubereats_order_json.get('store', {}).get('id', None)
        self.common_order_format['status'] \
            = self.UBER_ORDER_STATUS.get(
            self.ubereats_order_json.get('current_state'))
        self.common_order_format['type'] \
            = self.UBER_ORDER_TYPES.get(self.ubereats_order_json.get('type'))
        # self.common_order_format['notes'] = self.ubereats_order_json.get('')
        self.common_order_format['requiredAt'] \
            = self.ubereats_order_json.get('placed_at')
        self.common_order_format['availableEta'] \
            = self.ubereats_order_json.get('estimated_ready_for_pickup_at')
        self.set_items()
        self.set_consumer()
        self.set_surcounts()
        # self.set_taxes()
        self.set_delivery()
        self.set_transactions()
        # self.common_order_format['posCreatedAt'] = self.ubereats_order_json.get('')
        # self.common_order_format['updatedAt'] = self.ubereats_order_json.get('')
        self.common_order_format['createdAt'] = self.ubereats_order_json.get('placed_at')

    def set_items(self):
        items = self.ubereats_order_json.get('cart', {}).get('items', [])
        for item in items:
            unit_item = {
                "posId": item.get('id'),
                "name": item.get('title'),
                "quantity": item.get('quantity'),
                "unitPrice": item.get('price', {})
                .get('unit_price', {}).get('amount', None),
                "includedItems": [],
            }
            self.map_include_item(
                item.get('selected_modifier_groups', []) or [], 
                unit_item)
            self.common_order_format['items'].append(unit_item)

    def set_consumer(self):
        eater = self.ubereats_order_json.get('eater', {})
        full_name = eater.get('first_name')
        if "last_name" in eater.get('last_name'):
            full_name += " " + eater.get('last_name')
        consumer = {
            "name": full_name,
            "email": "",
            "phone": eater.get('phone', ""),
        }
        if eater.get('delivery', {}).get('location', {}) \
                .get('google_place_id', None):
            consumer["address"] = self.get_address()
        self.common_order_format['consumer'] = consumer

    def set_surcounts(self):
        # Promotions
        promotions = self.ubereats_order_json.get('payment', {}) \
            .get('promotions', {}).get('promotions', {})
        if promotions:
            for promotion in promotions:
                self.common_order_format['surcounts'].append({
                    "posId": promotion.get('external_promotion_id', ""),
                    "name": promotion.get('promo_type', ""),
                    "description": "",
                    "amount": promotion.get('promo_discount_value', ""),
                    "type": "absolute",
                    "value": promotion.get('promo_discount_value', ""),
                })
        # Delivery Fee
        delivery_fee = self.ubereats_order_json.get('payment', {}) \
            .get('charges', {}).get('delivery_fee', {})
        if delivery_fee:
            self.common_order_format['surcounts'].append({
                "posId": "DELIVERY_FEE",
                "name": "Delivery Fee",
                "description": "",
                "amount": delivery_fee.get('amount', ""),
                "type": "absolute",
                "value": delivery_fee.get('amount', ""),
            })

    def set_taxes(self):
        pass

    def set_delivery(self):
        pass

    def set_transactions(self):
        charges = self.ubereats_order_json.get('payment', {}) \
            .get('charges', {})
        tip = charges.get('tip', {})
        total = charges.get('total', {})
        self.common_order_format['transactions'] = {
            "orderId": self.ubereats_order_json.get('display_id'),
            "reference": self.ubereats_order_json.get('id'),
            "amount": total.get('amount', 0),
            "tip": tip.get('amount', 0),
            "currencyCode": total.get('currency_code', ''),
            "acceptLess": False,
        }

    def map_include_item(self, selected_modifiers, parent_item):
        def map_selected_items(selected_modifiers, parent_item):
            for modifier in selected_modifiers:
                unit_price = modifier.get('price', {})\
                    .get('unit_price', {}).get('amount', None)
                included_item = {
                    "name": modifier.get('title'),
                    "posId": modifier.get('id'),
                    "quantity": modifier.get('quantity'),
                    "unitPrice": unit_price,
                    "options": [],
                }
                self.map_options(modifier.get('selected_modifier_groups', []) or [], included_item)
                parent_item['includedItems'].append(included_item)
        for modifier in selected_modifiers:
            if "include:" in modifier['id']:
                map_selected_items(modifier.get('selected_items', []) or [], parent_item)

    def map_options(self, options, parent_item):
        for option in options:
            pos_id = option.get('id', '').replace('option:', '')
            option_details = {
                "posId": pos_id,
                "name": option.get('title'),
                "variants": [
                    {
                        "posId": selected_item['id'],
                        "name": selected_item['title'],
                        "price": selected_item.get('price', {}).get('unit_price', {}).get('amount')
                    }
                    for selected_item in option.get('selected_items', [])
                ],
            }
            parent_item.setdefault('options', []).append(option_details)

    def get_address(self):
        place_id = self.ubereats_order_json.get('eater', {}).get('delivery', {})\
            .get('location', {}).get('google_place_id', None)
        google_place = GoogleMapsService()
        google_address_components = google_place.get_address(place_id)
        if google_address_components.get('result'):
            address = {}
            for component in google_address_components.get('result', {}).get('address_components', []):
                if 'street_number' in component['types']:
                    address['line1'] = component.get('short_name', "")
                elif 'route' in component['types']:
                    address['line1'] += " " + component.get('short_name', "")
                elif 'locality' in component['types']:
                    address['city'] = component.get('long_name', "")
                elif 'administrative_area_level_1' in component['types']:
                    address['state'] = component.get('short_name', "")
                elif 'postal_code' in component['types']:
                    address['postalCode'] = component.get('short_name', "")
                elif 'country' in component['types']:
                    address['country'] = component.get('short_name', "")
            address['line2'] = self.ubereats_order_json.get('eater', {}) \
                .get('delivery', {}).get('location', {}).get('unit_number', "")
            address['notes'] = self.ubereats_order_json.get('eater', {}) \
                .get('delivery', {}).get('location', {}).get('notes', "")
            return address
