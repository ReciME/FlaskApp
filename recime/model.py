from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String, Text, text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    type = Column(String(255))
    name = Column(String(255))
    quantity = Column(Numeric)
    measurement = Column(String(255))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    _pass = Column('pass', String(128), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255))
    ingredients = Column(String(255))
    nutritionid = Column(Integer)
    img = Column(Text)
    recipe = Column(Text)

    user = relationship('User')
