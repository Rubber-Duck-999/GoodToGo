#!/usr/bin/python3
import unittest
import stores
import main


class TestStores(unittest.TestCase):

    def test_init(self):
        '''Create stores object'''
        test_stores = stores.Stores()
        self.assertFalse(test_stores.stores_updated)
        self.assertEqual(0, len(test_stores.stores))

    def test_add_store(self):
        '''Test adding one store increases list'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 1
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))

    def test_find(self):
        '''Check finding a store'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 1
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))
        # Now check that it can be found
        found, index = test_stores.find(store_name)
        self.assertTrue(found)

    def test_not_find(self):
        '''Check finding a store doesn't find as expected'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 1
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))
        # Now check that it can not be found
        bad_store_name = 'NotRight'
        found, index = test_stores.find(bad_store_name)
        self.assertFalse(found)

    def test_update_zero(self):
        '''Check updating a store success'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 1
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))
        # Now check that it isnt updated for emailing
        test_stores.update_count(0, 0)
        self.assertFalse(test_stores.stores[0]['updated'])

    def test_update_no_change(self):
        '''Check updating a store success'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 0
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))
        # Now check that it isnt updated for emailing
        test_stores.update_count(0, 0)
        self.assertFalse(test_stores.stores[0]['updated'])

    def test_update_change(self):
        '''Check updating a store success'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 0
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))
        # Now check that it can be updated
        test_stores.update_count(0, 2)
        self.assertTrue(test_stores.stores[0]['updated'])

    def test_all_flow(self):
        '''Check the sequential flow of the class'''
        test_stores = stores.Stores()
        store_name = 'Test'
        count = 0
        test_stores.add_store(store_name, count)
        self.assertTrue(test_stores.stores_updated)
        self.assertEqual(1, len(test_stores.stores))
        # Run find to get index
        found, index = test_stores.find(store_name)
        self.assertTrue(found)
        # Now check that it can be updated
        test_stores.update_count(index, 2)
        self.assertTrue(test_stores.stores[index]['updated'])

    def test_main_init(self):
        '''Constructor test for Api'''
        test_api = main.Api()
        self.assertEqual('', test_api.account)

    def test_main_get_config(self):
        '''test for Api checking configuration file'''
        test_api = main.Api()
        test_api.config_file = "/home/simon/Documents/HouseGuardServices/config.json"
        valid = test_api.get_config()
        self.assertTrue(valid)

    def test_check_item_success(self):
        '''Checking item on json object'''
        item = {
            'store': {
                'store_name': 'Greggs'
            },
            'items_available': 0
        }
        test_api = main.Api()
        test_api.check_item(item)
        self.assertTrue(test_api.stores.stores_updated)

    def test_check_item_failure(self):
        '''Checking item is not added as its count is 0'''
        item = {
            'store': {
                'store_name': 'Greggs'
            },
            'item_available': 0
        }
        test_api = main.Api()
        test_api.check_item(item)
        self.assertFalse(test_api.stores.stores_updated)

    def test_check_items(self):
        '''Check item multiple times 
        to ensure its being updated'''
        item = {
            'store': {
                'store_name': 'Greggs'
            },
            'items_available': 0
        }
        test_api = main.Api()
        test_api.check_item(item)
        self.assertTrue(test_api.stores.stores_updated)
        test_api.stores.stores_updated = False
        # Update item and re check
        item = {
            'store': {
                'store_name': 'Greggs'
            },
            'items_available': 1
        }
        test_api.check_item(item)
        self.assertTrue(test_api.stores.stores_updated)

    def test_check_items_no_update(self):
        '''Check items so that a item is not updated with zero count'''
        item = {
            'store': {
                'store_name': 'Greggs'
            },
            'items_available': 0
        }
        test_api = main.Api()
        test_api.check_item(item)
        self.assertTrue(test_api.stores.stores_updated)
        test_api.stores.stores_updated = False
        # Update item and re check
        item['items_available'] = 0
        test_api.check_item(item)
        self.assertFalse(test_api.stores.stores_updated)

    def test_check_items_no_update_again(self):
        '''Check items so that a item is 
        not updated with same count'''
        item = {
            'store': {
                'store_name': 'Greggs'
            },
            'items_available': 2
        }
        test_api = main.Api()
        test_api.check_item(item)
        self.assertTrue(test_api.stores.stores_updated)
        test_api.stores.stores_updated = False
        # Update item and re check
        item['items_available'] = 2
        test_api.check_item(item)
        self.assertFalse(test_api.stores.stores_updated)

if __name__ == '__main__':
    unittest.main()