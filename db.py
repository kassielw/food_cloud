from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

CATEGORIES = ["Studying", "Food", "Fitness", "Hotspots", "Dorms"]

class Attraction(db.Model):
    __tablename__ = "attraction"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", cascade="delete")
    category = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.address = kwargs.get("address")
        self.description = kwargs.get("description")
        self.category = kwargs.get("category")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "description": self.description,
            "category": self.category,
            "posts": [p.serialize() for p in self.posts]
        }


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=True)
    rating = db.Column(db.Integer,  nullable=True)
    description = db.Column(db.String, nullable=False)
    comments = db.relationship("Comment", cascade="delete")
    attraction_id = db.Column(db.Integer, db.ForeignKey("attraction.id"))

    def __init__(self, **kwargs):
        self.netid = kwargs.get("netid")
        self.name = kwargs.get("name")
        self.picture = kwargs.get("picture")
        self.rating = kwargs.get("rating")
        self.description = kwargs.get("description")
        self.attraction_id = kwargs.get("attraction_id")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name if self.name else "Anonymous",
            "picture": self.picture if self.picture else "N/A",
            "rating": self.rating if self.rating else "N/A",
            "description": self.description,
            "comments": [c.serialize() for c in self.comments]
        }


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, default="Anonymous")
    description = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __init__(self, **kwargs):
        self.netid = kwargs.get("netid")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.post_id = kwargs.get("post_id")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
