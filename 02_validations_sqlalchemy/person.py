from sqlalchemy import Column, Integer, String, create_engine, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates

conn = create_engine('sqlite:///validations.db')
Base = declarative_base()
session = sessionmaker(conn)()
Base.metadata.create_all(conn)

class Person(Base):
    __tablename__ = 'person'
    __table_args__ = (CheckConstraint('birth_year < hire_year'),)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    birth_year = Column(Integer, CheckConstraint('birth_year < 2023'))
    hire_year = Column(Integer)

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError(f'Invalid email: {email}')
        return email


