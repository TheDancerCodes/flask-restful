"""
Models to represent and persist the message categories,
messages, and their relationships.
SQLAlchemy will use the data to generate the tables in the PostgreSQL database.
"""

from marshmallow import Schema, fields, pre_load
from marshallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# creates an instance of the flask_sqlalchemy.SQLAlchemy class
# instance will provide access to all the SQLAlchemy functions and classes.
db = SQLAlchemy()

# creates an instance of the flask_marshmallow.Marshmallow class.
# Marshmallow is a wrapper class that integrates Mashmallow with a Flask app.
ma = Marshmallow()

# Declares these methods to add, update, and delete a resource through SQLAlchemy sessions:
class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.add(resource)
        return db.session.commit()

# db.relationship function provides a many-to-one relationship to the Category model.
class Message(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('messages', lazy='dynamic', order_by='Message.message'))
    printed_times = db.Column(db.Integer, nullable=False, server_default='0')
    printed_once = db.Column(db.Boolean, nullable=False, server_default='false')

    def __init__(self, message, duration, category):
        self.message = message
        self.duration = duration
        self.category = category


class Category(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


# Flask-Marshmallow schemas to validate, serialize, and deserialize the
# previously declared Category and Message models and their relationships.

# We have two objects that nest to each other, that is,
# We will create a two-way nesting between categories and messages.
class CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.categoryresource', id='<id>', _external=True)
    messages = fields.Nested('MessageSchema', many=True, exclude=('category',))0029

class MessageSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    message = fields.String(required=True, validate=validate.Length(1))
    duration = fields.Integer()
    creation_date = fields.DateTime()
    category = fields.Nested(CategorySchema, only=['id', 'url', 'name'], required=True)
    printed_times = fields.Integer()
    printed_once = fields.Boolean()
    url = ma.URLFor('api.messageresource', id='<id>', _external=True)


 # This decorator registers a method to invoke before deserializing an object.
 # Before Marshmallow deserializes a message, the process_category method will be executed.

 # The code in the process_category method checks the value for the 'category'
 # key and returns a dictionary with the appropriate data to make it sure that
 # we are able to deserialize a category with the appropriate key-value pairs,
 # no matter the differences of the incoming data.
    @pre_load
    def process_category(self, data):
        category = data.get('category')
        if category:
            if isinstance(category, dict):
                category_name = category.get('name')
            else:
                category_name = category
            category_dict = dict(name=category_name)
        else:
            category_dict = {}
        data['category'] = category_dict
        return data
