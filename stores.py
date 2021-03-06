#!/usr/bin/python3

class Stores:

    def __init__(self):
        '''Constructor for stores class'''
        self.stores = []
        self.stores_updated = False

    def add_store(self, store_name, count):
        '''Adds a store to the list'''
        print('# add_store()')
        updated = True
        store = {
            'store_name': store_name,
            'count': count,
            'updated': updated
        }
        self.stores.append(store)
        self.stores_updated = True

    def find(self, store_name):
        '''Checks if a store exists'''
        print('# find()')
        found = False
        index = 0
        for i in range(len(self.stores)):
            name = self.stores[i]['store_name']
            if name == store_name:
                found = True
                index = i
        return found, index

    def update_count(self, store_index, store_count):
        '''Update the count for store'''
        print('# update_count()')
        count = self.stores[store_index]['count']
        self.stores[store_index]['count'] = store_count
        if store_count > 0 and count != store_count:
            self.stores[store_index]['updated'] = True
            self.stores_updated = True
        else:
            self.stores[store_index]['updated'] = False
