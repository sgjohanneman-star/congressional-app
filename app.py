#App File
from flask import Flask, session, request, redirect, url_for, render_template, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import date,datetime,timezone,timedelta
import os,re
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


load_dotenv()

app = Flask(__name__)
limiter = Limiter(get_remote_address,app=app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY","burned_replace_later")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
#Note to self: Leave to false locally, but 1 on actual hosting platforms (pythonanywhere)
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("PRODUCTION") == "1"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Cache-Control"] = "no-store"
    return response


csrf = CSRFProtect(app)

db = SQLAlchemy(app)





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    total_points = db.Column(db.Integer, nullable=False, default=0)

class Island(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    description = db.Column(db.String(160), nullable=False)
    slot = db.Column(db.Integer,unique=True, nullable=False)
    questions = db.relationship("Question", back_populates="island")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    island_id = db.Column(db.Integer, db.ForeignKey("island.id"), nullable=False,)
    text = db.Column(db.String(500), nullable=False)
    choices = db.Column(db.JSON, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    island = db.relationship("Island", back_populates="questions")

class UserIslandProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    island_id = db.Column(db.Integer,db.ForeignKey("island.id"), nullable=False)
    current_question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    progress = db.Column(db.Integer, nullable=False, default=0)
    last_decay_date = db.Column(db.Date, default=date.today)
    __table_args__ = (db.UniqueConstraint("user_id", "island_id", name="one_progress_per_user_and_island"),)

class QuestionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    correctly_answered = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"), nullable=False)
    last_answered_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id", "question_id", name="one_result_per_user_and_question"),)

with app.app_context():
    db.create_all()


#App routing + login reqs + flask
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if(user_id):
            g.user = db.session.get(User,user_id)
        else:
            g.user = None
        if g.user is None:
            session.clear()
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped



@app.route("/")
@login_required
def hub():
    return f"Hi, {g.user.username}!"


@app.route("/register", methods=["GET","POST"])
def register():
    if(request.method == "POST"):
        username = request.form.get("username","").strip().lower()
        password = request.form.get("password","")
        rejected = False
        if not re.fullmatch(r"[A-Za-z0-9_]{6,35}", username):
            rejected = True
            flash("Usernames have to be 6-35 letters, numbers, or underscores.","error")
        pattern = r'[^a-zA-Z0-9\s]'
        if (len(password) < 10):
            rejected = True
            flash("Password was too short.","error")
        if(len(password) > 80):
            rejected = True
            flash("Password was too long.","error")
        if(not re.search(pattern,password)):
            rejected = True
            flash("Password did not contain special characters.","error")
        if(not (User.query.filter_by(username=username).first() is None)):
            rejected = True
            flash("Username is already taken.","error")
        if(not rejected):
            user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.flush()
            for island in Island.query.all():
                db.session.add(UserIslandProgress(user_id=user.id, island_id=island.id))
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("Username is already taken.","error")
            else:
                flash("Account created! Please log in.","success")
                return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
@limiter.limit("10 per minute", methods="POST")
def login():
    if(request.method == "POST"):
        username = request.form.get("username","").strip().lower()
        password = request.form.get("password","")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for("hub"))
        else:
            flash("Invalid username or password.","error")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))



if(__name__ == "__main__"):
    #Remove debug on production
    app.run(debug=True)