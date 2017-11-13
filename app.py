from flask import Flask, Blueprint, render_template, json, request, jsonify

app = Flask(__name__, static_url_path='')
import sqlalchemy
from sqlalchemy import create_engine
from models import *
from pizzaOrdering import pizzaOrdering

models = __import__("models")
app.register_blueprint(pizzaOrdering)

@app.route("/")
def main():
    return render_template('layout.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
'''
@app.route('/api/Account/Login',methods=['POST'])
def login():
    model = request.form
    print(model)
    if(model['userName'][0:3] == 'bad') :
        return "bad request", 400
    if(model['userName'][0:3] == 'mod') :
        return jsonify({
            'status' : "success",
            'redirect_url' : "views/moderator/ModeratorLayout.html#/" 
        })
    
    return jsonify({
            'status' : "success"
        })

@app.route('/api/Account/Logout',methods=['POST'])
def logout():
    return jsonify({
            'status' : "success"
        })
 
    # read the posted values from the UI
    #_name = request.form['inputName']
    #_email = request.form['inputEmail']
    #_password = request.form['inputPassword']
 
    # validate the received values
    #if _name and _email and _password:
    #    return json.dumps({'html':'<span>All fields good !!</span>'})
    #else:
    #    return json.dumps({'html':'<span>Enter the required fields</span>'})


#Will move later
@app.route('/api/Order/GetCurrent', methods=['GET'])
def getCurrent():
    sessionlocal = getSession()
    id = sessionlocal.query(PizzaHouse).filter(PizzaHouse.ModeratorId == 1).first().Id
    queryModified = sessionlocal\
        .query(OrderItem)\
        .filter(OrderItem.Order.has(PizzaHouseId = id))\
        .filter(sqlalchemy.not_(OrderItem.Order.has(Status = 4)))\
        .filter(OrderItem.IsModified == True)
    fixedQuery = sessionlocal\
        .query(OrderItem, FixPizza)\
        .filter(OrderItem.PizzaId == FixPizza.Id)\
        .filter(OrderItem.Order.has(PizzaHouseId = id))\
        .filter(sqlalchemy.not_(OrderItem.Order.has(Status = 4)))\
        .filter(OrderItem.IsModified == False)
   
    fixed = [GetOrderViewModel(item, pizza) for item, pizza in fixedQuery]
    modified = [GetOrderViewModel(x) for x in  queryModified ]
    res = fixed + modified
    sessionlocal.close()
    return jsonify(res)

@app.route('/api/Order/GetNew', methods=['GET'])
def getNew():
    sessionlocal = getSession()
    id = sessionlocal.query(PizzaHouse).filter(PizzaHouse.ModeratorId == 1).first().Id
    queryModified = sessionlocal\
        .query(OrderItem)\
        .filter(OrderItem.Order.has(PizzaHouseId = id))\
        .filter(OrderItem.Order.has(Status = 0))\
        .filter(OrderItem.IsModified == True)
    fixedQuery = sessionlocal\
        .query(OrderItem, FixPizza)\
        .filter(OrderItem.PizzaId == FixPizza.Id)\
        .filter(OrderItem.Order.has(PizzaHouseId = id))\
        .filter(OrderItem.Order.has(Status = 0))\
        .filter(OrderItem.IsModified == False)
   
    fixed = [GetOrderViewModel(item, pizza) for item, pizza in fixedQuery]
    modified = [GetOrderViewModel(x) for x in  queryModified ]
    res = fixed + modified
    sessionlocal.close()
    return jsonify(res)

@app.route('/api/settings', methods=['GET'])
def GetSettings():
    sessionlocal = getSession()
    house = sessionlocal.query(PizzaHouse).filter(PizzaHouse.ModeratorId == 1).first()
    sessionlocal.close()
    return jsonify(GetSettingsModel(house))

@app.route('/api/order/accept/<id>', methods=['POST'])
def acceptOrder(id):
    order = session.query(Order).filter(Order.Id == id).first()
    if order.Status == 0:
        order.Status = 1
        session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/order/reject/<id>',  methods=['POST'])
def rejectOrder(id):
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
'''
if __name__ == "__main__":
    app.run()


