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
    
    tags = db.relationship("Tag",
                            secondary = "posts_tags",
                            backref = "posts")
    
    def __repr__(self):
        """Show info about the post"""

        p = self
        return f"<User: {p.id} {p.title} {p.user_id} {u.content}>"
        
class Tag(db.Model):
    """Model for tags"""
    __tablename__ = "tags"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(127),
                      nullable = False)
                      
class PostTag(db.Model):
    """Model joining posts and tags"""
    __tablename__ = "posts_tags"
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key = True)
    
    
def get_tag_check_list(post_id):
    """Take a post_id and return the full list of tags marked with whether or not 
        the specified post has the tag
    """
    return db.session.query(Tag, PostTag).outerjoin(PostTag).all()#filter_by(PostTag.post_id == post_id)