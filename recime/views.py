from application import *
from lib import *
from model import *

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/addRecipe')
def addRecipe():
    ingredients = db.session.query(Ingredient).all()
    return render_template('addRecipe.html', ingredients=ingredients)

@app.route('/createRecipe', methods=['POST'])
def createRecipe():
    name = request.form.get('name')
    pic = request.files.getlist('picture')
    items = request.form.getlist('items')
    itemArr = []
    for item in items:
        if (item is not ""):
            itemArr.append(item)
    print("Name: ", name)
    for f in pic:
        f.filename = createFileName(name, f.filename.split(".")[len(f.filename.split(".")) - 1])
        f.save(os.path.join(app.config['PICS'], f.filename))
        print("File: ", f)
    for i in items:
        print("Item: ", i)
    return render_template('editRecipe.html', measurements=app.config['MEASUREMENTS'], types=app.config['TYPES'], name=name, pic=pic[0].filename, items=itemArr)

@app.route('/editRecipe')
def editRecipe():
    recipes = db.session.query(Recipe).all()
    return render_template("editRecipes.html", recipes=recipes)

@app.route('/deleteRecipes', methods=['POST'])
def deleteRecipes():
    recipes = request.form.getlist('recipe')
    for ide in recipes:
        recipe = db.session.query(Recipe).filter_by(id = ide).delete()
    db.session.commit()
    flash("Recipe Successfully Deleted")
    return redirect(url_for('landing'))

@app.route('/changeRecipe/<recipeID>')
def changeRecipe(recipeID):
    recipe = db.session.query(Recipe).filter_by(id = recipeID).first()
    items = recipe.ingredients
    itemList = []
    for item in items.split(","):
        if (item is not "" and item is not None):
            itemList.append(db.session.query(Ingredient).filter_by(id = item).first())
    return render_template('changeRecipe.html', measurements=app.config['MEASUREMENTS'], types=app.config['TYPES'], recipe=recipe, items=itemList, pic=getFileName(recipe.name))

@app.route('/add/<name>', methods=['POST'])
def addRecipeToDB(name):
    items = request.form.getlist('items')
    recipeDesc = request.form.get('recipeDesc')
    itemsArr = []
    itemIDs = []
    for item in items:
        itemsArr.append((str(item),
                        request.form.get(str(item) + 'q'),
                        request.form.get(str(item) + 'm'),
                        request.form.get(str(item) + 't')));
    for tup in itemsArr:
        if (not isItem(tup)):
            itemIDs.append(createItem(tup))
        else:
            ingredient = db.session.query(Ingredient).filter_by(name = tup[0], quantity = tup[1], measurement = tup[2], type = tup[3]).all()
            itemIDs.append(ingredient[0].id)
    recipeName = name.split("/")[len(name.split("/")) - 1].split(".")[0]
    listOfItems = ""
    for ide in itemIDs:
        if (listOfItems == ""):
            listOfItems = str(ide)
        else:
            listOfItems = listOfItems + " ," + str(ide)
    newRecipe = Recipe(userid = app.config['USERID'], name = recipeName, ingredients = listOfItems, img = getFileName(name), recipe = recipeDesc)
    db.session.add(newRecipe)
    db.session.commit()
    return redirect(url_for('landing'))

@app.route('/startShopping')
def startShoppingList():
    recipes = db.session.query(Recipe).all()
    return render_template("startShoppingList.html", recipes=recipes)

@app.route('/readList')
def readList():
    lists = db.session.query(List).all()
    return render_template("readShoppingLists.html", lists=lists)

@app.route('/openList/<listID>')
def openList(listID):
    list = db.session.query(List).filter_by(id = listID).first()
    items = list.ingredients
    itemList = []
    for item in items.split(","):
        if (item is not "" and item is not None):
            itemList.append(db.session.query(Ingredient).filter_by(id = item).first())
    return render_template("readShoppingList.html", ingredients=itemList, list=list)

@app.route('/createList', methods=['POST'])
def createShoppingList():
    recipes = request.form.getlist('recipe')
    recipeList = {}
    for ide in recipes:
        recipe = db.session.query(Recipe).filter_by(id = ide).first()
        recipeName = recipe.name
        recipeFile = recipe.img
        for itemID in recipe.ingredients.split(","):
            item = db.session.query(Ingredient).filter_by(id = itemID).first()
            try:
                recipeList[item.type].append(item)
            except:
                recipeList[item.type] = [item]
    recipeList = reduceList(recipeList)
    app.config['CURR_RECIPE'] = recipeList
    return render_template('generateList.html', recipeList=recipeList)

@app.route('/finalize', methods=['POST'])
def finalizeShoppingList():
    currList = app.config['CURR_RECIPE']
    listName = request.form.get("name")
    for itemType in currList:
        delItems = request.form.getlist(itemType)
        for itemID in delItems:
            for i in currList[itemType]:
                if (i.id == int(itemID)):
                    currList[itemType].remove(i)
    app.config['CURR_RECIPE'] = currList
    db_createShoppingList(listName, currList)
    return render_template('shoppingList.html', recipeList=currList)

@app.route('/updateRecipe/<recipeID>', methods=['POST'])
def updateRecipe(recipeID):
    itemsArr = []
    itemIDs = []
    recipe = db.session.query(Recipe).filter_by(id = recipeID).first()
    items = recipe.ingredients
    for itemID in items.split(","):
        item = db.session.query(Ingredient).filter_by(id = itemID).first()
        print(item.name, request.form.get(str(item.name) + 'q'), request.form.get(item.name + 'm'), request.form.get(item.name + 't'))
        quantity = request.form.get(str(item.name) + 'q')
        measurement = request.form.get(str(item.name) + 'm')
        type = request.form.get(str(item.name) + 't')

        # Update the ingredient in the db if changed
        if (quantity != str(item.quantity) or measurement != str(item.measurement) or type != str(item.type)):
            item.quantity = quantity
            item.measurement = measurement
            item.type = type
            db.session.commit()

        #Add the ingredient to our items array to change the recipe later
        itemsArr.append((str(item.name), quantity, measurement, type));
    for tup in itemsArr:
        if (not isItem(tup)):
            itemIDs.append(createItem(tup))
        else:
            ingredient = db.session.query(Ingredient).filter_by(name = tup[0], quantity = tup[1], measurement = tup[2], type = tup[3]).all()
            itemIDs.append(ingredient[0].id)
    listOfItems = ""
    for ide in itemIDs:
        if (listOfItems == ""):
            listOfItems = str(ide)
        else:
            listOfItems = listOfItems + " ," + str(ide)
    recipe.ingredients = listOfItems
    db.session.commit()
    return redirect(url_for('landing'))

@app.route('/download')
def downloadList():
    recipeList = app.config['CURR_RECIPE']
    newFile = os.path.join(app.config['DOCS'], 'shoppingList.txt')
    output = open(newFile, 'w')
    for t in recipeList:
        output.write("\t" + str(t).upper())
        output.write("\n\n")
        for item in recipeList[t]:
            output.write("   * " + str(item.name) + " " + str(item.quantity) + " " + str(item.measurement))
            output.write("\n")
        output.write("==========================================================================")
    output.close()
    retFile = 'utils/documents/' + 'shoppingList.txt'
    return send_file(retFile, as_attachment=True, mimetype='text/plain')
