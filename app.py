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
    #Add new 
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
    posts = Post.query.filter_by(user_id = user_id)
    return render_template("view.html",
        header = "SqlAlchemy",
        title = "Edit User" + user_id,
        name = user.first_name + " " + user.last_name,
        image_url = user.image_url,
        user_id = user.id,
        posts = posts)
        
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
    
@app.route("/users/<user_id>/posts/new")
def new_post(user_id):
    """Add new post"""
    user = User.query.get(user_id) 
    tags = Tag.query.all()
    if request.args:
        new_post = Post(user_id = user.id,
                        title = request.args["title"],
                        content = request.args["content"])
        #add new tags to the new post
        for tag in tags:
            if(request.args.get("tag-"+str(tag.id), False)):
                new_post.tags.append(tag)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/users/" + str(user.id))
    
    return render_template("createPost.html",
        header = "Add Post for " + user.full_name(),
        title = "Create new post",
        tags = tags)
    
@app.route("/posts/<post_id>")
def view_post(post_id):
    post = Post.query.get(post_id)
    tags = post.tags
    return render_template("viewPost.html",
        header = post.title,
        title = "View post",
        post = post,
        author = User.query.get(post.user_id).full_name(),
        tags = tags)

        
@app.route("/posts/<post_id>/edit")
def edit_post(post_id):
    """Edit given post"""
    post = Post.query.get(post_id) 
    tags = get_tag_check_list(post_id)#Tag.query.all()
    if request.args:
        post.title = request.args["title"]
        post.content = request.args["content"]
        #update tags on the post
        for tag in tags:
            if(request.args.get("tag-"+str(tag[0].id), False) and tag[1] ==None):
                post.tags.append(tag[0])
            elif(not request.args.get("tag-"+str(tag[0].id), False) and tag[1] != None):
                post.tags.remove(tag[0])
        db.session.commit()
        return redirect("/users/" + str(post.user_id))
    return render_template("editPost.html",
        header = "SqlAlchemy",
        title = "Edit post" + str(post_id),
        post = post,
        tags = tags)
        
@app.route("/posts/<post_id>/delete")
def delete_post(post_id):
    """Delete given post"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit() 
    return redirect("/users/"+str(post.user_id))   
    
@app.route("/tags")    
def start_tags():
    """render tag view page"""
    tags = Tag.query.all()
    return render_template("startTags.html",
        header = "SqlAlchemy",
        title = "tags",
        tags = tags) 
               
@app.route("/tags/new")
def create_tag():
    """Add new tag"""
    #Add new 
    if request.args:
        new_tag = Tag(name = request.args["name"])
        db.session.add(new_tag)
        db.session.commit()
        return redirect("/tags")
    return render_template("createTag.html",
        header = "SqlAlchemy",
        title = "Add New tag")     

@app.route("/tags/<tag_id>")
def view_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template("viewTag.html",
        header = "View Tag",
        title = "View tag",
        tag = tag)        

        
@app.route("/tags/<tag_id>/edit")
def edit_tag(tag_id):
    """Edit given tag"""
    tag = Tag.query.get(tag_id) 
    if request.args:
        tag.name = request.args["name"]
        db.session.commit()
        return redirect("/tags")
    return render_template("editTag.html",
        header = "SqlAlchemy",
        title = "Edit tag" + str(tag_id),
        tag = tag)
        
@app.route("/tags/<tag_id>/delete")
def delete_tag(tag_id):
    """Delete given tag"""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit() 
    return redirect("/tags")   
   