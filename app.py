#App File
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime,timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
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
