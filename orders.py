"""API regarding orders"""
from flask import Flask, Blueprint, render_template, json, request, current_app, jsonify
from models import *
import sqlalchemy

orders = Blueprint('orders', __name__)

@orders.route('/api/Order/GetCurrent', methods=['GET'])
def getCurrent():
    db = current_app.config["db"]
    id = db.session.query(PizzaHouse).filter(PizzaHouse.ModeratorId == 1).first().Id
    query_modified = db.session\
        .query(OrderItem)\
        .filter(OrderItem.Order.has(PizzaHouseId=id))\
        .filter(sqlalchemy.not_(OrderItem.Order.has(Status=4)))\
        .filter(OrderItem.IsModified == True)
    fixed_query = db.session\
        .query(OrderItem, FixPizza)\
        .filter(OrderItem.PizzaId == FixPizza.Id)\
        .filter(OrderItem.Order.has(PizzaHouseId=id))\
        .filter(sqlalchemy.not_(OrderItem.Order.has(Status=4)))\
        .filter(OrderItem.IsModified == False)
    fixed = [GetOrderViewModel(item, pizza) for item, pizza in fixed_query]
    modified = [GetOrderViewModel(x) for x in query_modified]
    res = fixed + modified
    return jsonify(res)

@orders.route('/api/Order/GetNew', methods=['GET'])
def getNew():
    db = current_app.config["db"]
    id = db.session.query(PizzaHouse).filter(PizzaHouse.ModeratorId == 1).first().Id
    query_modified = db.session\
        .query(OrderItem)\
        .filter(OrderItem.Order.has(PizzaHouseId=id))\
        .filter(OrderItem.Order.has(Status=0))\
        .filter(OrderItem.IsModified == True)
    fixed_query = db.session\
        .query(OrderItem, FixPizza)\
        .filter(OrderItem.PizzaId == FixPizza.Id)\
        .filter(OrderItem.Order.has(PizzaHouseId=id))\
        .filter(OrderItem.Order.has(Status=0))\
        .filter(OrderItem.IsModified == False)
    fixed = [GetOrderViewModel(item, pizza) for item, pizza in fixed_query]
    modified = [GetOrderViewModel(x) for x in  query_modified]
    res = fixed + modified
    return jsonify(res)

@orders.route('/api/settings', methods=['GET'])
def getSettings():
    db = current_app.config["db"]
    house = db.session.query(PizzaHouse).filter(PizzaHouse.ModeratorId == 1).first()
    in_stock_query = db.session\
        .query(IngredientAmount)\
        .filter(IngredientAmount.PizzaHouseId == house.Id)
    in_stock = [GetIngredientQuantityDto(item) for item in in_stock_query]
    res = GetSettingsModel(house)
    res["InStock"] = in_stock
    return jsonify(res)

@orders.route('/api/pizza', methods=['GET'])
def getPizzaHouses():
    db = current_app.config["db"]
    return jsonify(getAllPizzaHouses(db.session))



@orders.route('/api/pizza', methods=['POST'])
def getApropriatePizzaHouses():
    db = current_app.config["db"]
    order_settings = request.get_json()
    houses = getAllPizzaHouses(db.session)
    ing_counts = {}
    for item in order_settings["orderItems"]:
        for ing in item["ingredients"]:
            id = ing["id"]
            if id in ing_counts:
                ing_counts[id] = ing_counts[id] + ing["count"]
            else:
                ing_counts[id] = ing["count"]
        
    return jsonify([house for house in houses if filterPizzaHouses(house, ing_counts)])

@orders.route('/api/settings', methods=['POST'])
def postSettings():
    house_settings = request.get_json()
    db = current_app.config["db"]
    house = db.session.query(PizzaHouse).get(house_settings["PizzaHouseId"])
    house.Capacity = house_settings["Capacity"]
    ing_quantity_dict = {}
    for quantity in house_settings["IngState"]:
        item = db.session\
                .query(Ingredient, IngredientAmount)\
                .filter(sqlalchemy.and_(Ingredient.Id == quantity["Id"],  
                                IngredientAmount.PizzaHouseId == house.Id,
                                IngredientAmount.IngredientId == Ingredient.Id))\
                .first()
        if item is None:
            ing_qu = IngredientAmount()
            ing_qu.IngredientId = quantity["Id"]
            ing_qu.PizzaHouseId = house.Id
            ing_qu.Quantity = quantity["Quantity"]
            db.session.add(ing_qu)
        else:
            item.IngredientAmount.Quantity = quantity["Quantity"]
        ing_quantity_dict[quantity["Id"]] = quantity["Quantity"]

    db.session.commit()
    return jsonify({
            'status' : "success"
        })

@orders.route('/api/order/accept/<id>', methods=['POST'])
def acceptOrder(id):
    db = current_app.config["db"]
    order = db.session.query(Order).filter(Order.Id == id).first()
    if order.Status == 0:
        order.Status = 1
        db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@orders.route('/api/order/reject/<id>',  methods=['POST'])
def rejectOrder(id):
    db = current_app.config["db"]
    order = session.query(Order).filter(Order.Id == id).first()
    order.Status = 4
    session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def GetSettingsModel(item):
    res = {
        'Id': item.Id,
        'Close': 24,
        'Open': 9,
        'Capacity': item.Capacity
    }
    return res

def GetOrderViewModel(item, pizza=None):
    res = {}
    res['Id'] = item.Id
    res['State'] = item.Order.Status
    res['Start'] = item.StartTime
    res['End'] = item.EndTime
    res['OrderId'] = item.OrderId
    res['Price'] = int(item.Price)
    res['StartStr'] = item.StartTime.strftime("%Y-%m-%d")
    res['EndStr'] = item.EndTime.strftime("%Y-%m-%d")
    res['StHour'] = item.StartTime.hour
    res['StMinute'] = item.StartTime.minute
    res['EndHour'] = item.EndTime.hour
    res['EndMinute'] = item.EndTime.minute
    if pizza is None:
        res['Name'] = "Custom"
    else:
        res['Name'] = pizza.Name
    return res

def GetIngredientDto(item):
    res = {}
    res['Id'] = item.Id
    res['Price'] = float(item.Price)
    res['Weight'] = float(item.Weight)
    res['Name'] = item.Name
    return res

def GetIngredientQuantityDto(item):
    res = {}
    res['Quantity'] = item.Quantity
    res['IngredientDto'] = GetIngredientDto(item.Ingredient)
    return res

def getAllPizzaHouses(session):
    houses = session.query(PizzaHouse)
    res = []
    for house in houses:
        in_stock_query = session\
            .query(IngredientAmount)\
            .filter(IngredientAmount.PizzaHouseId == house.Id)
        in_stock = [GetIngredientQuantityDto(item) for item in in_stock_query]
        res.append(GetSettingsModel(house))
        res[len(res) - 1]["InStock"] = in_stock
    return res

def filterPizzaHouses(house, ingCounts):
    house_ing_count = {}
    for ing in house["InStock"]:
        house_ing_count[ing["IngredientDto"]["Id"]] = ing["Quantity"]
    
    for key, value in ingCounts.items():
        if (not key in house_ing_count) or house_ing_count[key] < value:
            return False
    
    return True