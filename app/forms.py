from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional

from app.models import User

class RegistrationForm(FlaskForm):
    """Formulaire d'inscription"""
    username = StringField('Nom d\'utilisateur', 
                           validators=[DataRequired()])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', 
                             validators=[DataRequired()])
    password2 = PasswordField('Confirmez le mot de passe', 
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    # Vérifie si le nom d'utilisateur n'est pas déjà pris
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    # Vérifie si l'email n'est pas déjà pris
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', 
                             validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class TaskForm(FlaskForm):
    """Formulaire pour ajouter une nouvelle tâche"""
    title = StringField('Titre de la tâche', validators=[DataRequired()])
    description = TextAreaField('Description (optionnel)', validators=[Optional()])
    submit = SubmitField('Ajouter la tâche')