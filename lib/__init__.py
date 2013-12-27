import json
import random
from datetime import datetime


def random_ticket():
    store = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.sample(store, 40))


def parse_request(request):
    if request.content_type == 'application/json':
        return request.json_body
    # application/x-www-form-urlencoded
    return request.POST


def update_attributes(obj, dictionary):
    for key, val in dictionary.items():
        setattr(obj, key, val)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)

custom_encoder = CustomEncoder()


def jsonize(obj):
    return custom_encoder.encode(obj)
