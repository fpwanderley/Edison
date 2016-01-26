from requests import *

IP_ADDRESS = 'http://localhost'
PORT = ':8000'
MESSAGE_URL = '/receiver/receive_message_data'
COMMAND_URL = '/receiver/receive_command'

CHART_DATA = 'chart_data'
CHAT_DATA = 'chat_data'
IA_DATA = 'ia_data'

class Sender(object):

    def create_JSON_obj(self, type, data):
        json_data = {
            "type": type,
            "data": data
        }
        return json_data

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

    def send_message(self, message, timestamp, case, type=CHAT_DATA):
        if (type==CHAT_DATA):
            payload_message = self.create_JSON_obj(type=type,
                                                   data=('{0}s: {1}').format(timestamp, message))
        elif (type==CHART_DATA):
            payload_message = self.create_JSON_obj(type=type,
                                                   data=message)
        elif (type==IA_DATA):
            payload_message = self.create_JSON_obj(type=type,
                                                   data=message)

        payload = {
            'message':str(payload_message),
            'case': case
        }
        return post(self.message_url, payload)
