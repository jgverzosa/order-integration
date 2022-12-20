import json
from services.entities.ubereats import UberEatsMenuSchema


class UberEatsMapper:

    def __init__(self, commonJson) -> None:
        self.commonJson = commonJson
        self.uber_eats_menu_schema = UberEatsMenuSchema()
        self.uber_eats_menu_format = {
            'menus': [],
            'categories': [],
            'items': [],
            'modifier_groups': [],
            'display_options': {}
        }
        self.transform()

    def transform(self):
        self.uber_eats_menu_format['menus'].append(self.get_menu_details())
        self.uber_eats_menu_format['categories'] = self.get_categories()
        self.map_items()
        pass

    def map_items(self):
        products = self.commonJson.get('products')
        for index, product in enumerate(products):
            item = self.get_item(product)
            # Options group
            if product.get('options'):
                modifier_ids = self.map_option_items(product)
                item['modifier_group_ids']['ids'] = modifier_ids
            # Bundled group
            if product.get('bundledItems'):
                self.map_bundled_items(product)
            # Included group
            if product.get('includedItems'):
                self.map_included_items(product, product)
            self.add_item(item)

    def map_bundled_items(self, parent_item):
        bundled_products = parent_item.get('bundledItems')
        for product in bundled_products:
            self.map_included_items(parent_item, product)

    def map_included_items(self, parent_item, product):
        if product.get('includedItems'):
            modifier_ids = []
            for included_items in product.get('includedItems'):
                item = self.get_item(included_items)
                item['price_info']['price'] = int(included_items['unitPrice'])
                if included_items.get('options'):
                    option_modifiers = self.map_option_items(included_items)
                    item['modifier_group_ids']['ids'] = option_modifiers
                self.add_item(item)
                modifier_ids.append(item.get('id'))
            modifier = self.get_modifier(product)
            modifier['modifier_options'] = self.get_modifier_options(modifier_ids)
            self.add_modifier(modifier)
            # Append the modifier_group_ids of the part item
            parent = next((item for item in self.uber_eats_menu_format['items'] if item['id'] == parent_item.get('posId')), None)
            if parent:
                parent['modifier_group_ids']['ids'].append(product.get('posId'))

    def map_option_items(self, product):
        if product.get('options'):
            modifier_ids = []
            for option in product.get('options'):
                variant_ids = self.map_option_variants(option)
                modifier = self.get_modifier(option)
                modifier['modifier_options'] = self.get_modifier_options(variant_ids)
                self.add_modifier(modifier)
                modifier_ids.append(option['posId'])
            return modifier_ids

    def map_option_variants(self, option):
        variant_ids = []
        for variant in option.get('variants'):
            item = self.get_item(variant)
            item['price_info']['price'] = variant['price']
            self.add_item(item, option)
            variant_ids.append(variant['posId'])
        return variant_ids

    def get_categories(self):
        categories = self.commonJson.get('categories') if self.commonJson.get('categories') else []
        uber_eats_categories = []

        def get_entities(entities):
            uber_eats_entities = []
            for entity in entities:
                uber_eats_entities.append({'id': str(entity)})
            return uber_eats_entities

        for category in categories:
            uber_eats_category = {
                'id': str(category.get('displayOrder')),
                'title': self.get_translations(category.get('category')),
                'entities': get_entities(category.get('productIds'))
            }
            uber_eats_categories.append(uber_eats_category)
        return uber_eats_categories

    def get_menu_details(self):
        menu = self.commonJson
        menus = {
            'id': menu['locationId'],
            'title': self.get_translations(menu['description']),
            'subtitle': self.get_translations(menu['description']),
            'service_availability': [
                {
                    'day_of_week': 'monday',
                    'time_periods': [
                        {
                            'start_time': '01:00',
                            'end_time': '23:15'
                        }
                    ]
                },
                {
                    'day_of_week': 'tuesday',
                    'time_periods': [
                        {
                            'start_time': '00:00',
                            'end_time': '23:45'
                        }
                    ]
                },
                {
                    'day_of_week': 'wednesday',
                    'time_periods': [
                        {
                            'start_time': '10:45',
                            'end_time': '19:45'
                        }
                    ]
                },
                {
                    'day_of_week': 'thursday',
                    'time_periods': [
                        {
                            'start_time': '10:45',
                            'end_time': '19:45'
                        }
                    ]
                },
                {
                    'day_of_week': 'friday',
                    'time_periods': [
                        {
                            'start_time': '17:00',
                            'end_time': '00:00'
                        }
                    ]
                },
                {
                    'day_of_week': 'saturday',
                    'time_periods': [
                        {
                            'start_time': '17:00',
                            'end_time': '00:00'
                        }
                    ]
                }
            ],
            'category_ids': self.get_category_ids()
        }
        return menus

    def get_category_ids(self):
        categories = self.commonJson.get('categories') if self.commonJson.get('categories') else []
        categories_ids = [str(k['displayOrder']) for k in categories]
        categories_ids.sort()
        return categories_ids

    def get_item(self, product):
        item = {
            'id': str(product.get('posId')),
            'external_data': str(product.get('posId')),
            'title': self.get_translations(product.get('name')),
            'description': self.get_translations(product.get('description')),
            'image_url': product.get('imageUri'),
            'price_info': {
                'price': product.get('unitPrice'),
                'overrides': []
            },
            'tax_info': {},
            'nutritional_info': {},
            'dish_info': {
                'classifications': {
                    'alcoholic_items': 0,
                    'dietary_label_info': {
                        'labels': product.get('dietary')
                    },
                    'ingredients': None,
                    'additives': None
                }
            },
            'modifier_group_ids': {
                'ids': [],
                'overrides': []
            },
            'product_info': {
                'product_traits': None,
                'countries_of_origin': None
            },
             'bundled_items': None
        }
        return item     

    def get_modifier(self, product):
        modifier = {
            'id': str(product.get('posId')),
            'title': self.get_translations(product.get('name')),
            'quantity_info': {
                'quantity': {
                    'min_permitted': product.get('min'),
                    'max_permitted': product.get('max')
                },
                'overrides': []
            },
            'modifier_options': [],
            'display_type': 'collapsed'
        }
        return modifier

    def add_item(self, item, overrides_item=None):
        exist_item = next((map_item for map_item in self.uber_eats_menu_format['items'] if map_item['id'] == item['id']), None)  
        if exist_item is None:
            self.uber_eats_menu_format['items'].append(item)
        elif overrides_item is not None and exist_item['price_info']['price'] != item['price_info']['price'] \
                and overrides_item['posId'] not in [exist_overrides_ids['context_value'] for exist_overrides_ids in exist_item['price_info']['overrides']]:
            overrides = {
                "context_value": str(overrides_item.get('posId')),
                "price": item['price_info']['price'],
                "context_type": "MODIFIER_GROUP"
            }            
            exist_item['price_info']['overrides'].append(overrides)

    def add_modifier(self, item):
        exist_item = next((map_item for map_item in self.uber_eats_menu_format['modifier_groups'] if map_item['id'] == item['id']), None)  
        if exist_item is None:
            self.uber_eats_menu_format['modifier_groups'].append(item)

    def get_modifier_options(self, modifier_ids):
        uber_eats_modifier_ids = []
        for modifier_id in modifier_ids:
            uber_eats_modifier_ids.append({'id': modifier_id, 'type': 'ITEM'})
        return uber_eats_modifier_ids

    def get_translations(self, word):
        return {'translations': {'en': word if word else ""}}