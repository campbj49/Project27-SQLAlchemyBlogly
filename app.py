"""Blogly application."""

from flask import Flask,render_template, redirect, flash, session, request, jsonify
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def redir():
    return redirect("/users")

@app.route("/users")
def start():
    """render landing page"""
    steve = User.query.get(1)#User(first_name = "Steve", last_name = "Minecraft", image_url = "https://minecraftfaces.com/wp-content/bigfaces/big-steve-face.png")
    #db.session.add(steve)
    #db.session.commit()
    users = User.query.all()
    return render_template("start.html",
        header = "SqlAlchemy",
        title = "Users",
       users = users)
        
@app.route("/users/new")
def create():
    """Add new user"""
    new_user = "Unassigned New Users"
    if request.args:
        new_user = User(first_name = request.args["firstName"], 
                        last_name = request.args["lastName"], 
                        image_url = request.args["imageURL"])
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    return render_template("create.html",
        header = "SqlAlchemy",
        title = "Add New User")
        
@app.route("/users/<user_id>")
def view(user_id):
    """View given user_id"""
    user = User.query.get(user_id)
    return render_template("view.html",
        header = "SqlAlchemy",
        title = "Edit User" + user_id,
        name = user.first_name + " " + user.last_name,
        image_url = user.image_url,
        user_id = user.id)
        
@app.route("/users/<user_id>/edit")
def edit(user_id):
    """Edit given user"""
    user = User.query.get(user_id) 
    if request.args:
        user.first_name = request.args["firstName"]
        user.last_name = request.args["lastName"]
        user.image_url = request.args["imageURL"]
        db.session.commit()
        return redirect("/users")
    return render_template("edit.html",
        header = "SqlAlchemy",
        title = "Edit User" + user_id,
        user = user)
        
@app.route("/users/<user_id>/delete")
def delete(user_id):
    """Delete given user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit() 
    return redirect("/users")