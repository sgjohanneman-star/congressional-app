#App File
from flask import Flask, session, request, redirect, url_for, render_template, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import datetime,timezone,timedelta
import os,re
import random
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import update

#Loading environment tools
load_dotenv()

#Creating a function to find the universal/comparable datetime
def today_utc():
    return datetime.now(timezone.utc).date()



#Creating the app and its limiter
app = Flask(__name__)
limiter = Limiter(get_remote_address,app=app)

#Setting app configurations and handling missing info
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
if "SECRET_KEY" not in os.environ:
    raise RuntimeError("SECRET_KEY is missing. Copy .env.example to .env and add a key (see README).")
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("PRODUCTION") == "1"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

#Post request processing to prevent cybersecurity attacks 
@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Cache-Control"] = "no-store"
    return response

#Handling a CSRF error from an alternate website
@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    flash("That page is expired. Please try again.","error")
    return redirect(url_for("login"))

#Handling each error and returning the user to a customized error page
@app.errorhandler(429)
def handle_rate_limit(error):
    return render_template("429.html"), 429

@app.errorhandler(500)
def not_found(error):
    db.session.rollback()
    return render_template("500.html"), 500

@app.errorhandler(404)
def server_error(error):
    return render_template("404.html"), 404

#Initializing the SQLLite database and CSRF protection
csrf = CSRFProtect(app)

db = SQLAlchemy(app)

#Points per question variables for easy code editing
points_per_question = 10
points_per_question_replay = points_per_question // 2




#Database model that holds the information for an app user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    total_points = db.Column(db.Integer, nullable=False, default=0)

#Database model that holds the information for each of the app's islands
class Island(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    description = db.Column(db.String(160), nullable=False)
    slot = db.Column(db.Integer,unique=True, nullable=False)
    questions = db.relationship("Question", back_populates="island")

#Database model that holds the information for each of the app's questions
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    island_id = db.Column(db.Integer, db.ForeignKey("island.id"), nullable=False,)
    text = db.Column(db.String(500), nullable=False)
    choices = db.Column(db.JSON, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    island = db.relationship("Island", back_populates="questions")

#Database model that holds the information for user progress
class UserIslandProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    island_id = db.Column(db.Integer,db.ForeignKey("island.id"), nullable=False)
    current_question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    progress = db.Column(db.Integer, nullable=False, default=0)
    last_decay_date = db.Column(db.Date, default=today_utc)
    __table_args__ = (db.UniqueConstraint("user_id", "island_id", name="one_progress_per_user_and_island"),)

#Database model that holds the information for each of the app's question results
class QuestionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    correctly_answered = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"), nullable=False)
    last_answered_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id", "question_id", name="one_result_per_user_and_question"),)




#Creating all databases when the program is run
with app.app_context():
    db.create_all()


#Ensures that a user is logged in to access a specific URL/page
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

#Progress decay function to encourage daily activity/memorization
def apply_decay(prog):
    days_away = (today_utc() - prog.last_decay_date).days
    if days_away > 0:
        prog.progress = max(0,prog.progress-days_away)
        prog.last_decay_date = today_utc()

#Function to return the islands progress as a string
def island_status(progress, total):
    if progress >= total:
        return "completed"
    if progress > 0:
        return "in_progress"
    return "not_started"

#Route for the hub, requiring a user's login to access, showing each island, progress, and the home page.
@app.route("/")
@login_required
def hub():
    for island in Island.query.all():
        prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first()
        if prog is None:
            prog = UserIslandProgress(user_id=g.user.id, island_id=island.id,progress=0, last_decay_date=today_utc())
        db.session.add(prog)
        apply_decay(prog)
    rows = (db.session.query(UserIslandProgress, Island).join(Island, UserIslandProgress.island_id == Island.id).filter(UserIslandProgress.user_id == g.user.id).order_by(Island.slot).all())
    islands = []
    for prog, island in rows:
        total = len(island.questions)
        islands.append({
        "slot": island.slot,
        "name": island.name,
        "description": island.description,
        "progress": prog.progress,
        "total": total,
        "status": island_status(prog.progress, total),
        })
    db.session.commit()
    
    return render_template("hub.html", username=g.user.username,total_points=g.user.total_points, islands=islands)

#Registration for the application, saves username and hashed password inputted
@app.route("/register", methods=["GET","POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("hub"))
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

#Login page, gets the user and hashed password, then compares to each of the names in the data base.
@app.route("/login", methods=["GET","POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("hub"))
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


#Logout route, clears session data and takes the user back to the login page.
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

#Finds eligible questions to ask and returns one to the user based on current island and previous question history
def pick_question(user_id, island):
    recent_rows = (
    QuestionResult.query.join(Question, QuestionResult.question_id == Question.id).filter(QuestionResult.user_id == user_id, Question.island_id == island.id).order_by(QuestionResult.last_answered_at.desc()).limit(5).all())
    recent_ids = [r.question_id for r in recent_rows]
    eligible = Question.query.filter(Question.island_id == island.id,Question.id.notin_(recent_ids),).all()
    if not eligible:
        eligible = island.questions
    return random.choice(eligible)

#Island question route, gives the user a question that they can submit to to send an answer and get points
@app.route("/island/<int:slot>", methods=["GET", "POST"])
@limiter.limit("60 per minute",methods=["POST"])
@login_required
def island_question(slot):
    island = Island.query.filter_by(slot=slot).first_or_404()
    prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first_or_404()
    apply_decay(prog)
    db.session.commit()
    total = len(island.questions)
    if prog.current_question_id is None:
        prog.current_question_id = pick_question(g.user.id, island).id
        db.session.commit()
    question = db.session.get(Question,prog.current_question_id)

    if request.method == "POST":
        answer = request.form.get("choice",type=int)
        if answer is None or not 0 <= answer < len(question.choices):
            flash("Not a valid answer to the question.","error")
            return redirect(url_for("island_question",slot=slot))
        submitted_id = request.form.get("question_id",type=int)
        if submitted_id != prog.current_question_id:
            flash("Question submitted does not match current question.","error")
            return redirect(url_for("island_question", slot=slot))
        claimed = db.session.execute(update(UserIslandProgress).where(UserIslandProgress.id == prog.id,UserIslandProgress.current_question_id == question.id).values(current_question_id=None)).rowcount
        if claimed == 0:
            db.session.rollback()
            flash("Question was already answered.", "error")
            return redirect(url_for("island_question", slot=slot))
        is_correct = answer == question.correct_answer
        result = QuestionResult.query.filter_by(user_id=g.user.id,question_id=question.id).first()
        points = 0
        if result is None:
            result = QuestionResult(user_id=g.user.id,question_id=question.id)
            db.session.add(result)
        already_earned = bool(result.correctly_answered)
        result.last_answered_at = datetime.now(timezone.utc)
        if is_correct:
            points = points_per_question_replay if already_earned else points_per_question
            result.correctly_answered = True
        old_progress = prog.progress
        if is_correct:
            prog.progress = min(prog.progress + 1, total)
            g.user.total_points = User.total_points + points
        was_replay = is_correct and bool(already_earned)
        
        just_completed = is_correct and old_progress < total and prog.progress == total
        session["last_result"] = {"slot": slot,"chosen_text": question.choices[answer],"correct_text": question.choices[question.correct_answer],"was_correct": is_correct,"points": points,"just_completed": just_completed,"was_replay": was_replay,}
        db.session.commit()
        return redirect(url_for("island_feedback",slot=slot))
    return render_template("quiz.html",island_name=island.name,question_text=question.text,choices=question.choices,question_id=question.id,progress=prog.progress,total=total,slot=slot)

#Island feedback route, shows the user what was wrong and their current progress.
@app.route("/island/<int:slot>/feedback", methods=["GET"])
@login_required
def island_feedback(slot):
    result = session.pop("last_result", None)
    if result is None or result["slot"] != slot:
        return redirect(url_for("island_question",slot=slot))
    island = Island.query.filter_by(slot=slot).first_or_404()
    prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first_or_404()
    total = len(island.questions)
    return render_template("feedback.html",island_name=island.name,slot=slot,was_correct=result["was_correct"],chosen_text=result["chosen_text"],correct_text=result["correct_text"],points_awarded=result["points"],progress=prog.progress,total=total,just_completed=result["just_completed"],was_replay=result.get("was_replay",False))

#Shows the user the complete question and gives positive feedback on their correct answer.
@app.route("/island/<int:slot>/complete", methods=["GET"])
@login_required
def island_complete(slot):
    island = Island.query.filter_by(slot=slot).first_or_404()
    prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first_or_404()
    total = len(island.questions)
    apply_decay(prog)
    db.session.commit()
    if(prog.progress < total):
        return redirect(url_for("island_question",slot=slot))
    return render_template("complete.html",island_name=island.name,slot=slot,progress=prog.progress,total=total,total_points=g.user.total_points)




#Runs the app if this is the main file run
if(__name__ == "__main__"):
    #add debug=True if locally testing alone (Never on development)

    app.run()