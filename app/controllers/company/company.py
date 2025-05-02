from flask import Blueprint, request, jsonify
from app.Models.company_model import Company, db
from app.extensions import bcrypt, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK

# Create a blueprint
company_api = Blueprint('company_api', __name__, url_prefix='/api/v1/companies')

# Define the create company endpoint
@company_api.route('/register', methods=["POST"])
@jwt_required()
def create_company():
    try:
        # Extract company data from the request JSON
        data = request.json
        name = data.get("name")
        origin = data.get("origin")
        description = data.get("description")
        user_id = get_jwt_identity()

        # Validate input data
        if not all([name, origin, description]):
            return jsonify({'error': "All fields are required"}), HTTP_400_BAD_REQUEST

        # Check if company name already exists
        if Company.query.filter_by(name=name).first():
            return jsonify({'error': 'Company name already exists'}), HTTP_400_BAD_REQUEST

        # Creating a new instance of the Company model
        new_company = Company(
            name=name,
            origin=origin,
            description=description,
            user_id=user_id
        )

        # Adding the new company instance to the database session
        db.session.add(new_company)
        db.session.commit()

        # Return a success response with the newly created company details
        return jsonify({
            'message': f"Company '{new_company.name}' has been successfully added",
            'company': {
                'id': new_company.id,
                'name': new_company.name,
                'origin': new_company.origin,
                'description': new_company.description,
                'user_id': new_company.user_id
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Define the get company endpoint
@company_api.route('/get/<int:company_id>', methods=["GET"])
@jwt_required()
def get_company(company_id):
    try:
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND

        # Return the company details
        return jsonify({
            'message': 'Company obtained successfully',
            'company': {
                'id': company.id,
                'name': company.name,
                'origin': company.origin,
                'description': company.description,
                'user_id': company.user_id
            }
        }), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Define the update company endpoint
@company_api.route('/edit/<int:company_id>', methods=["PUT"])
@jwt_required()
def update_company(company_id):
    try:
        # Extract company data from the request JSON
        data = request.json
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND

        # Update company fields based on provided data
        for key, value in data.items():
            setattr(company, key, value)

        # Commit the session to save the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Company updated successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Define the delete company endpoint
@company_api.route('/delete/<int:company_id>', methods=["DELETE"])
@jwt_required()
def delete_company(company_id):
    try:
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), HTTP_404_NOT_FOUND

        # Check if the authenticated user has permission to delete the company
        if company.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized to delete this company'}), 

        # Delete the company from the database
        db.session.delete(company)
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Company deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR