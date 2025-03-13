from app.extensions import db
from datetime import datetime
class Company(db.Model):
    __tablename__= "companys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    description = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False,unique=True )
    created_at= db.Column(db.Text(), nullable=False)
    author = db.relationship('Author', backref = 'companys')


    def __init__(self, id, name, description, origin, location, other_books, created_at, owner):
        super(Company,self).__init__()
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.created_at = created_at
        self.owner = owner

    def __author_details(self, id, name, description, origin, location, other_books, created_at, owner):
        return f"The book is {self.name} described by{self.description} found at{self.location} created at {self.created_at} ownwed by{self.owner}"


   
