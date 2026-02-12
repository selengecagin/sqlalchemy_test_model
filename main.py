from flask import Flask
from flask_sqlalchemy import SQLAlchemy #ORM

# create the app
app = Flask(__name__)
# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

# database object
db = SQLAlchemy(app)

# initialize the app with the extension
db.init_app(app)

# We want to create them model, model the holds the information on database. Done through a class
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50),nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self): #this part makes it easier to
        return {
            "id":self.id,
            "destination":self.destination,
            "country": self.country,
            "rating": self.rating
        }

# Create Routes
# https://www.thenerdhook.com

@app.route('/')
def home():
    return 'hello'



if __name__ == '__main__':
    app.run(debug=True)