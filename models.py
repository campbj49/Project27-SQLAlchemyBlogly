"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    app.app_context().push()
    
    
class User(db.Model):
    """User model adapted from Pets example"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User: {u.id} {u.first_name} {u.last_name} {u.image_url}>"
        
class Post(db.Model):
    """Model for storing blog posts"""
    __tablename__ = "posts"
    

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(255),
                      nullable = False)
    content = db.Column(db.String(1024))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = db.relationship("User", backref="posts")
    
    def __repr__(self):
        """Show info about the post"""

        p = self
        return f"<User: {p.id} {p.title} {p.user_id} {u.content}>"