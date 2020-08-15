from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Add new user form"""
    name=StringField('Name', validators=[DataRequired()])
    email=StringField('E-mail', validators=[DataRequired()])
    
    password=PasswordField('Password',validators=[DataRequired(), Length(min=6)])
    cooking_for=IntegerField('Cooking for', default=1)
    allergies=StringField("Allergens/Intolerances")
    # allergies=SelectField('Allergens/Intolerances',choices=[("dairy", "Dairy"),("egg",'Egg'),('gluten',"Gluten"),('grain',"Grain"),('peanut',"Peanut"),('seafood',"Seafood"),('sesame',"Sesame"),('shellfish',"Shellfish"),('soy',"Soy"),('sulfite',"Sulfite"),('tree nut',"Tree Nut"),('wheat',"Wheat")], validate_choice=False)
    # allergies = db.Column(db.Text)

class UserSignInForm(FlaskForm):
    """Sign in user form"""
    
    email=StringField('E-mail', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(), Length(min=6)])

class UserEditForm(FlaskForm):
    """Edit user form"""
    name=StringField('Name', validators=[DataRequired()])
    
    cooking_for=IntegerField('Cooking for', default=1)
    allergies=StringField("Allergens/Intolerances")

class RecipeNoteForm(FlaskForm):
    """Save user's notes for a recipe"""
    notes=TextAreaField('Notes', validators=[DataRequired()])
    
    # cooking_for=IntegerField('Cooking for', default=1)
    # allergies=StringField("Allergens/Intolerances")