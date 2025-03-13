
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from app.Models.author_model import Author
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required

# Auth blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')




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
                access_token = create_access_token(identity=author.id)
                refresh_token = create_refresh_token(identity=author.id)

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

