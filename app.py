import os
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import current_app
# from flask import Blueprint

from models.conn import db
from models.model import *

from flask_migrate import Migrate

from flask_login import LoginManager
from flask_login import login_required

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView #nuovo

from routes.api import api as bp_api
from routes.auth import auth as bp_auth
# from routes._admin import admin as bp_admin
from routes.examples import exa as bp_exa


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp_api,  url_prefix='/api')    
app.register_blueprint(bp_auth,  url_prefix='/auth')    
# app.register_blueprint(bp_admin,  url_prefix='/admin')    
app.register_blueprint(bp_exa,  url_prefix='/examples')    

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #L'opzione SQLALCHEMY_TRACK_MODIFICATIONS è una configurazione per Flask-SQLAlchemy che determina se SQLAlchemy deve o meno tenere traccia delle modifiche sugli oggetti per ogni sessione.

db.init_app(app)
migrate = Migrate(app, db)

# nuova classe
class UserProtectedModelView(ModelView):
    # can_view_details = True
    column_exclude_list = ['password_hash', ]
    create_modal = True
    edit_modal = True    
    column_editable_list = ['username', ]
    form_excluded_columns = ['password_hash', 'email']
    can_export = True
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url)) 

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html', 
                           title='My Admin Index View',
                            # name=current_app.config.get('NAME'),
                            # description=current_app.config.get('DESCRIPTION'),
                            # hostname=current_app.config.get('HOSTNAME'),
                            config=current_app.config,
                            map=current_app.url_map
                            )
admin = Admin(app, name='Admin dashboard', template_mode='bootstrap4', index_view=MyAdminIndexView() )
admin.add_view(UserProtectedModelView(User, db.session))

# flask_login user loader block
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    # return User.query.get(int(user_id))
    return user

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
