from application import *
from model import *

#Checks if a given item is already in the database
def db_isItem(itemTuple):
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
def db_createItem(itemTuple):
    name = itemTuple[0]
    quant = itemTuple[1]
    meas = itemTuple[2]
    typ = itemTuple[3]
    newItem = Ingredient(type=typ, name=name, quantity=float(quant), measurement=meas)
    db.session.add(newItem)
    db.session.commit()
    return newItem.id

#Creates a filename given a file's name. This will query the database and make sure we don't have duplicates
def db_createFileName(name, ext):
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
def db_getFileName(name):
    listOfPics = os.listdir(app.config['PICS'])
    for pic in listOfPics:
        if (name.replace(" ", "-") in pic):
            return pic

#Reduces the recipe list by combining same items
def db_reduceList(recipeList):
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

#Adds a new entry into the shopping list table
def db_createShoppingList(listName, currList):
    ingredients = ""
    for type in currList:
        for item in currList[type]:
            if (ingredients == ""):
                ingredients = str(item.id)
            else:
                ingredients = ingredients + "," + str(item.id)
    newList = List(userid=app.config['USERID'], name=listName, ingredients=ingredients)
    db.session.add(newList)
    db.session.commit()
    return newList.id

# Returns all ingredients in database
def db_getIngredients():
    return db.session.query(Ingredient).all()

# Return a specific ingredient from the database
def db_getIngredient(id):
    return db.session.query(Ingredient).filter_by(id = id).first()

# Return a specific ingredient from the database based on other than id
def db_getIngredientsNoID(name, quantity, measurement, type):
    return db.session.query(Ingredient).filter_by(name = name, quantity = quantity, measurement = measurement, type = type).all()

# Returns all recipes in database
def db_getRecipes():
    return db.session.query(Recipe).all()

# Return a specific recipe from the database
def db_getRecipe(id):
    return db.session.query(Recipe).filter_by(id = id).first()

# Delete a list of recipes
def db_deleteRecipes(recipes):
    for id in recipes:
        db.session.query(Recipe).filter_by(id = id).delete()
    db.session.commit()

# Add a recipe to the database
def db_addRecipe(userid, name, ingrs, fileName, desc):
    newRecipe = Recipe(userid = userid, name = name, ingredients = ingrs, img = fileName, recipe = desc)
    db.session.add(newRecipe)
    db.session.commit()

# Update a recipe to the databse
def db_updateRecipe(recipeID, listOfItems):
    recipe = db_getRecipe(recipeID)
    recipe.ingredients = listOfItems
    db.session.commit()

# Get all lists from the database
def db_getLists():
    return db.session.query(List).all()

# Get a specific list from the database
def db_getList(id):
    return db.session.query(List).filter_by(id = id).first()
