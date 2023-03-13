from flask import Flask, render_template, request, make_response
from models import db, Owner, Pet
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def root():
    print(request.headers)
    return render_template('index.html')

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
def get_pet_by_id(pet_id):
    pet = Pet.query.filter(Pet.id == pet_id).first()

    if not pet:
        return make_response(
            '<h1>404 Pet not found :(</h1>'
        )

    return make_response(
        f'<h1>Pet: {pet.name} ({pet.species})</h1>',
        200
    )


if __name__ == '__main__':
    app.run(port=5555, debug=True)
