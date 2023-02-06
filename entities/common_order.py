from marshmallow import Schema, fields, EXCLUDE


class Address(Schema):
    class Meta:
        unknown = EXCLUDE
    line1 = fields.String()
    line2 = fields.String()
    city = fields.String()
    state = fields.String()
    postalCode = fields.String()
    country = fields.String()  


class Consumer(Schema):
    class Meta:
        unknown = EXCLUDE
    name = fields.String()
    email = fields.Email()
    phone = fields.String()
    address = fields.Nested(Address)


class SurCount(Schema):
    class Meta:
        unknown = EXCLUDE
    posId = fields.String(required=True)
    name = fields.String()
    description = fields.String()
    amount = fields.Integer()
    type = fields.String()
    value = fields.String()


class Tax(Schema):
    class Meta:
        unknown = EXCLUDE
    posId = fields.String(required=True)
    name = fields.String()
    amount = fields.Number()
    type = fields.String()
    taxType = fields.String()
    value = fields.Number()


class Transaction(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String(required=True)
    orderId = fields.String()
    reference = fields.String()
    surcount = fields.Nested(SurCount, many=True)
    updatedAt = fields.DateTime(format="iso")
    createdAt = fields.DateTime(format="iso")
    uri = fields.String()
    status = fields.String()
    linkedTrxId = fields.String()
    posTerminalId = fields.String()


class Delivery(Schema):
    class Meta:
        unknown = EXCLUDE
    status = fields.String()
    displayId = fields.String()
    phase = fields.String()
    failedReason = fields.String()
    deliveryEta = fields.DateTime(format="iso")
    driverName = fields.String()
    driverPhone = fields.String()
    trackingUrl = fields.String()


class Variant(Schema):
    class Meta:
        unknown = EXCLUDE
    posId = fields.String()
    name = fields.String()
    price = fields.Integer()

class Option(Schema):
    class Meta:
        unknown = EXCLUDE
    posId = fields.String()
    name = fields.String()
    variants = fields.Nested(Variant, many=True)


class CommonItemFields(Schema):
    class Meta:
        unknown = EXCLUDE
    name = fields.String()
    posId = fields.String()
    quantity = fields.Integer()
    unitPrice = fields.Integer()
    options = fields.Nested(Option, many=True)


class Item(CommonItemFields):
    uuid = fields.String()
    description = fields.String()
    tags = fields.List(fields.String())
    type = fields.String()
    includedItems = fields.Nested(CommonItemFields, many=True)
    options = fields.Nested(Option, many=True)


class CommonOrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String(required=True)
    externalOrderRef = fields.String(required=True)
    deliveryOrderId = fields.String()
    locationId = fields.String(required=True)
    status = fields.String()
    type = fields.String()
    notes = fields.String()
    requiredAt = fields.DateTime(format="iso")
    availableEta = fields.DateTime(format="iso")
    items = fields.Nested(Item, many=True)
    consumer = fields.Nested(Consumer)
    surcounts = fields.Nested(SurCount, many=True)
    taxes = fields.Nested(Tax, many=True)
    delivery = fields.Nested(Delivery)
    transactions = fields.Nested(Transaction, many=True)
    posCreatedAt = fields.DateTime(format="iso")
    updatedAt = fields.DateTime(format="iso")
    createdAt = fields.DateTime(format="iso")
    version = fields.String()
    uri = fields.String()
