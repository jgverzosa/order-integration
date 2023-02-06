from marshmallow import Schema, fields, EXCLUDE


class Store(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String(required=True)
    name = fields.String()


class Eater(Schema):
    class Meta:
        unknown = EXCLUDE
    first_name = fields.String()
    last_name = fields.String()
    phone = fields.String()
    phone_code = fields.String()


class PriceSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    amount = fields.Integer(required=True)
    currency_code = fields.String()
    formatted_amount = fields.String()


class Price(Schema):
    class Meta:
        unknown = EXCLUDE
    price = fields.Nested(PriceSchema)
    unit_price = fields.Nested(PriceSchema)
    total_price = fields.Nested(PriceSchema)
    base_unit_price = fields.Nested(PriceSchema)
    base_total_price = fields.Nested(PriceSchema)


class Items(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String(required=True)
    title = fields.String()
    external_data = fields.String()
    quantity = fields.Integer()
    price = fields.Nested(Price)
    # selected_modifier_groups
    instance_id = fields.String()
    eater_id = fields.String()


class Cart(Schema):
    class Meta:
        unknown = EXCLUDE
    items = fields.Nested(Items, many=True)


class Charges(Schema):
    class Meta:
        unknown = EXCLUDE
    total = fields.Nested(PriceSchema)
    sub_total = fields.Nested(PriceSchema)


class Payment(Schema):
    class Meta:
        unknown = EXCLUDE
    charges = fields.Nested(Charges)


class Packaging(Schema):
    class Meta:
        unknown = EXCLUDE


class Eaters(Schema):
    class Meta:
        unknown = EXCLUDE


class Deliveries(Schema):
    class Meta:
        unknown = EXCLUDE


class OrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String(required=True)
    display_id = fields.String()
    current_state = fields.String(required=True)
    store = fields.Nested(Store)
    eater = fields.Nested(Eater)
    cart = fields.Nested(Items)
    payment = fields.Nested(Payment)
    placed_at = fields.DateTime(format="iso")
    estimated_ready_for_pickup_at = fields.DateTime(format="iso")
    type = fields.String(required=True)
    # packaging
    # eaters
    brand = fields.String()
    # deliveries
