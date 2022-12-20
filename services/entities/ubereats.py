from dataclasses import field
from email.mime import image
from json import load
from typing import List
from unicodedata import category
from marshmallow import Schema, fields, EXCLUDE, missing, pre_load


class MenuItems(Schema):
    class Meta:
        unknown = EXCLUDE
    item_id = fields.String(load_default=None)
    plu = fields.String()
    description = fields.String(required=True)
    SellShop = fields.String(required=True)
    SellDelivery = fields.String(load_default=None)
    SubCategoryID = fields.String(load_default=None)
    Special = fields.String(load_default=None)
    SellSpecial = fields.String(load_default=None)
    ItemDescription = fields.String(load_default=None)


class Url(Schema):
    class Meta:
        unknown = EXCLUDE
    url = fields.String(load_default="")


class EnName(Schema):
    class Meta:
        unknown = EXCLUDE
    en = fields.String(load_default="", allow_none=True)

class Translations(Schema):
    class Meta:
        unknown = EXCLUDE
    translations = fields.Nested(EnName)

class Overrides(Schema):
    class Meta:
        unknown = EXCLUDE
    context_type = fields.String()
    context_value = fields.String()
    price = fields.Integer()


class PriceInfo(Schema):
    class Meta:
        unknown = EXCLUDE
    price = fields.Integer()
    overrides = fields.Nested(Overrides, many=True, default=tuple())

class ModifiersGroupIds(Schema):
    class Meta:
        unknown = EXCLUDE
    ids = fields.List(fields.String(), load_default=[])

class TimePeriods(Schema):
    class Meta:
        unknown = EXCLUDE
    start_time = fields.String(required=True)
    end_time = fields.String(required=True)

class ServiceAvailability(Schema):
    class Meta:
        unknown = EXCLUDE
    day_of_week = fields.String(required=True)
    time_periods = fields.List(fields.Nested(TimePeriods), many=True)

class Menus(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String()
    title = fields.Nested(Translations)
    subtitle = fields.Nested(Translations)
    service_availability = fields.List(fields.Nested(ServiceAvailability), many=True)
    category_ids =  fields.List(fields.String(), load_default=[])


class EntitiesIds(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String()

class Categories(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String()
    title = fields.Nested(Translations)
    entities = fields.Nested(EntitiesIds, many=True)

class DietaryLabel(Schema):
    class Meta:
        unknown = EXCLUDE
    labels = fields.List(fields.String(), load_default=[])

class DietaryLabelInfo(Schema):
    class Meta:
        unknown = EXCLUDE
    dietary_label_info = fields.Nested(DietaryLabel)
    alcoholic_items = fields.Integer()

class DishInfo(Schema):
    class Meta:
        unknown = EXCLUDE
    classifications = fields.Nested(DietaryLabelInfo)

class LowerHigher(Schema):
    class Meta:
        unknown = EXCLUDE
    lower = fields.Integer()

class EnergyInterval(Schema):
    class Meta:
        unknown = EXCLUDE
    energy_interval = fields.Nested(LowerHigher)

class NutritionalInfo(Schema):
    class Meta:
        unknown = EXCLUDE
    kilojoules = fields.Nested(EnergyInterval)

class Items(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String()
    external_data = fields.String()
    title = fields.Nested(Translations)
    description = fields.Nested(Translations)
    image_url = fields.String()
    price_info = fields.Nested(PriceInfo)
    tax_rate = fields.Integer()
    modifier_group_ids = fields.Nested(ModifiersGroupIds)
    dish_info = fields.Nested(DishInfo)
    nutritional_info = fields.Nested(NutritionalInfo)


class ModifiersOption(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String(required=True)
    type = fields.String()

class Quantity(Schema):
    class Meta:
        unknown = EXCLUDE
    min_permitted = fields.Integer(required=True)
    max_permitted = fields.Integer(required=True)

class QuantityInfo(Schema):
    class Meta:
        unknown = EXCLUDE
    quantity = fields.Nested(Quantity)
    
class Modifiers(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.String()
    title = fields.Nested(Translations)
    modifier_options = fields.Nested(ModifiersOption, many=True)
    quantity_info = fields.Nested(QuantityInfo)
    display_type = fields.String()


class DisplayOptions(Schema):
    class Meta:
        unknown = EXCLUDE
    disable_item_instructions = fields.Boolean(required=True)

class UberEatsMenuSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    menus = fields.Nested(Menus, many=True)
    categories = fields.Nested(Categories, many=True)
    items = fields.Nested(Items, many=True)
    modifier_groups = fields.Nested(Modifiers, many=True)
    display_options = fields.Nested(DisplayOptions)
