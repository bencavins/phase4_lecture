from models import db, Owner, Pet, User
from faker import Faker
import random
from app import app

fake = Faker()


if __name__ == '__main__':

    # db.create_all()

    with app.app_context():
        Pet.query.delete()
        Owner.query.delete()
        User.query.delete()

        owners = []
        for x in range(10):
            owner = Owner(name=fake.name())
            owners.append(owner)
        db.session.add_all(owners)

        pets = []
        species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
        for x in range(30):
            pet = Pet(
                name=fake.first_name(), 
                species=random.choice(species),
                owner=random.choice(owners)
            )
            pets.append(pet)
        db.session.add_all(pets)

        users = []
        for _ in range(5):
            user = User(
                name=fake.first_name(),
                email=fake.email()
            )
            users.append(user)

        db.session.add_all(users)

        db.session.commit()