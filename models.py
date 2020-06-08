import os
# from datetime import datetime, timezone
from sqlalchemy import Column, String, create_engine, Integer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import sys

# if os.environ['ENV'] == 'test':
#   database_path = os.environ['TEST_DATABASE_URL']
# else:
#   database_path = os.environ['DATABASE_URL']

# database_path = os.environ['DATABASE_URL']
# database_path = os.environ.get('DATABASE_URL')
# if not database_path:
#     database_name = "capstone"
#     database_path = "postgres://{}/{}".format(
#         'localhost:5432', database_name)
database_name = "capstone"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    # db_drop_and_create_all()


class Movies(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    #release_date = Column(DateTime())

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}
