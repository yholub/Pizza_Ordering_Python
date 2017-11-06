from flask import Flask, Blueprint, render_template, json, request

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

@app.route('/signUp',methods=['POST'])
def signUp():
    return json.dumps(models.session.query(FixPizza).order_by(FixPizza.Id))
 
    # read the posted values from the UI
    #_name = request.form['inputName']
    #_email = request.form['inputEmail']
    #_password = request.form['inputPassword']
 
    # validate the received values
    #if _name and _email and _password:
    #    return json.dumps({'html':'<span>All fields good !!</span>'})
    #else:
    #    return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()


