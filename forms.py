from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class NewMealForm(FlaskForm):
    vegetarian = SelectField("Vegetariánské", choices=[("Ne", "Ne"), ("Ano", "Ano")])
    name = StringField("Název jídla", validators=[DataRequired()])
    meat = SelectField("Druh masa", choices=[("Kuřecí", "Kuřecí"), ("Vepřové", "Vepřové"), ("Hovězí", "Hovězí")])
    submit = SubmitField("Uložit")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Heslo", validators=[DataRequired()])
    login = SubmitField("Přihlásit se")


class RegisterForm(FlaskForm):
    username = StringField("Přezdívka", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Heslo", validators=[DataRequired()])
    register = SubmitField("Registrovat se")
