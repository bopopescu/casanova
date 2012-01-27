from django.conf import settings

class CachedItem(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<CachedItem {%s:%s}>' % (self.key, self.value)

class CachedDict(dict):

    def get(self, key):
        if key not in self:
            return None
        return self[key].value
        
    def set(self, key, value):
        if settings.CACHE:
            self[key] = CachedItem(key, value)