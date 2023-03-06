from app import db, login 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from flask_login import UserMixin


poke_teams = db.Table("poke_teams", 
                      db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                      db.Column("poke_id", db.Integer, db.ForeignKey('pokemon.id'))
                      )


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    wins = db.Column(db.Integer, default = 0)
    losses = db.Column(db.Integer, default = 0)
    pokemon = db.relationship('Pokemon', backref = 'owner', lazy = 'dynamic')
    #pokemon = db.relationship('Pokemon', secondary = poke_teams, backref = 'poke_teams', lazy = 'dynamic')

    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'
    
    # Human readable repr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def from_dict(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = self.hash_password(data["password"])
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.wins = data["wins"]
        self.losses = data["losses"]

    def add_win(self):
        self.wins += 1
        db.session.commit()

    def add_loss(self):
        self.losses -= 1
        db.session.commit()
    
    def check_pokemon(self, poke_check):
        return poke_check in self.pokemon
    
    def add_pokemon(self, poke_catch):
        self.pokemon.append(poke_catch)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ability = db.Column(db.String(64))
    base_experience = db.Column(db.Integer)
    base_attack = db.Column(db.Integer)
    hp_base = db.Column(db.Integer)
    sprite = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Pokemon {self.name}>'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def from_dict(self, pokemon_dict):
        self.id = pokemon_dict["id"]
        self.name = pokemon_dict["name"]
        self.ability = pokemon_dict["ability"]
        self.base_experience = pokemon_dict["base_experience"]
        self.base_attack = pokemon_dict["base_attack"]
        self.hp_base = pokemon_dict["hp_base"]
        self.sprite = pokemon_dict['sprite']
    
    def check_if_known(name):
        return Pokemon.query.filter_by(name = name).first()
    
