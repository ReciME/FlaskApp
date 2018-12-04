from flask import jsonify
from lib import *

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = db_getRecipes()
    ret = []
    for recipe in recipes:
        tmp = {
            'id': recipe.id,
            'userid': recipe.userid,
            'name': recipe.name,
            'ingredients': recipe.ingredients,
            'nutritionid': recipe.nutritionid,
            'img': recipe.img,
            'recipe': recipe.recipe
        }
        ret.append(tmp)
    return jsonify({'recipes': ret})
