'''Python script to check too good to go api'''
import smtplib
import json
import time
import os
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tgtg import TgtgClient


class Api:
    '''Api for good to go manager'''

    def __init__(self):
        '''Constructor for class'''
        self.config_file   = "./config.json"
        self.account       = ''
        self.password      = ''
        self.from_email    = ''
        self.to_email      = ''
        self.from_password = ''
        self.data_list     = []

    def get_config(self):
        '''Get configuration values'''
        print('# get_config()')
        try:
            if not os.path.isfile(self.config_file):
                return False
            config_file        = open(self.config_file, "r")
            config_data        = json.load(config_file)
            self.account       = config_data["email"]
            self.password      = config_data["password"]
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
            message['Subject'] = 'Two Good To Go Daily Update'
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
        if len(self.data_list) > 0:
            message = ''
            msg_list = []
            for data in self.data_list:
                if data["available"] > 0:
                    text = '{} has {} packages available until {}\n\n'
                else:
                    text = '{} has {} packages available {}\n\n'
                msg_list.append(text.format(data["store"], data["available"], data["end_time"]))
            message = message.join(msg_list)
            self.email(message)

    def check_item(self, item):
        '''Check each item for fields'''
        print('# check_item()')
        try:
            store_name = item["store"]["store_name"]
            count = item["items_available"]
            if count > 0:
                available_till = item["purchase_end"]
            else:
                available_till = ""
            data = {
                "store": store_name,
                "available": count,
                "end_time": available_till
            }
            self.data_list.append(data)
            time.sleep(1)
        except KeyError as error:
            print('Key Error: {}'.format(error))
            print('Item: {}'.format(item))
        except ValueError as error:
            print('Value Error: {}'.format(error))
            print('Item: {}'.format(item))

    def get_items(self):
        '''Get 2G2G favourites'''
        print('# get_items()')
        try:
            if not self.get_config():
                return
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

api = Api()
api.get_items()
