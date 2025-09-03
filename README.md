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

## 🎥 Demo Video  

[![Quiz Management System Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID "Quiz Management System Demo")  

*(Replace `YOUR_VIDEO_ID` with your actual YouTube demo link)*  

---

## 🏗️ System Architecture  

```mermaid
flowchart TD
    %% Users
    A[User] -->|Login/Register| B[Flask Application]
    G[Admin] -->|Login| B

    %% Flask Core
    B[Flask Application] --> C[Authentication Layer (Flask-Login + Werkzeug)]
    B --> D[Database Layer (SQLAlchemy ORM)]
    B --> E[Frontend Layer (Jinja2 + Bootstrap)]

    %% Database
    D --> F[(SQLite Database)]
    F -->|Stores Data| H[(Subjects, Chapters, Quizzes, Questions, Options, Scores)]
