from flask import Flask, request, redirect, render_template, session, flash
from models import User, db, connect_db, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from forms import AddUserForm, LoginForm, AddFeedback

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

with app.app_context():

    connect_db(app)
    db.create_all()


@app.route("/")
def home():
    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Form to register/create a user"""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data

        new_user = User.register(username, password, email, first, last)
        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username 

        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("add-user.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login_page():
    """Show login form and handle the submission"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_log = User.authenticate(username, password)

        if user_log:
            session["username"] = user_log.username 
            return redirect(f"/users/{user_log.username}")
        else:
            form.username.errors = ["Incorrect username/password"]

    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    """Logout of website"""

    session.pop('username')
    return redirect("/")

@app.route("/users/<username>")
def show_edit_user(username):
    """Show user feedback and action links"""

    if 'username' not in session:
        flash("Must be logged in to view!", category = "alert alert-danger")
        return redirect("/")
    
    user = User.query.get_or_404(username)
    return render_template("user-feedback.html", user = user)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """DELETE user info and any feeback made by user"""

    if 'username' not in session:
        flash("Must be logged in to view!", category = "alert alert-danger")
        return redirect("/")
    
    db.session.delete(User.query.get_or_404(username))
    db.session.commit()

    session.pop("username")

    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Add Feedback form handle showing form and submission"""

    if 'username' not in session:
        flash("Must be logged in to view!", category = "alert alert-danger")
        return redirect("/")
    
    form = AddFeedback()
    
    if form.validate_on_submit():
        fb = Feedback(title=form.title.data, content=form.content.data, username=username)
        db.session.add(fb)
        db.session.commit()
        return redirect(f"/users/{session['username']}")

    return render_template("add-feedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update feedback form and handle form submission"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.user.username != session['username']:
        flash("Not Authorized!", category = "error")
        return redirect("/")
    
    form = AddFeedback()
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{session['username']}")

    form.title.data = feedback.title
    form.content.data = feedback.content
    return render_template("add-feedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """DELETE feedback and then redirect"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.user.username != session['username']:
        flash("Not Authorized!", category = "error")
        return redirect("/")
    
    db.session.delete(Feedback.query.get_or_404(feedback_id))
    db.session.commit()

    return redirect(f"/users/{session['username']}")
