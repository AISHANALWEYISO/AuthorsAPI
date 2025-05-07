from app.extensions import db
from datetime import datetime
class Company(db.Model):
    __tablename__= "companys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    origin = db.Column(db.String(50))
    authors_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    description = db.Column(db.String(50))
    location = db.Column(db.String(50),unique=True )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('Author', backref = 'companys')


    def __init__(self, name, description, origin, authors_id):
        super(Company,self).__init__()
        self.name = name
        self.description = description
        self.origin = origin
        self.authors_id = authors_id

    def author_details(self):
        return f"The company {self.name} that deals {self.description} is located at{self.location}."


   
