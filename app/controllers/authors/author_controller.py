
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN
import validators
from app.Models.author_model import Author
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db, bcrypt
from sqlalchemy import or_

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
@authors.route('/edit/<int:id>', methods=["PUT","PATCH"])
@jwt_required()
def updateauthordetails(id):
    try:
        current_author = get_jwt_identity()
        loggedInUser = Author.query.filter_by(id=current_author).first()

        author = Author.query.filter_by(id=id).first()

        if not author:
            return jsonify({"error":"author not found"}), HTTP_404_NOT_FOUND

        elif author.id!=current_author:
            return jsonify({"error":"You are not authorised to update the author details"}),HTTP_403_FORBIDDEN
        
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

            author_name = author.get_full_name()
            return jsonify({
                 "message":author_name + "'s details have been successfully updated",
                 "author":{
                     "id":author.id,
                     "first_name":author.first_name,
                "last_name":author.last_name,
                "email":author.email,
                "contact":author.contact,
                "type":author.user_type,
                'biography':author.biography,
                "update_at":author.updated_at,
                     
                 }
             })
        
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#delete the author
@authors.route('/delete/<int:id>', methods=["DELETE"])
@jwt_required()
def Deleteauthordetails(id):
     
     try:
        current_author = get_jwt_identity()
        loggedInUser = Author.query.filter_by(id=current_author).first()

        author = Author.query.filter_by(id=id).first()

        if not author:
            return jsonify({"error":"author not found"}), HTTP_404_NOT_FOUND

        elif author.id!= current_author:
            return jsonify({"error":"You are not authorised to update the author details"}),HTTP_403_FORBIDDEN
        
        else:

            #deleting associated companys
            for company in author.companys:
                db.session.delete(company)

            #deleting associated companys
            for book in author.books:
                db.session.delete(book)
    
            db.session.delete(author)
            db.session.commit()

            
            return jsonify({
                 "message": "author deleted successfully",
              
             })
        
     except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#searching an author

@authors.get('/search')
@jwt_required()
def searchAuthors():

    try:

        search_query = request.args.get('query','')

        authors = Author.query.filter(
    or_(
        Author.first_name.ilike(f"%{search_query}%"),
        Author.last_name.ilike(f"%{search_query}%")
    ),
    Author.user_type == 'author'
).all()
        
        if len(authors) == 0:
            return jsonify({
                "message" : "no results found"
            }),HTTP_404_NOT_FOUND
        else:


          authors_data = []

        for author in authors:
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
            'message':f"Authors with name {search_query} retrieved successfully",
            "total_search":len(authors_data),
            "search_results":authors_data
        }),HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
