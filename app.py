import os
from flask import Flask, render_template, jsonify, request, redirect, session, g, abort, flash
from flask_debugtoolbar import DebugToolbarExtension
# from flask_bootstrap import Bootstrap
# import random
import requests
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserSignInForm, UserEditForm

from models import db, connect_db, User, Recipe, Recipe_ingredient, Ingredient, Mealplan

import requests
from config import apikey

app = Flask(__name__)

# Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mealplanner'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

API_BASE_URL=f"https://api.spoonacular.com/"
CURR_USER='curr_user'
allergens=["Dairy","Egg","Gluten","Grain","Peanut","Seafood","Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"]
# setup is going to be lengthy...   

###################

# set up routes to get recipes 
@app.route('/')
def show_landing_page():
    """show landing page"""
    return render_template("home-anon.html")

@app.route('/advanced_search')
def show_advanced_search():
    """show advanced search form"""
    diets = ["","glutenfree","ketogenic",'vegetarian','lacto-vegetarian','ovo-vegetarian','vegan','pescetarian','paleo','whole30']

    return render_template("recipe-search.html",intolerances=allergens, diets=diets)

@app.route('/adv_search_results')
def adv_search_query():
    """perform advanced search from advanced search form"""
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

    return render_template("recipe-results.html",resp=response)    


@app.route('/search')
def search_query():
    """perform basic search from search bar"""
    search = request.args.get('search-bar-recipe')
    res = requests.get(f"{API_BASE_URL}/recipes/complexSearch?query={search}&number=5&apiKey={apikey}")

    response = res.json()

    return render_template("recipe-results.html",resp=response)

@app.route('/recipe/<int:id>')
def show_recipe_info(id):
    """display detailed recipe information"""

    res = requests.get(f"{API_BASE_URL}/recipes/{id}/information?apiKey={apikey}")
    response =res.json()

    return render_template("recipe-info.html",recipe=response)

###########################
### ### User Routes ### ###
###########################
    # import pdb
    # pdb.set_trace()
# warbler l.247 edit/delete
# warbler
@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""

    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])

    else:
        g.user = None


def log_in(user):
    """logs in user by adding to session"""
    session[CURR_USER] = user.id

def log_out():
    """log out user"""
    if session[CURR_USER]:
        del session[CURR_USER]

@app.route('/user/signup', methods=['GET','POST'])
def signup():
    """Handle user signup. Create user and add to DB. Redirect to homepage. If form not valid, present form. If user already exists, present form"""
    if CURR_USER in session:
        del session[CURR_USER]

    form=UserAddForm()

    if form.validate_on_submit():
        try:
            user=User.signup(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                cooking_for=form.cooking_for.data,
                allergies=form.allergies.data
            )
            db.session.commit()
            log_in(user)
            flash(f"Welcome {form.name.data}!",'success')

        except IntegrityError as e:
            flash("Email already registered",'danger')
            return render_template('signup.html', form=form)
    
    return render_template('user/signup.html', form=form)

@app.route('/user/logout')
def log_out_user():
    log_out()
    flash("You have successfully logged out.", 'success')
    return redirect("/")

@app.route('/user/login', methods=['GET','POST'])
def log_in_user():
    
    form=UserSignInForm()

    if form.validate_on_submit():
        user = User.authenticate(email=form.email.data, password=form.password.data)
        if user:
            log_in(user)
            flash(f"Welcome back {user.name}", 'success')
        
        else:
            flash("Invalid credentials",'danger')
    
    return render_template("user/login.html", form=form)

@app.route('/user/profile')
def show_user():
    if not g.user:
        flash("Unauthorized access",'danger')
        return redirect('/')
    
    user=g.user

    return render_template("user/profile.html", user=user)


@app.route('/user/edit', methods=['GET','POST'])
def edit_user_profile():
    if not g.user:
        flash("Unauthorized access",'danger')
        return redirect('/')
    
    user=g.user
    form=UserEditForm(obj=user)

    if form.validate_on_submit():
        user.name=form.name.data
        user.cooking_for=form.cooking_for.data
        user.allergies = form.allergies.data
        
        db.session.commit()
        flash("Profile updated successfully!",'success')
    return render_template('user/edit-user.html',form=form)

@app.route('/user/delete', methods=['GET','POST'])
def delete_user_profile():
    if not g.user:
        flash("Unauthorized access",'danger')
        return redirect('/')
    
    user=g.user
    form=UserSignInForm()

    if form.validate_on_submit():
        user = User.authenticate(email=form.email.data, password=form.password.data)
        if user:
            db.session.delete(user)
            db.session.commit()
            log_out()
            flash(f"Account deleted", 'success')

        else:
            flash("Invalid credentials",'danger')

    return render_template('user/delete-user.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    """Set the 404 status explicitly"""
    return render_template('404.html'), 404