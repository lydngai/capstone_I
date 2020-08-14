from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app. Called in app.py
    """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User profile"""
    __tablename__ = 'users'

    id = db.Column(
        db.Integer, primary_key=True )
    
    email = db.Column(
        db.Text,   nullable=False, unique=True )

    name = db.Column(
        db.Text,   nullable=False)

    password = db.Column(
        db.Text,   nullable=False)

    cooking_for = db.Column(
        db.Integer,   nullable=False, default = 1 )
    
    allergies = db.Column(db.Text)

    recipes = db.relationship("Recipe", backref="recipes", secondary= "user_recipes")
    recipe_notes = db.relationship("User_Recipe", backref="user_recipes",cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User #{self.id}: {self.email}, {self.name}>"  

    @classmethod
    def signup(cls, name, email, password, cooking_for,allergies):
        """Sign up user.
        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            name=name,
            email=email,
            password=hashed_pwd,
            cooking_for=cooking_for,
            allergies=allergies
        )
        db.session.add(user)
        
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Recipe(db.Model):
    """Recipe instance """
    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer, primary_key=True
    )
    name = db.Column(
        db.Text, nullable=False
    )
    image_url = db.Column(
        db.Text, default="https://f0.pngfuel.com/png/312/993/bowl-with-stick-sticker-beer-vegetarian-cuisine-hamburger-japanese-cuisine-food-food-icon-png-clip-art.png"
    )
    source_url = db.Column(db.Text)
    servings = db.Column(db.Integer)
    ready_in_minutes = db.Column(db.Integer)

    
    def __repr__(self):
        return f"<Recipe #{self.id}: {self.name}>"  


class User_Recipe(db.Model):
    """Planned recipes for user"""
    __tablename__ = 'user_recipes'
    id = db.Column(
        db.Integer, primary_key=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    recipe_id=db.Column(db.Integer, db.ForeignKey("recipes.id"))

    notes = db.Column(db.Text)
    

# class Ingredient(db.Model):
#     """Ingredients"""
#     __tablename__ = 'ingredients'
#     id = db.Column(
#         db.Integer, primary_key=True
#     )
#     name = db.Column(
#         db.Text,   nullable=False, unique=True,
#     )
#     ## create method to parse and add missing ingredients?

# class Recipe_ingredient(db.Model):
#     """Recipe ingredient set with quantities"""
    
#     __tablename__ = 'recipe_ingredients'
#     id = db.Column(
#         db.Integer, primary_key=True
#     )

#     recipe_id = db.Column(db.Integer,  db.ForeignKey("recipes.id"))

#     ingredient_id=db.Column(db.Integer, db.ForeignKey("ingredients.id"))

#     unit = db.Column(db.Text, nullable = False)
#     quantity = db.Column(db.Integer, nullable=False)

    ## create method to parse and add recipe_ingredient?
    

