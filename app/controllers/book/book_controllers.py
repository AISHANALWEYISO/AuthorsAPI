from flask import Blueprint, request, jsonify
from app.Models.book_model import Book, db
from app.extensions import bcrypt, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_403_FORBIDDEN


# Create a  book blueprint
books = Blueprint('book', __name__, url_prefix='/api/v1/books')

# Define the create book endpoint
@books.route('/create', methods=["POST"])
@jwt_required()
def createbook():
    try:
        # Extract book data from the request JSON
        data = request.get_json()
        title = data.get("title")
        price = data.get("price")
        price_unit = data.get("price_unit")
        description = data.get("description")
        generation = data.get("generation")
        other_books = data.get("other_books")
        number_of_pages = data.get("number_of_pages")
        publication_date = data.get("publication_date")
        company_id = data.get("company_id")
        author_id = get_jwt_identity()
        writer = data.get("writer")


        # Validating data to avoid data redandancy
        if not title or not other_books or not price_unit or not generation or not publication_date or not company_id or not price or not number_of_pages or not writer:
            return jsonify({'error': "All fields are required"}), HTTP_400_BAD_REQUEST

        # Check if book name already exists
        if Book.query.filter_by(title=title, author_id=author_id).first() is not None:
            return jsonify({'error': 'book with this title and author id already exists'}), HTTP_400_BAD_REQUEST
        
        # if Book.query.filter_by(generation=generation).first() is not None:
        #     return jsonify({'error': 'book generation already exists'}), HTTP_400_BAD_REQUEST
        
        # Creating a new book
        new_book = Book(
            title=title,
            description=description,
            number_of_pages=number_of_pages,
            price_unit=price_unit,
            price=price,
            generation=generation,
            author_id=author_id,
            company_id=company_id,
            publication_date=publication_date
        )
        
            

        # Adding the new book instance to the database session
        db.session.add(new_book)
        db.session.commit()

        # Return a success response with the newly created book details
        return jsonify({
            'message':  title + " has been created successfully",
            'book': {
                "id":new_book.id,
                'title':new_book.title,
            'description':new_book.description,
            'number_of_pages':new_book.number_of_pages,
            'price_unit':new_book.price_unit,
            'price':new_book.price,
            'generation':new_book.generation,
            'publication_date':new_book.publication_date,
            "company":{
                       
                'id': new_book.company.id,
                'name': new_book.company.name,
                'origin': new_book.company.origin,
                'description': new_book.company.description,
            },

            "author":{
                 "first_name":new_book.author.first_name,
                "last_name":new_book.author.last_name,
                "authorname":new_book.author.get_full_name(),
                "email":new_book.author.email,
                "contact":new_book.author.contact,
                "type":new_book.author.user_type,
                'biography':new_book.author.biography,
                "created_at":new_book.author.created_at,
            }

            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    
    
#getting all books

@books.get('/')
def getAllbooks():

    try:
        all_books = Book.query.all()

        books_data = []
        for book in all_books:
            book_info = {
                    "id":book.id,
                'title':book.title,
            'description':book.description,
            'number_of_pages':book.number_of_pages,
            'price_unit':book.price_unit,
            'price':book.price,
            'generation':book.generation,
            'publication_date':book.publication_date,
            "company":{
                       
                'id': book.company.id,
                'name': book.company.name,
                'origin': book.company.origin,
                'description': book.company.description,
            },

            }

            books_data.append(book_info)


        return jsonify({
                'message':"All books retrieved successfully",
            "total_books":len(books_data),
            "books":books_data
        }),  HTTP_200_OK
        
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    

    #getting book by id
@books.get('/book/<int:id>')
@jwt_required()
def getbook(id):

    try:
        book = Book.query.filter_by(id=id).first()

      

        return jsonify({
            "message":"book details retrieved successfully",
            "book":{
              
                    "id":book.id,
                'title':book.title,
            'description':book.description,
            'number_of_pages':book.number_of_pages,
            'price_unit':book.price_unit,
            'price':book.price,
            'generation':book.generation,
            'publication_date':book.publication_date,
            "company":{
                       
                'id': book.company.id,
                'name': book.company.name,
                'origin': book.company.origin,
                'description': book.company.description,
            },

            "author":{
                 "first_name":book.author.first_name,
                "last_name":book.author.last_name,
                "authorname":book.author.get_full_name(),
                "email":book.author.email,
                "contact":book.author.contact,
                "type":book.author.user_type,
                'biography':book.author.biography,
                "created_at":book.author.created_at,
            }
            }
        })  ,HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
    