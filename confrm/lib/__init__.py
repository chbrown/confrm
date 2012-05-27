import random
import hashlib

def hash_password(string):
    return hashlib.sha256(string).hexdigest()

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
