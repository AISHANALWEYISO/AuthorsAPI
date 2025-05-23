
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from app.Models.author_model import Author
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required

# Auth blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


#User registration

@auth.route('/register' , methods=['POST'])
def register_author():
    #Storing request values
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    user_type = data.get('user_type')
    password = data.get('password')
    biography = data.get('biography', '') 

#Validations of the incoming request.
    if not first_name or not last_name or not contact or not password or not email:
        return({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    
    if not biography:
        return({"error": 'Enter your author biography'}),HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return({"error":'The password is too short'}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return({"error":"Email is not valid"}),HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first() is not None:
        return({"error":"Email address in use"}),HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return({"error":"Number is already in use"}),HTTP_409_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash(password)# Hashing the password

        #Creating the user
        new_author = Author(first_name=first_name,last_name=last_name,password=hashed_password,email=email,contact=contact,biography=biography,user_type=user_type)
        db.session.add(new_author)
        db.session.commit()
        #User name
        authorname = new_author.get_full_name()

        return({
            'message': authorname + " has succesfully created as an " + new_author.user_type,
            'author':{
                "id":new_author.id,
                "first_name":new_author.first_name,
                "last_name":new_author.last_name,
                "email":new_author.email,
                "contact":new_author.contact,
                "biography":new_author.biography,
                "created_at":new_author.created_at,

            }
        }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify ({"error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
# User login
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        if not password or not email:
            return jsonify({'Message': "Email and password are required"}), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email=email).first()

        if author:
            is_correct_password = bcrypt.check_password_hash(author.password, password)

            if is_correct_password:
                access_token = create_access_token(identity=str(author.id))
                refresh_token = create_refresh_token(identity=str(author.id))

                return jsonify({
                    'user': {
                        'id': author.id,
                        'authorname': author.get_full_name(),
                        'email': author.email,
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    },
                    'message': "You have successfully logged into your account."
                }), HTTP_200_OK
            else:
                return jsonify({'Message': "Invalid password"}), HTTP_401_UNAUTHORIZED

        else:
            return jsonify({'Message': "Invalid email address"}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# We are using the `refresh=True` options in jwt_required to only allow refresh tokens to access this route.
@auth.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=str(identity))
    return jsonify({'access_token': access_token})

