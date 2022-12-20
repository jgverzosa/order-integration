from marshmallow import Schema, fields, EXCLUDE, ValidationError


class Variants(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String()
    posId = fields.String()
    price = fields.Integer()


class Options(Schema):
    class Meta:
        unknown = EXCLUDE

    max = fields.Integer()
    min = fields.Integer()
    name = fields.String()
    posId = fields.String()
    variants = fields.Nested(Variants, many=True)


class IncludedItems(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String()
    options = fields.Nested(Options, many=True)
    posId = fields.String()
    unitPrice = fields.Integer()
    productIds = fields.Dict(fields.String(), load_default=[])
    quantity = fields.Integer()


class BundledItems(Schema):
    class Meta:
        unknown = EXCLUDE

    includedItems = fields.Nested(IncludedItems, many=True)
    max = fields.Integer()
    min = fields.Integer()
    name = fields.String()
    posId = fields.String(required=True)
    productIds = fields.Dict(fields.String(), load_default=[])


class Categories(Schema):
    class Meta:
        unknown = EXCLUDE

    category = fields.String()
    description = fields.String()
    displayOrder = fields.Integer()
    productIds = fields.List(fields.String(), load_default=[])


class Products(Schema):
    class Meta:
        unknown = EXCLUDE

    availability = fields.String()
    bundledItems = fields.Nested(BundledItems, many=True)
    customPosId = fields.String()
    description = fields.String()
    dietary = fields.List(fields.String(), load_default=[])
    imageUri = fields.String()
    includedItems = fields.Nested(IncludedItems, many=True)
    menuDir = fields.List(fields.String(), load_default=[])
    name = fields.String()
    options = fields.Nested(Options, many=True)
    posId = fields.String()
    tags = fields.List(fields.String())
    type = fields.String()
    unitPrice = fields.Integer()


class MenuSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    categories = fields.Nested(Categories, many=True)
    description = fields.String()
    products = fields.Nested(Products, many=True)
    locationId = fields.Integer(required=True)
    createdDate = fields.DateTime()