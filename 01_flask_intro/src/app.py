from flask import Flask, jsonify, render_template, request, make_response, session as browser_session
from models import db, Owner, Pet, User
from flask_cors import CORS

# from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt

from extentions import *

import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


def create_app():
    app = Flask(__name__)
    register_extensions(app)

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)


EXCLUDED_ENDPOINTS = ['login', 'root', 'signup']
@app.before_request
def check_authorized():
    print(request.endpoint)
    if request.endpoint not in EXCLUDED_ENDPOINTS:
        if not browser_session.get('user_id'):
            return jsonify({'error': 'not authorized'}), 401

@app.route('/')
def root():
    user_id = browser_session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    return render_template('index.html', username=user.username if user else None)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter(User.username == username).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404
    
    browser_session['user_id'] = user.id
    return jsonify(user.to_dict()), 200

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(username=data.get('username'))
        new_user.password_hash = data.get('password')
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

@app.route('/logout', methods=['DELETE'])
def logout():
    browser_session.pop('user_id')
    return jsonify({}), 204

@app.route('/authorized')
def check_session():
    user_id = browser_session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return jsonify({'error': 'not authorized'}), 401
    
    return jsonify(user.to_dict()), 200

@app.route('/message/<my_message>')
def message(my_message):
    return render_template('message.html', message=my_message)

@app.route('/owners/<name>')
def get_owner_by_name(name):
    owner = Owner.query.filter(Owner.name == name).first()
    resp_body = f'<h1>Owner: {name}</h1>'

    if not owner:
        return make_response(
            '<h1>404 Owner not found</h1>',
            404
        )
    
    for pet in owner.pets:
        resp_body += f'<h2>Pet {pet.name}, ({pet.species})</h2>'
    
    return make_response(resp_body, 200)


@app.route('/pets/<int:pet_id>')
def get_pet(pet_id):
    pet = Pet.query.filter(Pet.id == pet_id).first()

    if not pet:
        return make_response(
            '<h1>404 Pet not found :(</h1>'
        )

    return make_response(
        f'<h1>Pet: {pet.name} ({pet.species})</h1>',
        200
    )

@app.route('/api/pets', methods=['GET', 'POST'])
def get_all_pets():
    if browser_session.get('read_count') is None:
        browser_session['read_count'] = 0

    print(f"read count = {browser_session['read_count']}")
    
    if browser_session['read_count'] >= 3:
        return make_response('<h1>Limit reached</h1>', 401)
    
    browser_session['read_count'] += 1

    if request.method == 'GET':
        pets = Pet.query.all()
        pets_dict = [pet.to_dict() for pet in pets]
        return make_response(jsonify(pets_dict), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_pet = Pet()

        # update new_pet with data from json
        for field in data:
            # new_pet.field = 'fido'  #this does not work!
            setattr(new_pet, field, data[field])
        db.session.add(new_pet)
        db.session.commit()
        return make_response(jsonify(new_pet.to_dict()), 201)

@app.route('/api/pets/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def get_pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        error = {'error': 'could not find pet'}
        return make_response(jsonify(error), 404)
    
    if request.method == 'GET':
        return make_response(jsonify(pet.to_dict()), 200)

    elif request.method == 'DELETE':
        db.session.delete(pet)
        db.session.commit()
        return make_response(jsonify({'status': 'delete success'}), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        for field in data:
            setattr(pet, field, data[field])
        db.session.add(pet)
        db.session.commit()
        return make_response(jsonify(pet.to_dict()), 200)

@app.route('/api/owners/<int:id>')
def get_owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        error = {'error': 'could not find owner'}
        return make_response(jsonify(error), 404)
    
    return make_response(jsonify(owner.to_dict()), 200)


@app.route('/api/owners')
def get_all_owners():
    owners = Owner.query.all()
    data = [owner.to_dict() for owner in owners]
    return make_response(jsonify(data), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True, ssl_context=('cert.pem', 'key.pem'))
