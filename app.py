import os
from flask import Flask, render_template, jsonify, request, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
# import random
import requests
# from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, UserEditForm, LoginForm, MessageForm
from models import db, connect_db, User, Recipe, Mealplan, Recipe_ingredient, Ingredient

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