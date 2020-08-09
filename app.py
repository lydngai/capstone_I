import os
from flask import Flask, render_template, jsonify, request, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
# import random
import requests
# from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, UserEditForm, LoginForm, MessageForm
from models import db, connect_db, User, Recipe, Recipe_ingredient, Ingredient, Mealplan
from config import apikey


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mealplanner'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# setup is going to be lengthy...   

###################
# seed code for starting up
#
# db.drop_all()
# db.create_all()
# u = User(name="lu", email="lu@gmail.com", password='asdf')
# rec = Recipe(name="brownies",source_url="https://smittenkitchen.com/", servings=12, ready_in_min=45)
# ing= Ingredient(name="chocolate")
# ing1= Ingredient(name="flour")
# ing2= Ingredient(name="butter")
# ing3= Ingredient(name="eggs")
# db.session.add_all([u,rec,ing,ing1,ing2,ing3])
# db.session.commit()
# mp = Mealplan(user_id=1, planned_day="2020-08-16", recipe_id=1,meal=4)


##############
# set up routes to get recipes 
@app.route('/')
def show_landing_page():
    return render_template("home-anon.html")

@app.route('/advanced_search')
def show_advanced_search():
    allergens=["Dairy","Egg","Gluten","Grain","Peanut","Seafood","Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
    diets = ["glutenfree","ketogenic",'vegetarian','lacto-vegetarian','ovo-vegetarian','vegan','pescetarian','paleo','whole30']
    return render_template("recipe-search.html",intolerances=allergens, diets=diets)


