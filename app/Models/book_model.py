from app.extensions import db
from datetime import datetime
class Book(db.Model):
    __tablename__= "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    number_of_pages = db.Column(db.String(50), nullable=False,unique=True)
    price_unit = db.Column(db.String(50), nullable=False,unique=True )
    publication_date = db.Column(db.Text(), nullable=False)
    writer = db.Column(db.String(50), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companys.id'))
    other_books = db.Column(db.String(30),default='author')
    generation = db.Column(db.DateTime,default=datetime.now())


    def __init__(self, id, title, description, number_of_pages, price_unit, writer, other_books, generation, publication_date):
        super(Book,self).__init__()
        self.id = id
        self.title = title
        self.description = description
        self.number_of_pages = number_of_pages
        self.price_unit = price_unit
        self.writer = writer
        self.publication_date = publication_date
        self.other_books = other_books
        self.generation = generation 

    def __book_details(self, id, title, description, number_of_pages, price_unit, writer, other_books, generation, publication_date):
        return f"The book is {self.title} described as {self.description} with these {self.number_of_pages} of pages costly {self.price_unit} wrote by {self.writer} and other books {self.other_books} generated on {self.generation} published on {self.publication_date} ."

