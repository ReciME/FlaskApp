from flaskr import db
"""
    The Database Tables

    Recipe is a table that consists of an id, name, picture, and listofItems. The listofItems will just be a list
    of id's for the Item table.

    Item is just a table for an individual food item. This will be the id, type (produce, meat, etc), and a name
"""
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300))
    listOfItems = db.Column(db.String(300))
    file = db.Column(db.String(300))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(300))
    name = db.Column(db.String(300))
    quantity = db.Column(db.Integer)
    measurement = db.Column(db.String(300))
