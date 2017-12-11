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
    logUser = db.session.query(User)\
                .filter(sqlalchemy.and_(User.Email == model['userName'], User.PasswordHash == model['password']))\
                .first()
    if logUser is None:
        return "bad request", 400
    roles = db.session.query(UserRole, Role)\
                .filter(logUser.Id == UserRole.UserId)\
                .filter(Role.Id == UserRole.RoleId)\
                .first() 
        
    if(roles is not None and roles[1].Name == 'Moderator') :
        return jsonify({
            'status' : "success",
            'redirect_url' : "views/moderator/ModeratorLayout.html#/" 
        })
    
    return jsonify({
            'status' : "success"
        })

@app.route('/api/Account/Register',methods=['POST'])
def register():
    model = request.form
    modUser = User()
    modUser.Name = model["name"]
    modUser.UserName = model["name"]
    modUser.PasswordHash = model["password"]
    modUser.Email = model["email"]
    modUser.EmailConfirmed = True
    modUser.PhoneNumberConfirmed = True
    modUser.SecurityStamp = "security"
    modUser.TwoFactorEnabled = False
    modUser.LockoutEnabled = False
    modUser.AccessFailedCount = 0
    db.session.add(modUser)
    db.session.commit()
    
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


