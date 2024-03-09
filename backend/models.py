from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import ForeignKey, MetaData
from datetime import datetime


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players_table'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Player {self.id}>'