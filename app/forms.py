from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo

class UserCreationForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    email = StringField("Email", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    submit = SubmitField()

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    email = StringField("Email", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class ProductForm(FlaskForm):
    product_name = StringField("Title", validators= [DataRequired()])
    price = StringField("Price", validators= [DataRequired()])
    img_file = FileField("Upload File", validators= [DataRequired()])
    description = StringField("Description", validators= [])

    submit = SubmitField()