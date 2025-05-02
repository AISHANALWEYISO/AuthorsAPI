
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from app.Models.author_model import Author
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db, bcrypt

# Authors blueprint
authors = Blueprint('authors', __name__, url_prefix='/api/v1/authors')


#Retrieving data from database

@authors.get('/')
def getAllauthors():

    try:
        all_authors = Author.query.all()

        authors_data = []
        for author in all_authors:
            author_info = {
                "id":author.id,
                "first_name":author.first_name,
                "last_name":author.last_name,
                "authorname":author.get_full_name(),
                "email":author.email,
                "contact":author.contact,
                "type":author.user_type,
                "created_at":author.created_at,
            }

            authors_data.append(author_info)


        return jsonify({
            'message':"All authors retrieved successfully",
            "authors":authors_data
        }),HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#get user by id
@authors.get('/author/<int:id>')
@jwt_required()
def getauthor(id):

    try:
        author = Author.query.filter_by(id=id).first()

      

        return jsonify({
            "message":"author details retrieved successfully",
            "author":{
                "id":author.id,
                "first_name":author.first_name,
                "last_name":author.last_name,
                "authorname":author.get_full_name(),
                "email":author.email,
                "contact":author.contact,
                "type":author.user_type,
                'biography':author.biography,
                "created_at":author.created_at,
               
            }
        })  ,HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR



#update the user details
@authors.route('/edit/<int:user_id>', methods=["PUT","PATCH"])
@jwt_required()
def updateauthordetails(id):
    try:
        current_author = get_jwt_identity()
        loggedInUser = Author.query.filter_by(id=current_author).first()

        author = Author.query.filter_by(id=id).first()

        if not author:
            return jsonify({"error":"author not found"}), HTTP_404_NOT_FOUND

        elif loggedInUser.author_type!='admin' and author.id!=current_author:
            return jsonify({"error":"You are not authorised to update the author details"})
        
        else:
            first_name = request.get_json().get('first_name',author.first_name)
            last_name = request.get_json().get('last_name',author.last_name)
            email = request.get_json().get('email',author.email)
            contact = request.get_json().get('contact',author.contact)
            password = request.get_json().get('first_name',author.first_name)
            biography = request.get_json().get('biography',author.biography)
            user_type = request.get_json().get('user_type',author.user_type)

            if "password" in request.json:
                hashed_password = bcrypt.generate_password_hash(request.json.get('password'))
                author.password = hashed_password

            author.first_name = first_name
            author.last_name = last_name
            author.email = email
            author.contact = contact
            author.biography = biography
            author.user_type = user_type
            
            db.session.commit()

            author_name
