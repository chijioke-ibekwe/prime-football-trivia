import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = 'prime-football-trivia'
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "postgres", "localhost:5432", database_name
)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    difficulty = Column(Integer)
    options = db.relationship('Option', backref='questions', lazy=False)

    def __init__(self, question, answer, difficulty):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

        return self.id

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'options': self.options,
            'answer': self.answer,
            'difficulty': self.difficulty
            }


class Option(db.Model):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    option = Column(String, nullable=False)
    letter = Column(String, nullable=False)
    question_id = Column(Integer, db.ForeignKey('questions.id'), nullable=False)

    def __init__(self, option, letter, question_id):
        self.option = option
        self.letter = letter
        self.question_id = question_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'option': self.option,
            'letter': self.letter,
            'question_id': self.question_id
            }