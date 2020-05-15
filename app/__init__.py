from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
from werkzeug.utils import secure_filename

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

mail=Mail()
db=SQLAlchemy()
bootstap=Bootstrap()

photos = UploadSet('photos',IMAGES)
def create_app(config_name):
    #Initializing Application
    app=Flask(__name__)

    # creating the application configurations
    app.config.from_object(config_options[config_name])
    
    # Initializing flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstap.init_app(app)
    mail.init_app(app)
      # configure UploadSet
    configure_uploads(app,photos)

       #main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
        # auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/authenticate')

    
    
    return app