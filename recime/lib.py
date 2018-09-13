from application import *
from model import *

#Checks if a given item is already in the database
def isItem(itemTuple):
    nm = itemTuple[0]
    quant = itemTuple[1]
    meas = itemTuple[2]
    typ = itemTuple[3]
    print(nm, quant, meas, typ)
    ingredient = db.session.query(Ingredient).filter_by(name = nm, quantity = quant, measurement = meas, type = typ).all()
    if (len(ingredient) > 0):
        return True
    return False

#Creates a new Item; takes in a tuple and creates the item in the database
#Format of the tuple: (itemName, item quantity, item measurement, item type)
def createItem(itemTuple):
    name = itemTuple[0]
    quant = itemTuple[1]
    meas = itemTuple[2]
    typ = itemTuple[3]
    newItem = Ingredient(type=typ, name=name, quantity=float(quant), measurement=meas)
    db.session.add(newItem)
    db.session.commit()
    return newItem.id

#Creates a filename given a file's name. This will query the database and make sure we don't have duplicates
def createFileName(name, ext):
    listofnames = db.session.query(Recipe).filter_by(name = name).all()
    counter = 0
    currName = name
    while (len(listofnames) > 0):
        currName = str(name) + str(counter)
        counter += 1
        listOfItems = db.session.query(Recipe).filter(name = currName).all()
    filename = currName + "." + str(ext)
    filename = filename.replace(" ", "-")
    return filename

#Gets the filename of a given recipe name
def getFileName(name):
    listOfPics = os.listdir(app.config['PICS'])
    for pic in listOfPics:
        if (name.replace(" ", "-") in pic):
            return pic

#Reduces the recipe list by combining same items
def reduceList(recipeList):
    for itemType in recipeList:
        delList = []
        for i in range(len(recipeList[itemType])):
            for j in range(len(recipeList[itemType])):
                if (i != j):
                    iItem = recipeList[itemType][i]
                    jItem = recipeList[itemType][j]
                    if (iItem.name == jItem.name and iItem.measurement == jItem.measurement and iItem not in delList and jItem not in delList):
                        jItem.quantity = jItem.quantity + iItem.quantity
                        delList.append(iItem)
        for index in delList:
            recipeList[itemType].remove(index)
    return recipeList
