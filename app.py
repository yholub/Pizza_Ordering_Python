"""This module runs the flask program"""
from flask import Flask, render_template, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *
import sqlalchemy

from pizzaOrdering import pizzaOrdering
from orders import orders

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)
app.config["db"] = db

app.register_blueprint(pizzaOrdering)
app.register_blueprint(orders)

@app.route("/")
def main():
    return render_template('layout.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/api/Account/Login',methods=['POST'])
def login():
    model = request.form
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
if __name__ == "__main__":
    app.run()


