from extensions import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

# db = SQLAlchemy()
# from app import bcrypt

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
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
