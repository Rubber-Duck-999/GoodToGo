#!/usr/bin/python3

class Stores:

    def __init__(self):
        '''Constructor for stores class'''
        self.stores = []
        self.stores_updated = False

    def add_store(self, store_name, count):
        '''Adds a store to the list'''
        store = {
            'store_name': store_name,
            'count': count,
            'updated': True
        }
        self.stores.append(store)
        self.stores_updated = True

    def find(self, store_name):
        '''Checks if a store exists'''
        found = False
        for store in self.stores:
            name = store['store_name']
            if name == store_name:
                found = True
        return found

    def update_count(self, store_name, store_count):
        '''Update the count for store'''
        for store in self.stores:
            name = store['store_name']
            if name == store_name:
                if store['count'] != store_count:
                    store['count'] = store_count
                    store['updated'] = True
                    self.stores_updated = True
