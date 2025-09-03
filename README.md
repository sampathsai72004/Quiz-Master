<h1 align="center">📘 Quiz Management System</h1>

<p align="center">
  A powerful and user-friendly <b>Flask-based Quiz Platform</b> with <b>Admin & User roles</b>, 
  secure authentication, and complete content management.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Flask-Framework-green?logo=flask" />
  <img src="https://img.shields.io/badge/SQLite-Database-orange?logo=sqlite" />
  <img src="https://img.shields.io/badge/Bootstrap-Frontend-purple?logo=bootstrap" />
</p>

---

## 🎥 Demo Video  

> 📺 Click below to watch the demo of the project:  

[![Quiz Management System Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID "Quiz Management System Demo")

*(Replace `YOUR_VIDEO_ID` with your YouTube video link ID. If you want a local `.mp4` or `.gif`, upload it to the repo and use `![Demo](demo.mp4)`)*

---

## 📖 Overview  

The **Quiz Management System** is designed for **educational institutions, trainers, and learners** to manage quizzes efficiently.  
It offers:  

- **Admin Panel** 🛠️ → Manage subjects, chapters, quizzes, questions, and answer options.  
- **User Dashboard** 🎓 → Take quizzes, track scores, and analyze performance.  
- **Secure Authentication** 🔐 → Role-based login (Admin/User).  

This ensures a **complete learning ecosystem** where admins can create structured content, and students can engage through interactive quizzes.  

---

## 🚀 Features  

### 🔐 Authentication & Security  
✔️ Role-based login system (**Admin/User**)  
✔️ Password hashing with **Werkzeug Security**  
✔️ Session management with **Flask-Login**  

### 👨‍🏫 Admin Features  
✔️ Add, edit, delete **Subjects, Chapters, Quizzes, Questions, and Options**  
✔️ Search & filter quizzes easily  
✔️ Track user performances and scores  

*Example Admin Workflow:*  
1. Create a **Subject** (e.g., *Mathematics*).  
2. Add **Chapters** (e.g., *Algebra, Geometry*).  
3. Add **Quizzes** under each chapter.  
4. Add **Questions** with multiple choice **Options**.  
5. Mark the correct answers ✅  

### 👩‍🎓 User Features  
✔️ Register and log in to the platform  
✔️ Explore **Subjects** and **Chapters**  
✔️ Take quizzes with a **timer** ⏳  
✔️ View **past scores** and performance analysis  
✔️ Reattempt quizzes with previous results stored  

*Example User Workflow:*  
1. Log in as a user.  
2. Choose a **subject → chapter → quiz**.  
3. Answer questions within the **time limit**.  
4. Submit and view score instantly.  
5. Check performance summary with **marks & answers**.  

### 🖥️ System Features  
✔️ Clean & responsive **Bootstrap UI**  
✔️ **MVC Architecture** for maintainable code  
✔️ Lightweight **SQLite database** (easy setup, portable)  
✔️ **Dynamic content rendering** with Jinja2 templates  

---

## 🏗️ System Architecture  

```mermaid
flowchart TD
    A[User/Admin] -->|Login| B[Flask Application]
    B -->|Flask-Login| C[Authentication Layer]
    B -->|SQLAlchemy ORM| D[(SQLite Database)]
    B -->|Jinja2 Templates| E[Frontend (Bootstrap UI)]
    D -->|Stores| F[Subjects, Chapters, Quizzes, Questions, Options, Scores]
