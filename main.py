#!/usr/bin/python3
'''Python script to check too good to go api'''
import smtplib
import json
import time
import os
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tgtg import TgtgClient
from stores import Stores


class Api:
    '''Api for good to go manager'''

    def __init__(self):
        '''Constructor for class'''
        self.config_file   = "/home/simon/Documents/HouseGuardServices/config.json"
        self.account       = ''
        self.password      = ''
        self.from_email    = ''
        self.to_email      = ''
        self.from_password = ''
        self.stores        = Stores()

    def get_config(self):
        '''Get configuration values'''
        print('# get_config()')
        try:
            if not os.path.isfile(self.config_file):
                return False
            with open(self.config_file, "r") as config_file:
                config_data        = json.load(config_file)
                self.account       = config_data["account_email"]
                self.password      = config_data["account_password"]
                self.from_email    = config_data["from_email"]
                self.from_password = config_data["from_password"]
                self.to_email      = config_data["to_email"]
            return True
        except IOError as error:
            print('File not available: {}'.format(error))
        except KeyError as error:
            print('Key not available: {}'.format(error))
        except TypeError as error:
            print('Type not available: {}'.format(error))
        return False

    def email(self, text):
        '''Set up message for email from stores'''
        print('# email()')
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            message = MIMEMultipart()
            message['Subject'] = 'Too Good To Go Update'
            message['From'] = self.from_email
            message['To'] = ", ".join(self.to_email)
            message.attach(MIMEText(text, 'plain'))
            server.login(self.from_email, self.from_password)
            server.sendmail(self.from_email, self.to_email, message.as_string())
            server.close()
        except smtplib.SMTPAuthenticationError as error:
            print('Error occured on auth: {}'.format(error))
        except smtplib.SMTPException as error:
            print('Error occured on SMTP: {}'.format(error))

    def notify_user(self):
        '''Count of items available'''
        print('# notify_user()')
        message = ''
        msg_list = []
        if not self.stores.stores_updated:
            return
        found = False
        for store in self.stores.stores:
            if store["updated"]:
                text = '{} has {} packages available\n\n'
                found = True
                msg_list.append(text.format(store["store_name"], store["count"]))
                store["updated"] = False
        if len(msg_list) > 0:
            message = message.join(msg_list)
            self.email(message)
            self.stores_updated = False

    def check_item(self, item):
        '''Check each item for fields'''
        print('# check_item()')
        try:
            store_name = item["store"]["store_name"]
            count = item["items_available"]
            if count > 0:
                print('Found item for: {}, {}'.format(store_name, count))
                store_found, store_index = self.stores.find(store_name)
                if store_found:
                    self.stores.update_count(store_index, count)
                else:
                    self.stores.add_store(store_name, count)
                time.sleep(1)
        except KeyError as error:
            print('Key Error: {}'.format(error))
        except ValueError as error:
            print('Value Error: {}'.format(error))

    def get_items(self):
        '''Get 2G2G favourites'''
        print('# get_items()')
        try:
            client = TgtgClient(email=self.account,
                                password=self.password)
            items = client.get_items()
            for item in items:
                self.check_item(item)
            self.notify_user()
        except KeyError:
            print('Key Error')
        except TypeError:
            print('Type Error')

    def time_loop(self):
        '''Loop checking in time periods'''
        if not self.get_config():
            return
        while True:
            api.get_items()
            print('Waiting')
            time.sleep(60)

if __name__ == "__main__":
    api = Api()
    api.time_loop()
