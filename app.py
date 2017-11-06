from flask import Flask, render_template, json, request

app = Flask(__name__, static_url_path='')
import sqlalchemy
from sqlalchemy import create_engine
from models import *

models = __import__("models")

@app.route("/")
def main():
    fixPizzas = []
    for instance in models.session.query(FixPizza).order_by(FixPizza.Id):
        fixPizzas.append(instance)
    return render_template('layout.html')

@app.route("/home")
def home():
    return render_template('home.html')

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

