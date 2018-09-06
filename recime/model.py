from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, server_default=text("nextval('ingredients_id_seq'::regclass)"))
    type = Column(String(255))
    name = Column(String(255))
    quantity = Column(Integer)
    measurement = Column(String(255))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = Column(String(255), nullable=False)
    _pass = Column('pass', String(255), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, server_default=text("nextval('recipes_id_seq'::regclass)"))
    userid = Column(ForeignKey('users.id'), nullable=False)
    name = Column(String(255))
    ingredients = Column(String(255))
    nutritionid = Column(Integer)
    img = Column(LargeBinary)
    recipe = Column(Text)

    user = relationship('User')
