
import cities_light

def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('GB', 'US', 'DE', 'IL', 'AU', 'CA'):
        raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)


from .signals import on_user_logged_in