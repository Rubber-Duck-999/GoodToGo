import smtplib
from tgtg import TgtgClient
import json
import time
import os

class Api:
    # Api for good to go manager

    def __init__(self):
        # Constructor for class
        self.file          = "./config.json"
        self.email         = ''
        self.password      = ''
        self.from_email    = ''
        self.to_email      = ''
        self.from_password = ''

    def get_config(self):
        # Get configuration values
        print('# get_config()')
        try:
            if not os.path.isfile(self.file):
                return False
            jsonfile           = open(self.file, "r")
            self.config_data   = json.load(jsonfile)
            self.email         = self.config_data["email"]
            self.password      = self.config_data["password"]
            self.from_email    = self.config_data["from_email"]
            self.from_password = self.config_data["from_password"]
            self.to_email      = self.config_data["to_email"]
            return True
        except IOError as error:
            print('File not available: {}'.format(error))
        except KeyError as error:
            print('Key not available: {}'.format(error))
        return False

    def notify_user(self, message):
        # Count of items available
        print('# notify_user')
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.from_email, self.from_password)
            server.sendmail(self.from_email, self.to_email, 'Hi')
            server.close()
        except Exception as error:
            print('Error occured: {}'.format(error))

    def check_item(self, item):
        # Check each item for fields
        print('# check_item()')
        try:
            store_name = item["store"]["store_name"]
            count = item["items_available"]
            available_till = item["purchase_end"]
            data = {
                "store": store_name,
                "available": count,
                "end_time": available_till
            }
            self.notify_user(data)
            time.sleep(1)
        except KeyError:
            print('Key Error')
        except ValueError:
            print('Value Error')

    def get_items(self):
        # Get 2G2G favourites
        print('# get_items()')
        try:
            if not self.get_config():
                return
            client = TgtgClient(email=self.email, 
                                password=self.password)
            items = client.get_items()
            for item in items:
                self.check_item(item)
        except KeyError:
            print('Key Error')
        except TypeError:
            print('Type Error')

api = Api()
api.get_items()