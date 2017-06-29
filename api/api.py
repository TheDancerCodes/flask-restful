"""
Creating a MessageManager class that will persist the MessageModel instances
in an in-memory dictionary.

insert_message:
This method receives a recently created MessageModel instance in the message argument.
The code increases the value for the last_id class attribute and then assigns
the resulting value to the id for the received message.
Finally, the code adds the message as a value to the key identified with the
generated id, last_id, in the self.messages dictionary.

get_message:
This method receives the id of the message that has to be retrieved from the
self.messages dictionary.

delete_message:
This method receives the id of the message that has to be removed from the
self.messages dictionary.

"""

from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import MessageModel
import status
from pytz import utc

class MessageManager():
    last_id = 0
    def __init__(self):
        self.messages = {}

    def insert_message(self, message):
        self.__class__.last_id += 1
        message.id = self.__class__.last_id
        self.messages[self.__class__.last_id] = message

    def get_message(self, id):
        return self.messages[id]

    def delete_message(self, id):
        del self.messages[id]


# create a message_fields dictionary to control the data that we want
# Flask_RESTful to render in our response, when we return MessageModel instances
message_fields = {
    'id': fields.Integer,
    'uri': fields.Url('message_endpoint'),
    'message': fields.String,
    'duration': fields.Integer,
    'creation_date': fields.DateTime,
    'message_category': fields.String,
    'printed_times': fields.Integer,
    'printed_once': fields.Boolean
}

# create an instance of the previously created MessageManager class.
# We use this instance to create, retrieve, and delete MessageModel instances.
message_manager = MessageManager()
