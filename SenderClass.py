from requests import *

IP_ADDRESS = 'http://localhost'
PORT = ':8000'
MESSAGE_URL = '/receiver/receive_message_data'
COMMAND_URL = '/receiver/receive_command'

class Sender(object):

    def __init__(self, *args, **kwargs):
        self.set_message_url()

    def set_message_url(self):
        self.message_url = IP_ADDRESS + PORT + MESSAGE_URL
        self.command_url = IP_ADDRESS + PORT + COMMAND_URL

    def start_process(self, message):
        payload = {
            'command':message
        }
        return post(self.command_url, payload)

    def finish_process(self, message):
        payload = {
            'command':message
        }
        return post(self.command_url, payload)

    def send_message(self, message, timestamp, case):
        payload_message = ('{0}s: {1}').format(timestamp, message)
        payload = {
            'message':payload_message,
            'case': case
        }
        return post(self.message_url, payload)
