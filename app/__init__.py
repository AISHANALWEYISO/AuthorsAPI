from flask import Flask
from app.extensions import db, migrate
from app.controllers.auth.auth_controllers import auth
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity,  jwt_required

# Application factory function
def create_app():
    app = Flask(__name__) #creates the flask instance application
    app.config.from_object('config.Config') #configuration first then db and migrate

    db.init_app(app)  
    migrate.init_app(app,db) 
   

    # importing and Registering models
    from app.Models.author_model import Author
    from app.Models.book_model import Book
    from app.Models.company_model import Company


    #Registering blueprints
    app.register_blueprint(auth)





    #index route

    @app.route('/')
    def index():
        return "Hello world"
    



    return app





