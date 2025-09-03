from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import joinedload


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    User_id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Passhash = db.Column(db.String(256), nullable=False)
    FullName = db.Column(db.String(120), nullable=True)
    Qualification = db.Column(db.String(200), nullable=True)
    DOB = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User {self.Email}>"

class Subject(db.Model):
    __tablename__ = 'subjects'
    Sub_id = db.Column(db.Integer, primary_key=True)
    SubName = db.Column(db.String(100), nullable=False)
    Sub_Description = db.Column(db.String(200), nullable=False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Subject {self.SubName}>"

class Chapter(db.Model):
    __tablename__ = 'chapters'
    Ch_id = db.Column(db.Integer, primary_key=True)
    Sub_id = db.Column(db.Integer, db.ForeignKey('subjects.Sub_id', ondelete='CASCADE'), nullable=False)
    Ch_name = db.Column(db.String(100), nullable=False)
    Ch_description = db.Column(db.String(200), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Chapter {self.Ch_name}>"

class Quiz(db.Model):
    __tablename__ = "quizzes"
    Q_id = db.Column(db.Integer, primary_key=True)
    Ch_id = db.Column(db.Integer, db.ForeignKey("chapters.Ch_id", ondelete='CASCADE'), nullable=False)
    Date_of_quiz = db.Column(db.Date, nullable=False)
    Time_duration = db.Column(db.Integer, nullable=False)  # in minutes
    No_of_questions = db.Column(db.Integer, nullable=False)
    Total_marks = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Quiz {self.Q_id}>"

class Question(db.Model):
    __tablename__ = "questions"
    Qs_id = db.Column(db.Integer, primary_key=True)
    Q_id = db.Column(db.Integer, db.ForeignKey("quizzes.Q_id", ondelete='CASCADE'), nullable=False)
    Qs_statement = db.Column(db.Text, nullable=False)
    Marks = db.Column(db.Integer, nullable=False)
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Question {self.Qs_id}>"

class Option(db.Model):
    __tablename__ = "options"
    O_id = db.Column(db.Integer, primary_key=True)
    Qs_id = db.Column(db.Integer, db.ForeignKey("questions.Qs_id", ondelete='CASCADE'), nullable=False)
    O_statement = db.Column(db.Text, nullable=False)
    Is_correct = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Option {self.O_id}>"

class Score(db.Model):
    __tablename__ = "scores"
    S_id = db.Column(db.Integer, primary_key=True)
    Q_id = db.Column(db.Integer, db.ForeignKey("quizzes.Q_id"), nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey("users.User_id"), nullable=False)
    Timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Total_scored = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref='scores', lazy=True)

    def __repr__(self):
        return f"<Score {self.S_id}>"