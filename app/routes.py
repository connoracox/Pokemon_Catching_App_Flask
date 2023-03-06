from flask import render_template, flash, redirect, request
from app import app 
from app.forms import RegisterForm, SignInForm, SearchPokemon
from app.models import User, Pokemon
from flask_login import login_user, logout_user, login_required
import requests 


@app.route('/')
@login_required 
def index():
    cdn= {
        'humans': ('connor'),
        'pokemon': ['charizard', 'pikachu', 'bulbasaur']
    }
    return render_template('index.jinja', cdn=cdn, title='Home')

@app.route('/about')
def about():
    return render_template('about.jinja')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username= form.username.data
        email= form.email.data
        password= form.password.data
        first_name= form.first_name.data
        last_name= form.last_name.data
        u = User(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
        user_match = User.query.filter_by(username=username).first()
        email_match = User.query.filter_by(email=email).first()
        if user_match:
            flash(f'Username {username} already exists. Try again!')
            return redirect('/register')
        elif email_match:
            flash(f'Email {email} already exists. Try again!')
            return redirect('/register')
        else:
            u.commit()
            flash(f'Request to register {username} successful.')
            return redirect('/')
    return render_template('register.jinja', register_form=form)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_match = User.query.filter_by(username=username).first()
        password_match = User.query.filter_by(password=password).first()
        if not user_match or not password_match:
            flash(f'Username and/or Password was incorrect. Try again!')
            return redirect('/log_in')
        flash(f'{username} successfully signed in!')
        login_user(user_match, remember=form.remember_me.data)
        return redirect('/')
    return render_template('sign_in.jinja', sign_in_form=form)

@app.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect('/')

@app.route('/user/<username>')
def user(username):
    user_match = User.query.filter_by(username=username).first()
    if not user_match:
        return redirect('/')
    pokemon = user_match.pokemon
    return render_template('your_pokemon.jinja', user=user_match, pokemon=pokemon)

@app.route('/your_pokemon')
@login_required
def your_pokemon():
    return render_template('your_pokemon.jinja')

@app.route('/search_pokemon', methods=['GET', 'POST'])
@login_required 
def search():
    form = SearchPokemon()
    if request.method == 'POST':
        name = form.name.data.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
        response = requests.get(url)
        if not response.ok:
            flash("Pokemon does not exist")
            return redirect('/search_pokemon')
        data = response.json()
        for pokemon in data:
            pokemon_dict = {}
            pokemon_dict = {
                "id": data['id'], 
                "name": data['name'].title(),
                "ability":data['abilities'][0]["ability"]["name"],
                "base_experience":data['base_experience'],
                "base_attack": data['stats'][1]['base_stat'],
                "hp_base":data['stats'][0]['base_stat'],
                "sprite":data['sprites']['other']['home']["front_default"]                                             
            }

            if not Pokemon.check_if_known(pokemon_dict['name']):
                pokemon = Pokemon()
                pokemon.from_dict(pokemon_dict)
                pokemon.commit()
                return redirect('/your_pokemon')
    return render_template('search_pokemon.jinja', search_pokemon=form)