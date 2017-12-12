from flask import Flask, Blueprint, render_template, json, request, current_app
import json

pizzaOrdering = Blueprint('pizzaOrdering', __name__)

import sqlalchemy
from sqlalchemy import create_engine
from models import *


@pizzaOrdering.route("/api/pizzas/fix")
def getFixPizzas():
    db = current_app.config["db"]
    fixPizzas = []
    for pizza in db.session.query(FixPizza).order_by(FixPizza.Id):
        ingredients = []
        for ingredientItem in db.session.query(IngredientItem).filter(IngredientItem.FixPizza_Id == pizza.Id):
            ingredient = ingredientItem.Ingredient
            ingredientName = ingredient.Name
            ingredients.append({'Name': ingredientName, 'IngredientId': ingredient.Id, 'Price': float(ingredient.Price) })

        pizzaName = pizza.Name
        fixPizzas.append({'Id': pizza.Id, 'Name': pizzaName, 'Price': float(pizza.Price), 'Ingredients': ingredients})

    print(json.dumps(fixPizzas))
    return json.dumps(fixPizzas)


@pizzaOrdering.route("/api/ingredients")
def getIngredients():
    db = current_app.config["db"]
    ingredients = []
    for ingredient in db.session.query(Ingredient).order_by(Ingredient.Id):
        ingredients.append({'Id': ingredient.Id, 'Name': ingredient.Name, 'Price': float(ingredient.Price), 'Weight': ingredient.Weight})

    print(json.dumps(ingredients))
    return json.dumps(ingredients)