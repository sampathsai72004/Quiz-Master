# 📘 Quiz Management System  

*An intelligent and user-friendly platform to manage quizzes with Admin & User roles.*  

---

## 🚀 Overview  

The **Quiz Management System** is a Flask-based web application that allows administrators to manage subjects, chapters, quizzes, and questions while enabling users to take quizzes, track their progress, and improve learning outcomes. With secure authentication, dynamic rendering, and responsive design, it ensures a seamless experience for both educators and learners.  

---

## 🎯 Why Quiz Management System?  

- **For Admins:**  
  Effortlessly create and manage subjects, chapters, quizzes, and questions. Monitor student performance with detailed reports.  

- **For Users:**  
  Register, take quizzes, track scores, and reattempt quizzes. Get instant feedback and detailed result summaries.  

---

## 🌟 Key Features  

- **🔐 Authentication & Security:** Secure login with password hashing and session management.  
- **👨‍🏫 Admin Dashboard:** CRUD operations for subjects, chapters, quizzes, questions, and options.  
- **👩‍🎓 User Portal:** Attempt quizzes with timers, view results, and track performance history.  
- **📊 Analytics:** Score tracking and detailed performance reports.  
- **🖥️ Modern UI:** Responsive Bootstrap-based frontend with dynamic Jinja2 templates.  
- **🗂️ Database Management:** Powered by SQLite & SQLAlchemy ORM.  

---

## 🛠️ Technology Stack  

- **Programming Language:** Python  
- **Backend Framework:** Flask  
- **Frontend:** HTML5, CSS3, Bootstrap, JavaScript  
- **Database:** SQLite (via SQLAlchemy ORM)  
- **Authentication:** Flask-Login + Werkzeug Security  
- **Templating Engine:** Jinja2  

---

## ⚙️ How It Works  

1. **User/Admin Authentication:** Secure login and registration.  
2. **Admin Role:** Create and manage quizzes, questions, and options.  
3. **User Role:** Attempt quizzes, submit answers, and view results.  
4. **Result Analysis:** Store scores in the database and display progress history.  

---

## 🎓 Benefits & Impact  

| Stakeholder     | Benefits                                                   |
|-----------------|------------------------------------------------------------|
| Admins          | Simplifies quiz management, easy tracking of student scores |
| Users           | Engaging quiz experience, score history, learning feedback |
| Institutions    | Efficient learning tool, scalable and lightweight system   |  

---

## 🗂️ Database Schema  

### Tables  

1. **Admin** – manages subjects, chapters, quizzes, and questions  
2. **Users** – stores student details and login credentials  
3. **Subjects** – defines quiz subjects  
4. **Chapters** – associated with subjects  
5. **Quizzes** – linked with chapters, contains metadata  
6. **Questions** – linked with quizzes  
7. **Options** – multiple-choice options for questions  
8. **Scores** – stores quiz performance of users  

### Relationships  

- One Subject → Many Chapters  
- One Chapter → Many Quizzes  
- One Quiz → Many Questions  
- One Question → Many Options  
- One Quiz → Many Scores  
- One User → Many Scores  

---

## 🎥 Demo Video  

[Quiz Management System Demo](https://drive.google.com/file/d/1tXBVyJkyy_2uUmiyRAD5TyICKRfe3v3P/view?usp=sharing "Quiz Management System Demo")  


---

## 🏗️ System Architecture   

[System Architecture](https://drive.google.com/file/d/1VVSneDkPQX2exfqetfiTVkD-YJoCNYT5/view?usp=sharing)
