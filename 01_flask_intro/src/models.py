from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    pets = db.relationship('Pet', backref='owner')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pets': [pet.to_dict() for pet in self.pets]
        }

    def __repr__(self) -> str:
        return f"<Owner name={self.name}>"


class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species
        }

    def __repr__(self) -> str:
        return f"<Pet name={self.name}, species={self.species}>"
