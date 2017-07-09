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


# This is a subclass of flask_restful.Resource and represents a RESTful Resource
# We declare methods for each supported HTTP verb here.
class Message(Resource):
    def abort_if_message_doesnt_exist(self, id):
        if id not in message_manager.messages:
            abort(
                status.HTTP_404_NOT_FOUND,
                message = "Message {0} doesn't exist".format(id))

# @marshal_with decorator takes message_fields as an argument.
# The decorator takes MessageModel instance and applies the field filtering
# and output formatting specified in message_fields.
# NB: Using @marshal_with decorator, automatically returns a HTTP 200 OK status code.
    @marshal_with(message_fields)
    def get(self, id):
        self.abort_if_message_doesnt_exist(id)
        return message_manager.get_message(id)

    @marshal_with(message_fields)
    def delete(self, id):
        self.abort_if_message_doesnt_exist(id)
        message_manager.delete_message(id)
        return '', status.HTTP_204_NO_CONTENT

    @marshal_with(message_fields)
    def patch(self, id):
        self.abort_if_message_doesnt_exist(id)
        message = message_manager.get_message(id)
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('duration', type=int)
        parser.add_argument('printed_times', type=int)
        parser.add_argument('printed_once', type=bool)

        # Call the parser.parse_args method to parse all the arguments
        # from the request and save the returned dictionary in the args variable.
        args = parser.parse_args()

        if 'message' in args:
            message.message = args['message']
        if 'duration' in args:
            message.duration = args['duration']
        if 'printed_times' in args:
            message.printed_times = args['printed_times']
        if 'printed_once' in args:
            message.printed_once = args['printed_once']
        return message

# MessageList class that represents the collection of messages.
class MessageList(Resource):
    @marshal_with(message_fields)
    def get(self):
        return [v for v in message_manager.messages.values()]

    @marshal_with(message_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True, help='Message cannot be blank!')
        parser.add_argument('duration', type=int, required=True, help='Duration cannot be blank!')
        parser.add_argument('message_category', type=str, required=True, help='Message category cannot be blank!')
        args = parser.parse_args()
        message = MessageModel(
            message=args['message'],
            duration=args['duration'],
            creation_date=datetime.now(utc),
            message_category=args['message_category']
        )
        message_manager.insert_message(message)
        return message, status.HTTP_201_CREATED


# Create the main entry point for the application,
# Initialize it with a Flask application and
# Configure the resource routing for the api.
app = Flask(__name__)
api = Api(app)
api.add_resource(MessageList, '/api/messages/')
api.add_resource(Message, '/api/messages/<int:id>', endpoint='message_endpoint')

if __name__ == '__main__':
    app.run(debug=True)
