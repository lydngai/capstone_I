import os
from flask import Flask, render_template, jsonify, request, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
# import random
import requests
# from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, UserEditForm, LoginForm, MessageForm
from models import db, connect_db, User, Recipe, Recipe_ingredient, Ingredient, Mealplan

import requests
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

API_BASE_URL=f"https://api.spoonacular.com/"
allergens=["Dairy","Egg","Gluten","Grain","Peanut","Seafood","Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
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

    diets = ["","glutenfree","ketogenic",'vegetarian','lacto-vegetarian','ovo-vegetarian','vegan','pescetarian','paleo','whole30']

    return render_template("recipe-search.html",intolerances=allergens, diets=diets)

@app.route('/adv_search_results')
def adv_search_query():
    intolerances=[]

    query=request.args.get('advQuery')
    inc_ing=request.args.get('includeIngredients')
    exc_ing=request.args.get('excludeIngredients')
    cooktime=request.args.get('cooktime')
    diet=request.args.get('diet')
    
    # intolerances=request.args.get('intolerances')
    for item in allergens:
        if request.args.get(f"{item}"):
            intolerances.append(item)

    payload={'query': query}
    
    
    if inc_ing:
        payload["includeIngredients"]=inc_ing
    if exc_ing:
        payload['excludeIngredients']=exc_ing
    if cooktime:
        payload['maxReadyTime']=cooktime
    if intolerances:
        payload['intolerances']=intolerances
    if diet:
        payload['diet']=diet

    res = requests.get(f"{API_BASE_URL}/recipes/complexSearch?query={query}&number=5&apiKey={apikey}",params=payload)

    response = res.json()
    
    # import pdb
    # pdb.set_trace()

    return render_template("recipe-results.html",resp=response)    


@app.route('/search')
def search_query():
    search = request.args.get('search-bar-recipe')
    res = requests.get(f"{API_BASE_URL}/recipes/complexSearch?query={search}&number=5&apiKey={apikey}")

    response = res.json()

    return render_template("recipe-results.html",resp=response)


    # intolerances, include ingredients, exclude ingredients,
    # diet
    # https://api.spoonacular.com/recipes/complexSearch?query=<string>&cuisine=<string>&excludeCuisine=<string>&diet=<string>&intolerances=<string>&equipment=<string>&includeIngredients=<string>&excludeIngredients=<string>&type=<string>&instructionsRequired=<boolean>&fillIngredients=<boolean>&addRecipeInformation=<boolean>&addRecipeNutrition=<boolean>&author=<string>&tags=<string>&recipeBoxId=<number>&titleMatch=<string>&maxReadyTime=<number>&ignorePantry=true&sort=<string>&sortDirection=<string>&minCarbs=<number>&maxCarbs=<number>&&offset=<number>&number=<number>

    #if __ not none, append to search query

@app.route('/recipe/<int:id>')
def show_recipe_info(id):
    res = requests.get(f"{API_BASE_URL}/recipes/{id}/information?apiKey={apikey}")
    response =res.json()

    return render_template("recipe-info.html",recipe=response)