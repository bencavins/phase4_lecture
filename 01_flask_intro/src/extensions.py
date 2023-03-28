from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()
bcrypt = Bcrypt()
db = SQLAlchemy()