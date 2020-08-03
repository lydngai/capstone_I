from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
bcrypt = Bcrypt()
db = SQLAlchemy()


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

    recipes = db.relationship("Recipes", backref="recipes", secondary= "mealplans", cascade="all, delete")

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
    source_url = db.Column(
        db.Text
    )
    servings = db.Column(db.Integer, nullable=False)
    ready_in_min = db.Column(db.Integer)
    
    ingredients = db.relationship('Ingredient', secondary ='recipe_ingredients', backref='recipes')
    

class Recipe_Ingredient(db.Model):
    """Recipe ingredient set with quantities"""
    
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(db.Integer,  db.ForeignKey("recipes.id"), primary_key=True )

    ingredient_id=db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)

    unit = db.Column(db.Text, nullable = False)
    quantity = db.Column(db.Integer, nullable=False)
    
class Ingredient(db.Model):
    """Ingredients"""
    __tablename__ = 'ingredients'
    id = db.Column(
        db.Integer, primary_key=True
    )
    name = db.Column(
        db.Text,   nullable=False, unique=True,
    )

class Mealplan(db.Model):
    """Planned recipes for user"""
    __tablename__ = 'mealplans'
    id = db.Column(
        db.Integer, primary_key=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), ondelete = "cascade")
    planned_day=db.Column(db.Date)
    meal = db.Column(db.Integer, nullable=False)
    recipe_id=db.Column(db.Integer, db.ForeignKey("recipes.id"), ondelete="cascade")

    
