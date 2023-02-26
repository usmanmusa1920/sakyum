# -*- coding: utf-8 -*-

from sakyum.utils import Security


secret = Security()
secure_app = secret.passcode_salt
long_comment = "\"\"\""


def pro_init_dummy():
  return f"""from .config import app, db
"""


def pro_config_dummy(proj_name, secure_app=secure_app, long_comment=long_comment):
  return f"""from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask import Flask
from pathlib import Path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db_ORIGIN = Path(__file__).resolve().parent.parent
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = '{secure_app}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+str(db_ORIGIN)+'/default.db'

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.adminLogin'
login_manager.login_message_category = 'info'
login_manager.login_message = u"You must login, in other to get access to that page"


{long_comment} You will need to import models themselves before issuing `db.create_all` {long_comment}
from auth.models import User
# from <app_name>.models import <app_model>
# from <app_name>.admin import QuestionChoiceAdminView
db.create_all() # method to create the tables and database


def admin_runner():
  {long_comment} Model views allow you to add a dedicated set of admin
    pages for managing any model in your database {long_comment}
  admin = Admin(app, name='{proj_name}')


  {long_comment} Register your model, by passing every model that you want
    to manage in admin page in the below list (reg_models) {long_comment}
  reg_models = [
    User,
    # <app_model>,
  ]
  for reg_model in reg_models:
    admin.add_view(ModelView(reg_model, db.session))
    
    
  # admin.add_view(QuestionChoiceAdminView(<app_name_uppercase>QuestionModel, db.session, name="Questions", category="Question-Choice"))
  # admin.add_view(QuestionChoiceAdminView(<app_name_uppercase>ChoiceModel, db.session, name="Choices", category="Question-Choice"))
"""


def pro_routes_dummy(proj):
  return f"""from flask import (render_template, Blueprint)
from sakyum.utils import footer_style, template_dir, static_dir, rem_blueprint
from sakyum.blueprint import default, errors, auth
from flask import render_template
# from <app_name>.views import <app_name>


base = Blueprint("base", __name__, template_folder=template_dir(), static_folder=static_dir("{proj}"))

rem_blue = [default, errors, auth, base]
reg_blueprints = [
  default,
  errors,
  auth,
  base,
  # <app_name>,
]


@default.route('/')
def index():
  # the default_base.html below is located in the sakyum package (templates/default_page) folder
  return render_template("default_base.html", project_name="{proj}", blueprints_list=rem_blueprint(lst_blue=reg_blueprints, rem_blue=rem_blue), footer_style=footer_style)
  
  
{long_comment} overwrite error pages here {long_comment}
"""
