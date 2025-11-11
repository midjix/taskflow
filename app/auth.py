from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm # <-- On importe nos formulaires

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Si l'utilisateur est déjà connecté, on le redirige
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    # C'est ici qu'on "décommente" la logique
    if form.validate_on_submit():
        # Hasher le mot de passe
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Votre compte a été créé ! Vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Inscription', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    
    # On "décommente" la logique de connexion
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # On vérifie si l'utilisateur existe ET si le mot de passe est correct
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            # Gère la redirection si l'utilisateur essayait d'accéder à une page protégée
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
            
    return render_template('login.html', title='Connexion', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))