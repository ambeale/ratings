"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show page about user"""

    user = User.query.filter(User.user_id == user_id).first()

    return render_template("user_info.html", user=user)

@app.route('/add-new')
def add_user_form():
    """Show new user form"""

    return render_template("add_user.html")


@app.route('/add_user', methods=["POST"])
def add_user():
    """Add new user to database."""
    
    new_email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    email_match = User.query.filter(User.email == new_email).first()

    if email_match:
        flash('You already exist.')
        return redirect('/login-form')
    else:
        new_user = User(email=new_email, 
                        password=password,
                        age=age,
                        zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

        flash("You've been added!")

        return redirect('/')

@app.route('/movies')
def movie_list():
    """Show list of movies"""

    movies = Movie.query.order_by('title').all()

    return render_template('movie_list.html', movies=movies)

@app.route('/login-form')
def login_page():
    """Show login form"""
    if session.get('user_id'):
        #show log out
        return render_template('logout_page.html')
    else:
        return render_template('login_page.html')


@app.route('/login', methods=["POST"])
def user_login():
    """Log user in"""

    email = request.form.get('email')
    password = request.form.get('password')

    user_info = User.query.filter(User.email == email).first()

    if user_info is None:
        #flash you don't exist 
        flash("""You don't exist. Are you a ghost?
                Or did you type your email wrong?""")
        return redirect('/')

    elif user_info.password == password:
        # go to homepage
        flash("You're logged in!")
        
        session['user_id'] = user_info.user_id
        print(session['user_id'])
        
        return redirect('/')

    else:
        flash("Wrong password. Try again. Be careful. Jeeeeezeeee")
        return redirect('/login-form')

@app.route('/logout')
def user_logout():
    """Log user out"""

    del session['user_id']

    flash("You're logged out. See you next time.")
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=5000, host='0.0.0.0')
