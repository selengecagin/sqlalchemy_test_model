from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #ORM

# create the app
app = Flask(__name__)
# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

# database object
db = SQLAlchemy(app)

# We want to create them model, model the holds the information on database. Done through a class
class Destination(db.Model):
    #everything here is a column
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False) #nullable = false, this column cannot be empty
    country = db.Column(db.String(50),nullable=False)
    rating = db.Column(db.Float, nullable=False)

# json data is very similar to a python dictionary, so we create a method to convert to data to a dict format so it is more easier to convert to json
    def to_dict(self): #this part makes it easier to
        return {
            "id":self.id,
            "destination":self.destination,
            "country": self.country,
            "rating": self.rating
        }

# create a context mmanager to set the actual file up
with app.app_context():
        db.create_all()

# Create Routes
# https://www.thenerdnook.com

@app.route('/')
def home():
    return jsonify({"message":"welcome to the travel api"})

# https://www.thenerdnook.com/destinations

@app.route("/destinations",methods=["GET"])
def get_destinations():
    destinations = Destination.query.all() # will fetch every row in the database

    return jsonify([destination.to_dict() for destination in destinations])


# https://www.thenerdnook.com/destinations/2
@app.route("/destinations/<int:destination_id>",methods = ["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found!"}),404

# POST
@app.route("/destinations",methods=["POST"])
def add_destination():
    data = request.get_json()

    new_destination = Destination(destination = data["destination"],
                                  country=data["country"],
                                  rating=data["rating"])

    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.to_dict()),201

# PUT -> Update
@app.route("/destinations/<int:destination_id>",methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id)
    if destination:
        destination.destination =data.get("destination",destination.destination)
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)

        db.session.commit()
        return jsonify(destination.to_dict())

    else:
        return jsonify({"error":"Destination not found"}),404

@app.route("/destinations/<int:destination_id>",methods=["DELETE"])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message":"destination was deleted"})
    else:
        return jsonify({"error":"Destination not found!"})

if __name__ == '__main__':
    app.run(debug=True)