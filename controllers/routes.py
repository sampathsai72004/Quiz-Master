from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, User, Subject, Chapter, Quiz, Question, Option, Score
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import joinedload
import matplotlib
matplotlib.use('Agg')

routes_bp = Blueprint("routes", __name__)

@routes_bp.route('/')
def index():
    if '_flashes' in session:
        session.pop('_flashes')
    return render_template('index.html')

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('fullname')
        qualification = request.form.get('qualification')
        dob_str = request.form.get('dob')

        if not all([username, password, confirm_password, name, qualification, dob_str]):
            flash("All fields are required!", "danger")
            return redirect(url_for('routes.register'))

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('routes.register'))

        existing_user = User.query.filter_by(Email=username).first()
        if existing_user:
            flash("Username already exists. Please log in.", "warning")
            return redirect(url_for('routes.login', role="user"))

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            new_user = User(
                Email=username,
                Passhash=generate_password_hash(password),
                FullName=name,
                Qualification=qualification,
                DOB=dob
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('routes.login', role="user"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('routes.register'))

    return render_template('register.html')

@routes_bp.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please fill out all fields", "danger")
            return redirect(url_for('routes.login', role=role))

        if username == "admin123@gmail.com" and password == "admin123":
            if role != 'admin':
                flash("Unauthorized login attempt", "danger")
                return redirect(url_for('routes.index'))

            admin_user = User.query.filter_by(Email=username, is_admin=True).first()
            if not admin_user:
                flash("Admin user not found in DB", "danger")
                return redirect(url_for('routes.index'))

            session.update({'user_id': admin_user.User_id, 'email': admin_user.Email, 'role': 'admin'})
            flash("Admin login successful!", "success")
            return redirect(url_for('routes.admin_dashboard'))

        user = User.query.filter_by(Email=username).first()
        if not user or not check_password_hash(user.Passhash, password):
            flash("Invalid credentials", "danger")
            return redirect(url_for('routes.login', role=role))

        if user.is_admin and role != 'admin':
            flash("You're not allowed to login as user!", "danger")
            return redirect(url_for('routes.index'))

        session.update({'user_id': user.User_id, 'email': user.Email, 'role': 'user'})
        flash("Login successful!", "success")
        return redirect(url_for('routes.user_dashboard'))

    return render_template('login.html', role=role)

@routes_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('routes.index'))

@routes_bp.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('routes.login', role='admin'))

    subjects = {}
    all_subjects = Subject.query.all()
    for subject in all_subjects:
        chapters = Chapter.query.filter_by(Sub_id=subject.Sub_id).all()
        subjects[subject] = chapters
    return render_template('admin_dashboard.html', subjects=subjects)

@routes_bp.route('/add_subject', methods=['POST'])
def add_subject():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        flash("All fields are required", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    new_subject = Subject(SubName=name, Sub_Description=description)
    db.session.add(new_subject)
    db.session.commit()
    flash("Subject added successfully", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes_bp.route('/edit_subject/<int:subject_id>', methods=['POST'])
def edit_subject(subject_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    name = request.form.get('name')
    description = request.form.get('description')
    subject = Subject.query.get_or_404(subject_id)

    subject.SubName = name
    subject.Sub_Description = description
    db.session.commit()
    flash("Subject updated", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes_bp.route('/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    subject = Subject.query.get_or_404(subject_id)
    for chapter in subject.chapters:
        Quiz.query.filter_by(Ch_id=chapter.Ch_id).delete()
    Chapter.query.filter_by(Sub_id=subject_id).delete()
    db.session.delete(subject)
    db.session.commit()
    flash("Subject and all related content deleted", "info")
    return redirect(url_for('routes.admin_dashboard'))

@routes_bp.route('/add_chapter/<int:subject_id>', methods=['POST'])
def add_chapter(subject_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    name = request.form.get('chapter_name')
    description = request.form.get('chapter_description')
    new_chapter = Chapter(Sub_id=subject_id, Ch_name=name, Ch_description=description)
    db.session.add(new_chapter)
    db.session.commit()
    flash("Chapter added", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes_bp.route('/edit_chapter/<int:chapter_id>', methods=['POST'])
def edit_chapter(chapter_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    name = request.form.get('name')
    description = request.form.get('description')
    chapter = Chapter.query.get_or_404(chapter_id)

    chapter.Ch_name = name
    chapter.Ch_description = description
    db.session.commit()
    flash("Chapter updated", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes_bp.route('/delete_chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.Sub_id
    Quiz.query.filter_by(Ch_id=chapter_id).delete()
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter and all related quizzes deleted", "info")
    return redirect(url_for('routes.admin_dashboard'))

@routes_bp.route('/add_quiz/<int:chapter_id>', methods=['POST'])
def add_quiz(chapter_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    try:
        quiz = Quiz(
            Ch_id=chapter_id,
            Date_of_quiz=datetime.strptime(request.form.get('date_of_quiz'), '%Y-%m-%d').date(),
            Time_duration=int(request.form.get('time_duration')),
            No_of_questions=int(request.form.get('no_of_questions')),
            Total_marks=int(request.form.get('total_marks'))
        )
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz added", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for('routes.admin_quiz', chapter_id=chapter_id))

@routes_bp.route('/edit_quiz/<int:quiz_id>', methods=['POST'])
def edit_quiz(quiz_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.Date_of_quiz = datetime.strptime(request.form.get('date_of_quiz'), '%Y-%m-%d').date()
    quiz.Time_duration = int(request.form.get('time_duration'))
    quiz.No_of_questions = int(request.form.get('no_of_questions'))
    quiz.Total_marks = int(request.form.get('total_marks'))
    db.session.commit()
    flash("Quiz updated", "success")
    return redirect(url_for('routes.admin_quiz', chapter_id=quiz.Ch_id))

@routes_bp.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.Ch_id
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted", "info")
    return redirect(url_for('routes.admin_quiz', chapter_id=chapter_id))

@routes_bp.route('/admin_quiz/<int:chapter_id>')
def admin_quiz(chapter_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(Ch_id=chapter_id).options(joinedload(Quiz.questions).joinedload(Question.options)).all()
    return render_template('admin_quiz.html', chapter=chapter, quizzes=quizzes)

@routes_bp.route('/add_question/<int:quiz_id>', methods=['POST'])
def add_question(quiz_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    statement = request.form.get('statement')
    correct_index = int(request.form.get('correct_option'))
    options = [request.form.get(f'option{i}') for i in range(1, 5)]

    question = Question(Qs_statement=statement, Marks=1, Q_id=quiz_id)
    db.session.add(question)
    db.session.flush()
    for i, opt in enumerate(options, start=1):
        db.session.add(Option(Qs_id=question.Qs_id, O_statement=opt, Is_correct=(i == correct_index)))
    db.session.commit()

    flash("Question added", "success")
    return redirect(url_for('routes.admin_quiz', chapter_id=question.quiz.Ch_id))

@routes_bp.route('/edit_question/<int:question_id>', methods=['POST'])
def edit_question(question_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    question = Question.query.get_or_404(question_id)
    question.Qs_statement = request.form.get('statement')
    correct_index = int(request.form.get('correct_option'))
    options = Option.query.filter_by(Qs_id=question_id).order_by(Option.O_id).all()
    for i, option in enumerate(options, start=1):
        option.O_statement = request.form.get(f'option{i}')
        option.Is_correct = (i == correct_index)
    db.session.commit()

    flash("Question updated", "success")
    return redirect(url_for('routes.admin_quiz', chapter_id=question.quiz.Ch_id))

@routes_bp.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    question = Question.query.get_or_404(question_id)
    chapter_id = question.quiz.Ch_id
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted", "info")
    return redirect(url_for('routes.admin_quiz', chapter_id=chapter_id))

import io
@routes_bp.route('/user_dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('routes.login', role='user'))
    quizzes = Quiz.query.options(joinedload(Quiz.chapter).joinedload(Chapter.subject)).all()
    return render_template('user_dashboard.html', quizzes=quizzes)

@routes_bp.route('/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'user_id' not in session:
        flash("Please log in", "danger")
        return redirect(url_for('routes.login', role='user'))
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('start_quiz.html', quiz=quiz, questions=quiz.questions)

@routes_bp.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user_id = session.get('user_id')
    total_score = 0
    for question in quiz.questions:
        selected_option_id = request.form.get(f"question_{question.Qs_id}")
        if selected_option_id:
            selected_option = Option.query.get(int(selected_option_id))
            if selected_option and selected_option.Is_correct:
                total_score += question.Marks
    score = Score(User_id=user_id, Q_id=quiz.Q_id, Total_scored=total_score)
    db.session.add(score)
    db.session.commit()
    flash(f"Your score: {total_score}", "success")
    return redirect(url_for('routes.user_dashboard'))

@routes_bp.route('/scores')
def scores():
    if 'user_id' not in session:
        flash("Please log in.", "danger")
        return redirect(url_for('routes.login', role='user'))
    user_id = session['user_id']
    scores = Score.query.filter_by(User_id=user_id).join(Quiz).join(Chapter).join(Subject).all()
    return render_template("scores.html", scores=scores)

from flask import render_template, session, redirect, url_for, flash
from models.models import db, Subject, Chapter, Quiz, User, Score
from sqlalchemy import func
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Blueprint

@routes_bp.route('/admin_summary')
def admin_summary():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.login', role='admin'))

    total_subjects = Subject.query.count()  
    total_chapters = Chapter.query.count()
    total_quizzes = Quiz.query.count()
    total_users = User.query.count()
    latest_quizzes = Quiz.query.order_by(Quiz.Date_of_quiz.desc()).limit(5).all()
    average_scores = db.session.query(func.avg(Score.Total_scored)).scalar()

    avg_scores_by_date = db.session.query(
        Quiz.Date_of_quiz, func.avg(Score.Total_scored)
    ).join(Score).group_by(Quiz.Date_of_quiz).order_by(Quiz.Date_of_quiz).all()
    dates = [record[0].strftime('%Y-%m-%d') for record in avg_scores_by_date]
    avg_scores = [record[1] for record in avg_scores_by_date]
    plt.figure(figsize=(6, 4))
    plt.plot(dates, avg_scores, marker='o', linestyle='-', color='mediumseagreen')
    plt.title("Average Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf1 = BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    line_chart = base64.b64encode(buf1.getvalue()).decode()
    plt.close()
    
    quiz_attempts = db.session.query(
        Quiz.Q_id, Quiz.Date_of_quiz, func.count(Score.S_id)
    ).join(Score).group_by(Quiz.Q_id).order_by(Quiz.Date_of_quiz).all()
    quiz_labels = [f"Q{q[0]} ({q[1].strftime('%b %d')})" for q in quiz_attempts]
    attempt_counts = [q[2] for q in quiz_attempts]
    plt.figure(figsize=(6, 4))
    plt.bar(quiz_labels, attempt_counts, color='cornflowerblue')
    plt.title("Quiz Attempt Count")
    plt.xlabel("Quiz")
    plt.ylabel("Attempts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf2 = BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    bar_chart = base64.b64encode(buf2.getvalue()).decode()
    plt.close()

    user_scores_query = db.session.query(
        User.FullName.label('username'),
        Quiz.Date_of_quiz.label('quiz_name'),
        Score.Total_scored.label('latest_score')
    ).join(Score, User.User_id == Score.User_id)\
     .join(Quiz, Quiz.Q_id == Score.Q_id)\
     .order_by(Score.Timestamp.desc())\
     .limit(10).all()

    return render_template("admin_summary.html",
        total_subjects=total_subjects,  
        total_chapters=total_chapters,
        total_quizzes=total_quizzes,
        total_users=total_users,
        latest_quizzes=latest_quizzes,
        average_scores=round(average_scores or 0, 2),
        user_scores=user_scores_query,
        line_chart=line_chart,
        bar_chart=bar_chart
    )

@routes_bp.route('/admin/quizzes')
def admin_quizzes():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_dashboard'))

    subjects = Subject.query.options(
        joinedload(Subject.chapters).joinedload(Chapter.quizzes)
    ).all()
    return render_template('admin_quizzes.html', subjects=subjects)

@routes_bp.route('/form_add_subject', methods=['POST'])
def form_add_subject():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_quizzes'))

    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        flash("Name and description are required.", "danger")
        return redirect(url_for('routes.admin_quizzes'))

    try:
        new_subject = Subject(SubName=name, Sub_Description=description)
        db.session.add(new_subject)
        db.session.commit()
        flash("Subject added successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Failed to add subject.", "danger")
    return redirect(url_for('routes.admin_quizzes'))

@routes_bp.route('/form_add_chapter', methods=['POST'])
def form_add_chapter():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_quizzes'))

    subject_id = request.form.get('subject_id')
    chapter_name = request.form.get('chapter_name')
    chapter_description = request.form.get('chapter_description')

    if not subject_id or not chapter_name or not chapter_description:
        flash("All fields are required.", "danger")
        return redirect(url_for('routes.admin_quizzes'))

    try:
        new_chapter = Chapter(Ch_name=chapter_name, Ch_description=chapter_description, Sub_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        flash("Chapter added successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Failed to add chapter.", "danger")
    return redirect(url_for('routes.admin_quizzes'))

@routes_bp.route('/form_delete_chapter/<int:chapter_id>', methods=['POST'])
def form_delete_chapter(chapter_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_quizzes'))

    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        Quiz.query.filter_by(Ch_id=chapter_id).delete()
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter and all related quizzes deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Failed to delete chapter.", "danger")
    return redirect(url_for('routes.admin_quizzes'))

@routes_bp.route('/admin_settings', methods=['GET', 'POST'])
def admin_settings():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.login', role='admin'))

    search_query = request.args.get('search', '').strip()
    if request.method == 'POST':
        if 'add_user' in request.form:
            fullname = request.form.get('fullname')
            email = request.form.get('email')
            password = request.form.get('password')
            qualification = request.form.get('qualification')
            dob_str = request.form.get('dob')
            is_admin = request.form.get('is_admin', '0') == '1'

            if not all([fullname, email, password]):
                flash("Name, email and password are required", "danger")
                return redirect(url_for('routes.admin_settings'))

            if User.query.filter_by(Email=email).first():
                flash("User already exists", "warning")
                return redirect(url_for('routes.admin_settings'))

            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
                new_user = User(
                    FullName=fullname,
                    Email=email,
                    Passhash=generate_password_hash(password),
                    Qualification=qualification,
                    DOB=dob,
                    is_admin=is_admin
                )
                db.session.add(new_user)
                db.session.commit()
                flash("User added successfully", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating user: {str(e)}", "danger")

        elif 'delete_user' in request.form:
            user_id = request.form.get('user_id')
            user = User.query.get(user_id)
            if user:
                if user.Email == 'admin123@gmail.com':  
                    flash("Cannot delete default admin user", "warning")
                else:
                    db.session.delete(user)
                    db.session.commit()
                    flash("User deleted", "success")
            else:
                flash("User not found", "danger")

    users_query = User.query
    if search_query:
        users_query = users_query.filter(
            db.or_(
                User.FullName.ilike(f'%{search_query}%'),
                User.Email.ilike(f'%{search_query}%')
            )
    )
    users = users_query.all()
    return render_template('settings.html', users=users, search_query=search_query)

@routes_bp.route('/add_user', methods=['POST'])
def add_user():
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_settings'))

    email = request.form.get('email')
    password = request.form.get('password')
    fullname = request.form.get('fullname')

    if User.query.filter_by(Email=email).first():
        flash("User already exists", "warning")
    else:
        new_user = User(Email=email, Passhash=generate_password_hash(password), FullName=fullname)
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully", "success")

    return redirect(url_for('routes.admin_settings'))

@routes_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('routes.admin_settings'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted", "success")
    else:
        flash("User not found", "danger")

    return redirect(url_for('routes.admin_settings'))



@routes_bp.route('/search')
def search():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('routes.login', role='admin'))
    
    query = request.args.get('query', '').strip()
    subjects = {}
    
    try:
        if query:
            subject_results = Subject.query.filter(
                db.or_(
                    Subject.SubName.ilike(f'%{query}%'),
                    Subject.Sub_Description.ilike(f'%{query}%')
                )
            ).all()
            chapter_results = Chapter.query.filter(
                db.or_(
                    Chapter.Ch_name.ilike(f'%{query}%'),
                    Chapter.Ch_description.ilike(f'%{query}%')
                )
            ).all()
            for subject in subject_results:
                if subject not in subjects:
                    subjects[subject] = []
                subjects[subject].extend(
                    Chapter.query.filter_by(Sub_id=subject.Sub_id).all()
                )
            
            for chapter in chapter_results:
                subject = Subject.query.get(chapter.Sub_id)
                if subject not in subjects:
                    subjects[subject] = []
                if chapter not in subjects[subject]:
                    subjects[subject].append(chapter)
        else:
            all_subjects = Subject.query.all()
            for subject in all_subjects:
                subjects[subject] = Chapter.query.filter_by(Sub_id=subject.Sub_id).all()
                
        return render_template('admin_dashboard.html', 
                           subjects=subjects,
                           search_query=query)
        
    except Exception as e:
        flash(f"Error searching: {str(e)}", "danger")
        return redirect(url_for('routes.admin_dashboard'))
    
    
@routes_bp.route('/summary')
def summary():
    """User performance summary route"""
    user_id = session.get('user_id')  
    if not user_id:
        return "User not authenticated", 403
    scores = Score.query.filter_by(User_id=user_id).all()

    if not scores:
        return render_template('performance_summary.html', line_chart=None, bar_chart=None, pie_chart=None)
    
    timestamps = [score.Timestamp.strftime('%Y-%m-%d') for score in scores]
    total_scores = [score.Total_scored for score in scores]

    def create_chart(fig, chart_type):
        img = io.BytesIO()
        fig.tight_layout()
        fig.savefig(img, format='png')
        img.seek(0)
        chart = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)
        return chart

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(timestamps, total_scores, marker='o', linestyle='-', color='blue')
    ax1.set_title('Scores Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Score')
    ax1.grid(True)
    plt.xticks(rotation=45)
    line_chart = create_chart(fig1, "line")

    quizzes = Quiz.query.join(Score, Quiz.Q_id == Score.Q_id).filter(Score.User_id == user_id).all()
    quiz_ids = [quiz.Q_id for quiz in quizzes]
    total_marks = [quiz.Total_marks for quiz in quizzes]
    user_scores = {score.Q_id: score.Total_scored for score in scores}
    bar_scores = [user_scores.get(qid, 0) for qid in quiz_ids]
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(quiz_ids, total_marks, label='Total Marks', color='gray')
    ax2.bar(quiz_ids, bar_scores, label='User Scores', color='green')
    ax2.set_title('User Score vs Total Marks')
    ax2.set_xlabel('Quiz ID')
    ax2.set_ylabel('Marks')
    ax2.legend()
    bar_chart = create_chart(fig2, "bar")
    passed = sum(1 for score in scores if score.Total_scored >= 0.5 * Quiz.query.get(score.Q_id).Total_marks)
    failed = len(scores) - passed

    fig3, ax3 = plt.subplots(figsize=(7, 7))
    labels = ['Passed', 'Failed']
    sizes = [passed, failed]
    colors = ['#4CAF50', '#FF6347']
    ax3.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    ax3.set_title('Pass vs Fail Distribution')
    pie_chart = create_chart(fig3, "pie")

    return render_template(
        'summary.html',
        line_chart=line_chart,
        bar_chart=bar_chart,
        pie_chart=pie_chart
    )