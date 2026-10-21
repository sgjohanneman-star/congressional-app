#App File
from flask import Flask, session, request, redirect, url_for, render_template, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import date,datetime,timezone,timedelta
import os,re
import random
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


load_dotenv()

def today_utc():
    return datetime.now(timezone.utc).date()


app = Flask(__name__)
limiter = Limiter(get_remote_address,app=app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
#need to replace the key later
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

@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    flash("That page is expired. Please try again","error")
    return redirect(url_for("login"))

csrf = CSRFProtect(app)

db = SQLAlchemy(app)


points_per_question = 10


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
    last_decay_date = db.Column(db.Date, default=today_utc)
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

def apply_decay(prog):
    days_away = (today_utc() - prog.last_decay_date).days
    if days_away > 0:
        prog.progress = max(0,prog.progress-days_away)
        prog.last_decay_date = today_utc()

def island_status(progress, total):
    if progress >= total:
        return "completed"
    if progress > 0:
        return "in_progress"
    return "not_started"


@app.route("/")
@login_required
def hub():
    for island in Island.query.all():
        prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first_or_404()
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


@app.route("/login", methods=["GET","POST"])
@limiter.limit("10 per minute", methods="POST")
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



@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

def pick_question(user_id, island):
    recent_rows = (
    QuestionResult.query
    .join(Question, QuestionResult.question_id == Question.id)
    .filter(QuestionResult.user_id == user_id, Question.island_id == island.id)
    .order_by(QuestionResult.last_answered_at.desc())
    .limit(5)
    .all()
)
    recent_ids = [r.question_id for r in recent_rows]
    eligible = Question.query.filter(
    Question.island_id == island.id,
    Question.id.notin_(recent_ids),
).all()
    return random.choice(eligible)

@app.route("/island/<int:slot>", methods=["GET", "POST"])
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
            return redirect(url_for("island_question"))
        submitted_id = request.form.get("question_id",type=int)
        if submitted_id != prog.current_question_id:
            flash("Question submitted does not match current question.","error")
            return redirect(url_for("island_question", slot=slot))
        is_correct = answer == question.correct_answer
        result = QuestionResult.query.filter_by(user_id=g.user.id,question_id=question.id).first()
        if result is None:
            result = QuestionResult(user_id=g.user.id,question_id=question.id)
            db.session.add(result)
        result.last_answered_at = datetime.now(timezone.utc)
        if is_correct:
            result.correctly_answered = True
        old_progress = prog.progress
        if is_correct:
            prog.progress = min(prog.progress + 1, total)
            g.user.total_points += points_per_question
        just_completed = is_correct and old_progress < total and prog.progress == total
        prog.current_question_id = None
        session["last_result"] = {
        "slot": slot,
        "chosen_text": question.choices[answer],
        "correct_text": question.choices[question.correct_answer],
        "was_correct": is_correct,
        "points": points_per_question if is_correct else 0,
        "just_completed": just_completed,
        }
        db.session.commit()
        return redirect(url_for("island_feedback",slot=slot))
    return render_template("quiz.html",island_name=island.name,question_text=question.text,choices=question.choices,question_id=question.id,progress=prog.progress,total=total,slot=slot)

@app.route("/island/<int:slot>/feedback", methods=["GET"])
@login_required
def island_feedback(slot):
    result = session.pop("last_result", None)
    if result is None or result["slot"] != slot:
        return redirect(url_for("island_question",slot=slot))
    island = Island.query.filter_by(slot=slot).first_or_404()
    prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first_or_404()
    total = len(island.questions)
    return render_template("feedback.html",island_name=island.name,slot=slot,was_correct=result["was_correct"],chosen_text=result["chosen_text"],correct_text=result["correct_text"],points_awarded=result["points"],progress=prog.progress,total=total,just_completed=result["just_completed"])


@app.route("/island/<int:slot>/complete", methods=["GET"])
@login_required
def island_complete(slot):
    island = Island.query.filter_by(slot=slot).first_or_404()
    prog = UserIslandProgress.query.filter_by(user_id=g.user.id, island_id=island.id).first_or_404()
    total = len(island.questions)

    if(prog.progress < total):
        return redirect(url_for("island_question",slot=slot))
    return render_template("complete.html",island_name=island.name,slot=slot,progress=prog.progress,total=total,total_points=g.user.total_points)





if(__name__ == "__main__"):
    #Remove debug on production
    app.run(debug=True)