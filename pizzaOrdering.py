from flask import Flask, Blueprint, render_template, json, request
import json

pizzaOrdering = Blueprint('pizzaOrdering', __name__)

import sqlalchemy
from sqlalchemy import create_engine
from models import *

models = __import__("models")


@pizzaOrdering.route("/api/pizzas/fix")
def getFixPizzas():
    fixPizzas = []
    for pizza in models.session.query(FixPizza).order_by(FixPizza.Id):
        ingredients = []
        for ingredientItem in models.session.query(IngredientItem).filter(IngredientItem.FixPizza_Id == pizza.Id):
            ingredient = ingredientItem.Ingredient
            ingredientName = ingredient.Name
            ingredients.append({'Name': ingredientName, 'IngredientId': ingredient.Id, 'Price': float(ingredient.Price) })

        pizzaName = pizza.Name
        fixPizzas.append({'Id': pizza.Id, 'Name': pizzaName, 'Price': float(pizza.Price), 'Ingredients': ingredients})

    print(json.dumps(fixPizzas))
    return json.dumps(fixPizzas)


@pizzaOrdering.route("/api/ingredients")
def getIngredients():
    ingredients = []
    for ingredient in models.session.query(Ingredient).order_by(Ingredient.Id):
        ingredients.append({'Id': ingredient.Id, 'Name': ingredient.Name, 'Price': float(ingredient.Price), 'Weight': ingredient.Weight})

    print(json.dumps(ingredients))
    return json.dumps(ingredients)