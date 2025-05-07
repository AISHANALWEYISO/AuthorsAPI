from flask import Flask
from app.extensions import db, migrate
from app.controllers.auth.auth_controllers import auth
from app.controllers.authors.author_controller import authors
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity,  jwt_required
from flask_jwt_extended import JWTManager
from app.controllers.company.company_controllers import companys
from app.controllers.book.book_controllers import books

# Application factory function
def create_app():
    app = Flask(__name__) #creates the flask instance application
    app.config.from_object('config.Config') #configuration first then db and migrate

    db.init_app(app)  
    migrate.init_app(app,db) 
    jwt = JWTManager(app)


    
    app.config['JWT_SECRET_KEY'] = 'HS256'
    jwt = JWTManager(app)

   

    # importing and Registering models
    from app.Models.author_model import Author
    from app.Models.book_model import Book
    from app.Models.company_model import Company


    #Registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(authors)
    app.register_blueprint(companys)
    app.register_blueprint(books)





    #index route

    @app.route('/')
    def index():
        return "Hello world"
    



    return app





