from flask import jsonify
from lib import *

def get_recipe_dict(recipe):
    dict = {
        'id': recipe.id,
        'userid': recipe.userid,
        'name': recipe.name,
        'ingredients': recipe.ingredients,
        'nutritionid': recipe.nutritionid,
        'img': recipe.img,
        'recipe': recipe.recipe
    }
    return dict

def get_ingredient_dict(ingredient):
    dict = {
        'id': ingredient.id,
        'type': ingredient.type,
        'name': ingredient.name,
        'quantity': str(ingredient.quantity),
        'measurement': ingredient.measurement
    }
    return dict

def get_list_dict(list):
    dict = {
        'id': list.id,
        'userid': list.userid,
        'name': list.name,
        'ingredients': list.ingredients
    }
    return dict

# Recipes
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = db_getRecipes()
    ret = []
    for recipe in recipes:
        ret.append(get_recipe_dict(recipe))
    return jsonify({'recipes': ret})

@app.route('/api/recipe/<id>', methods=['GET'])
def get_recipe(id):
    recipe = db_getRecipe(id)
    return jsonify(get_recipe_dict(recipe))

# Ingredients
@app.route('/api/ingredient/<id>', methods=['GET'])
def get_ingredient(id):
    ingredient = db_getIngredient(id)
    return jsonify(get_ingredient_dict(ingredient))

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = db_getIngredients()
    ret = []
    for ingredient in ingredients:
        ret.append(get_ingredient_dict(ingredient))
    return jsonify({'ingredients': ret})

# Shopping List
@app.route('/api/shoppinglists', methods=['GET'])
def get_shopping_lists():
    lists = db_getLists()
    ret = []
    for list in lists:
        ret.append(get_list_dict(list))
    return jsonify({'lists': ret})

@app.route('/api/shoppinglist/<id>', methods=['GET'])
def get_shopping_list(id):
    list = db_getList(id)
    return jsonify(get_list_dict(list))
