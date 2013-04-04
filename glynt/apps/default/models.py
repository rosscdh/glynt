
import cities_light

def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('GB', 'US'):
        raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)