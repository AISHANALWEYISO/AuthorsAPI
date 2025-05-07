from flask import Blueprint, request, jsonify
from app.Models.company_model import Company, db
from app.extensions import bcrypt, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_403_FORBIDDEN


# Create a  company blueprint
companys = Blueprint('company', __name__, url_prefix='/api/v1/companies')

# Define the create company endpoint
@companys.route('/create', methods=["POST"])
@jwt_required()
def createcompany():
    try:
        # Extract company data from the request JSON
        data = request.json
        name = data.get("name")
        origin = data.get("origin")
        description = data.get("description")
        author_id = get_jwt_identity()

        # Validating data to avoid data redandancy
        if not name or not origin or not description:
            return jsonify({'error': "All fields are required"}), HTTP_400_BAD_REQUEST

        # Check if company name already exists
        if Company.query.filter_by(name=name).first() is not None:
            return jsonify({'error': 'Company name already exists'}), HTTP_400_BAD_REQUEST

        # Creating a new Company 
        new_company = Company(
            name=name,
            origin=origin,
            description=description,
            authors_id=author_id
        )

        # Adding the new company instance to the database session
        db.session.add(new_company)
        db.session.commit()

        # Return a success response with the newly created company details
        return jsonify({
            'message':  name + " has been created successfully",
            'company': {
                'id': new_company.id,
                'name': new_company.name,
                'origin': new_company.origin,
                'description': new_company.description,
            
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    
#getting all companies

@companys.get('/')
def getAllcompanys():

    try:
        all_companys = Company.query.all()

        companys_data = []
        for company in all_companys:
            company_info = {
                "id":company.id,
                "name":company.name,
                "origin":company.origin,
                "description":company.description,
                "user":{
                "id":company.author.id,
                "first_name":company.author.first_name,
                "last_name":company.author.last_name,
                "authorname":company.author.get_full_name(),
                "email":company.author.email,
                "contact":company.author.contact,
                "type":company.author.user_type,
                'biography':company.author.biography,
                "created_at":company.author.created_at,
                },
                "created_at":company.created_at
            }

            companys_data.append(company_info)


        return jsonify({
                'message':"All companys retrieved successfully",
            "total_companies":len(companys_data),
            "companys":companys_data
        }),  HTTP_200_OK
        
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#get user by id
@companys.get('/company/<int:id>')
@jwt_required()
def getcompany(id):

    try:
        company = Company.query.filter_by(id=id).first()

      

        return jsonify({
            "message":"company details retrieved successfully",
            "company":{
                "id":company.id,
                "name":company.name,
                "origin":company.origin,
                "description":company.description,
                "user":{
                 "id":company.author.id,
                "first_name":company.author.first_name,
                "last_name":company.author.last_name,
                "authorname":company.author.get_full_name(),
                "email":company.author.email,
                "contact":company.author.contact,
                "type":company.author.user_type,
                'biography':company.author.biography,
                "created_at":company.author.created_at
                },
                "created_at":company.created_at,
               
            }
        })  ,HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#updating the company details
@companys.route('/edit/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
def updatecompanydetails(id):
    try:
        current_company = int(get_jwt_identity())
        loggedIncompany = Company.query.filter_by(id=current_company).first()

        company_to_update = Company.query.filter_by(id=id).first()

        if not company_to_update:
            return jsonify({"error": "company not found"}), HTTP_404_NOT_FOUND

        elif company_to_update.id != current_company:
            return jsonify({"error": "You are not authorized to update the company details"}), HTTP_403_FORBIDDEN

        else:
            data = request.get_json()
            name = data.get('name', company_to_update.name)
            origin = data.get('origin', company_to_update.origin)
            description = data.get('description', company_to_update.description)

            company_to_update.name = name
            company_to_update.origin = origin
            company_to_update.description = description

            db.session.commit()

            company_name = company_to_update.get_full_name()
            return jsonify({
                "message": f"{company_name}'s details have been successfully updated",
                "company": {
                    "id": company_to_update.id,
                    "name": company_to_update.name,
                    "origin": company_to_update.origin,
                    "description": company_to_update.description,
                }
            })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR



# Define the delete company endpoint
# @companys.route('/delete/<int:id>', methods=["DELETE"])
# @jwt_required()
# def delete_company(id):
#     try:
#         company = Company.query.get(id)
#         if not company:
#             return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND

#         # Check if the authenticated user has permission to delete the company
#         if company.authors_id != get_jwt_identity():
#             return jsonify({'error': 'Unauthorized to delete this company'}), 

#         # Delete the company from the database
#         db.session.delete(company)
#         db.session.commit()

#         # Return a success response
#         return jsonify({'message': 'Company deleted successfully'}), HTTP_200_OK

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@companys.route('/delete/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_company(id):
    try:
        # Retrieve the company object from the database
        company = Company.query.get(id)
        if not company:
            return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND

        # Check if the authenticated user is the author of the company
        if company.authors_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized to delete this company'}), HTTP_403_FORBIDDEN

        # Delete the company from the database
        db.session.delete(company)
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Company deleted successfully'}), HTTP_200_OK

    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
