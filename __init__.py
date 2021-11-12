from flask import Flask,request,render_template
import pandas as pd


from .models import db
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__, static_url_path = '/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/app"
app.secret_key = b'Gw\x16\xbd^x\xb6]\xe2\xc4:g+mk\xe1'

migrate = Migrate(app, db)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User
@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))



 # blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .synapsis import synapsis as synapsis_blueprint
app.register_blueprint(synapsis_blueprint)

from .neural import neural as neural_blueprint
app.register_blueprint(neural_blueprint)
      
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
