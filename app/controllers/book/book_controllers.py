from flask import Blueprint, request, jsonify
from app.Models.book_model import Book, db
from app.extensions import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
import validators

# Create a blueprint
book = Blueprint('book', __name__, url_prefix='/api/v1/books')


# Importing status codes
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_201_CREATED,HTTP_500_INTERNAL_SERVER_ERROR

# Define the create book endpoint
@book.route('/register', methods=["POST"])
def create_book():
    try:
        # Extract book data from the request JSON
        data = request.json
        title = data.get("title")
        description = data.get("description")
        price = data.get("price")
        price_unit = data.get("price_unit")
        publication_date = data.get("publication_date")
        isbn = data.get("isbn")
        number_of_pages = data.get("number_of_pages")
        genre = data.get("genre")
        image = data.get("image")
        user_id = get_jwt_identity()
        company_id = data.get("company_id")

        # Validate input data
        if not all([title, description, price, price_unit, publication_date, genre]):
            return jsonify({'error': "All required fields are not provided"}), HTTP_400_BAD_REQUEST

        # Create a new instance of the Book model
        new_book = Book(
            title=title,
            description=description,
            price=price,
            price_unit=price_unit,
            publication_date=publication_date,
            isbn=isbn,
            number_of_pages=number_of_pages,
            genre=genre,
            image=image,
            user_id=user_id,
            company_id=company_id
        )

        # Add the new book instance to the database session
        db.session.add(new_book)

        # Commit the session to save the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': f"Book '{new_book.title}', ID'{new_book.id}' has been created successfully", 
                        'book':{
                            'id':new_book.id,
                            'title': new_book.title,
                            'description': new_book.description,
                            'image': new_book.image,
                            'price': new_book.price,
                            'price_unit': new_book.price_unit,
                            'pages': new_book.number_of_pages,
                            'publication_date': new_book.publication_date,
                            'isbn': new_book.isbn,
                            'genre': new_book.genre,
                            'user_id': new_book.user_id,
                            'company_id': new_book.company_id}

            
            }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    
    

# # Define the get book endpoint
# @book_api.route('/get/<int:book_id>', methods=["GET"])
# def get_book(book_id):
#     try:
#         # querying the book by book_id to get a specific book
#         book = Book.query.get(book_id)
#         if not book:
#             return jsonify({'error': 'Book not found'}), 404

#         return jsonify({'message': 'Book obtained successfully', 'book_id': book_id}), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Define the update book endpoint
# @book_api.route('/edit/<int:book_id>', methods=["PUT"])
# def update_book(book_id):
#     try:
#         # Extract book data from the request JSON
#         data = request.json
#         book = Book.query.get(book_id)
#         if not book:
#             return jsonify({'error': 'Book not found'}), 404

#         # Update book fields if provided in the request
#         for key, value in data.items():
#             setattr(book, key, value)

#         # Commit the session to save the changes to the database
#         db.session.commit()

#         # Return a success response
#         return jsonify({'message': 'Book updated successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# # Define the delete book endpoint
# @book_api.route('/delete/<int:book_id>', methods=["DELETE"])
# @jwt_required()
# def delete_book(book_id):
    
#     try:
#         book_id = Book.query.filter_by(id=id).first()
        
#         if not book_id:
#             return jsonify({'error': 'Book not found'})
#         else:
#             db.session.delete(book_id)
#             db.session.commit()

#         return jsonify({'message': 'Book deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR