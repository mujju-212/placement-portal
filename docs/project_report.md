# Project Report - Placement Portal Application

---

## 1. Student Details

```
Name         : [Your Full Name]
Roll Number  : [Your Roll Number]
Email        : [Your IITM Email]

About Me:
I am a student of the IITM BS Degree program.
I enjoy building web applications and learning
new technologies through hands-on projects.
```

---

## 2. Project Details

**Project Title:** Placement Portal Application

**Problem Statement:**

Institutes need efficient systems to manage campus recruitment activities involving companies, students, and placement drives. Currently, many institutes rely on spreadsheets, emails, or manual processes, which makes it difficult to manage company approvals, track student applications, avoid duplicate registrations, and maintain placement records. The task was to build a Placement Portal Application where Admin (Institute), Company, and Student can interact with the system based on their roles.

**Approach:**

I started by understanding the three roles in the system — Admin, Company, and Student. I planned the database schema with 5 tables (User, Company, Student, PlacementDrive, Application) and mapped out all 30 routes before writing any code. The backend was built using Flask with SQLAlchemy ORM for database operations. Each role has its own dashboard with session-based access control — users cannot access pages of other roles. Key business rules like company approval before login, drive approval before student visibility, duplicate application prevention, and cascade operations on blacklisting were implemented in the route handlers. The frontend uses Bootstrap 5 with Jinja2 templates organized by role.

---

## 3. AI/LLM Declaration

I used ChatGPT as a supporting tool during this project. My use of AI was limited to the following areas:

- **Brainstorming:** I used it to think through the project structure and understand how to connect the three roles together before I started coding.
- **Code Fixing:** When I ran into bugs or errors, I described the problem and used AI suggestions to understand what went wrong and fix it.
- **CSS Styling:** I took help for basic styling ideas like card layout and color choices to make the UI look clean.
- **HTML Structure:** For a few template pages, I used AI to check if my HTML structure was correct.

The overall extent of AI usage is around 20-25%. All the main logic, route handling, database design, and final integration was done by me. I understood every part of the code before using it.

---

## 4. Frameworks and Libraries Used

| Technology / Library | Purpose |
|---|---|
| Flask 3.1.0 | Core backend web framework for routing and request handling |
| Flask-SQLAlchemy 3.1.1 | Object Relational Mapper for SQLite database |
| SQLite | Lightweight local database for storing all application data |
| Jinja2 | Template engine for rendering dynamic HTML pages |
| Bootstrap 5.3.0 | Frontend styling and responsive layout |
| Bootstrap Icons 1.10.0 | Icons used throughout the UI for better UX |
| HTML5 / CSS3 | Building and styling all web pages |
| Python OS Module | Handling resume file uploads and folder creation |

---

## 5. Database Schema / ER Diagram

**Tables:**

- **User** — stores login credentials and role for all users (id, username, email, password, role, is_active)
- **Company** — stores company profile and approval status (id, user_id, company_name, hr_contact, website, description, approval_status)
- **Student** — stores student profile details (id, user_id, full_name, email, phone, department, cgpa, resume_filename)
- **PlacementDrive** — stores placement drives created by companies (id, company_id, drive_name, job_title, job_description, eligibility, deadline, salary, location, status)
- **Application** — stores student applications for drives (id, student_id, drive_id, applied_date, status)

**Relationships:**

- One-to-One → User → Company
- One-to-One → User → Student
- One-to-Many → Company → PlacementDrive
- One-to-Many → Student → Application
- One-to-Many → PlacementDrive → Application

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────────────┐
│    user       │       │    company        │       │   placement_drive     │
├──────────────┤       ├──────────────────┤       ├──────────────────────┤
│ id       (PK)│──┐    │ id           (PK)│──┐    │ id              (PK) │
│ username     │  │    │ user_id      (FK)│←─┘    │ company_id      (FK) │←─┐
│ email        │  │    │ company_name     │       │ drive_name           │  │
│ password     │  │    │ hr_contact       │       │ job_title            │  │
│ role         │  │    │ website          │       │ job_description      │  │
│ is_active    │  │    │ description      │       │ eligibility          │  │
│ created_at   │  │    │ approval_status  │       │ deadline             │  │
└──────────────┘  │    │ created_at       │       │ salary, location     │  │
                  │    └──────────────────┘       │ status, created_at   │  │
                  │                               └──────────────────────┘  │
                  │    ┌──────────────────┐                                 │
                  │    │    student        │       ┌──────────────────────┐  │
                  │    ├──────────────────┤       │    application        │  │
                  └──→ │ id           (PK)│──┐    ├──────────────────────┤  │
                       │ user_id      (FK)│←─┘    │ id              (PK) │  │
                       │ full_name        │       │ student_id      (FK) │←─┤
                       │ email, phone     │       │ drive_id        (FK) │←─┘
                       │ department, cgpa │       │ applied_date         │
                       │ resume_filename  │       │ status               │
                       │ created_at       │       └──────────────────────┘
                       └──────────────────┘
```

*(Insert ER diagram image here — can be created using dbdiagram.io or draw.io)*

---

## 6. API Resource Endpoints

Since this project uses Flask with server-side rendering, all interactions happen through HTML form submissions and page routes. There are no separate REST API endpoints — all data is rendered directly in Jinja2 templates.

| Route | Method | Role | Description |
|---|---|---|---|
| `/` | GET | Public | Redirects to login page |
| `/login` | GET, POST | Public | Login for all roles |
| `/register` | GET, POST | Public | Register as student or company |
| `/logout` | GET | All | Logout and clear session |
| `/admin/dashboard` | GET | Admin | Dashboard with stats and pending approvals |
| `/admin/companies` | GET | Admin | View and search all companies |
| `/admin/company/<id>/approve` | POST | Admin | Approve a company registration |
| `/admin/company/<id>/reject` | POST | Admin | Reject a company registration |
| `/admin/company/<id>/blacklist` | POST | Admin | Blacklist company and close all drives |
| `/admin/company/<id>/delete` | POST | Admin | Delete company permanently |
| `/admin/students` | GET | Admin | View and search all students |
| `/admin/student/<id>/blacklist` | POST | Admin | Blacklist a student account |
| `/admin/student/<id>/delete` | POST | Admin | Delete student permanently |
| `/admin/drives` | GET | Admin | View all placement drives |
| `/admin/drive/<id>/approve` | POST | Admin | Approve a placement drive |
| `/admin/drive/<id>/reject` | POST | Admin | Reject a placement drive |
| `/admin/applications` | GET | Admin | View all applications |
| `/admin/search` | GET | Admin | Search students or companies |
| `/company/dashboard` | GET | Company | Company dashboard with drives |
| `/company/drive/create` | GET, POST | Company | Create new placement drive |
| `/company/drive/<id>/edit` | GET, POST | Company | Edit existing drive |
| `/company/drive/<id>/delete` | POST | Company | Delete a drive |
| `/company/drive/<id>/close` | POST | Company | Close a drive |
| `/company/drive/<id>/applications` | GET | Company | View applications for a drive |
| `/company/application/<id>/update` | POST | Company | Update application status |
| `/student/dashboard` | GET | Student | Dashboard with approved drives |
| `/student/profile` | GET, POST | Student | Edit profile and upload resume |
| `/student/drive/<id>` | GET | Student | View drive details |
| `/student/drive/<id>/apply` | POST | Student | Apply for a drive |
| `/student/history` | GET | Student | View complete application history |

---

## 7. Architecture and Features

**Architecture Overview:**

```
placement_portal/
├── app.py              → Main Flask application with all routes and logic
├── models.py           → Database models using SQLAlchemy (User, Company,
│                         Student, PlacementDrive, Application)
├── init_db.py          → Creates database tables and admin user
├── requirements.txt    → Python dependencies (Flask, Flask-SQLAlchemy)
├── README.md           → Project documentation and setup instructions
├── templates/
│   ├── base.html       → Common layout with navbar, flash messages
│   ├── login.html      → Login page for all roles
│   ├── register.html   → Registration page (Student / Company)
│   ├── admin/          → Admin dashboard, companies, students, drives,
│   │                     applications, search templates
│   ├── company/        → Company dashboard, create/edit drive,
│   │                     view applications templates
│   └── student/        → Student dashboard, profile, drive detail,
│                         history templates
└── static/
    ├── css/style.css   → Custom styles, badge colors, sidebar, stat cards
    └── uploads/
        └── resumes/    → Uploaded student resume files (PDF)
```

**Implemented Core Features:**

- Login and logout system for all three roles (Admin, Company, Student)
- Separate registration for students and companies (no admin registration)
- Admin is pre-created in the database via `init_db.py`
- Admin dashboard shows total count of students, companies, drives and applications
- Admin can approve or reject company registrations
- Admin can approve or reject placement drives
- Admin can blacklist companies — all their drives are automatically closed and account deactivated
- Admin can blacklist or delete student accounts
- Admin can search students by name, email or phone
- Admin can search companies by name
- Company can only login after admin approves their registration
- Company dashboard shows company profile, all drives with applicant count per drive
- Company can create, edit, close and delete placement drives
- Only approved companies can create drives
- Edited drives reset to pending status for re-approval by admin
- Company can view student applications and update status (Shortlisted / Selected / Rejected)
- Company can view student resume from the applications page
- Students can register and login directly without approval
- Student dashboard shows only approved placement drives
- Students can view full drive details and apply
- Duplicate applications prevented — student cannot apply twice to same drive
- Students can edit their profile and upload resume (PDF)
- Students can view their application status on dashboard
- Students can view complete application history with summary cards (total, shortlisted, selected, rejected)

**Additional Features:**

- Resume upload stored on server and viewable/downloadable by company
- Flash messages shown for every user action across all roles
- Application history page with summary counts (shortlisted, selected, rejected cards)
- Role-based access control on every route — users cannot access pages of other roles
- Session-based authentication with proper logout and session clearing
- Sidebar navigation on all dashboard pages for easy navigation
- Status badges with color coding (pending=yellow, approved=green, rejected=red, blacklisted=grey)
- Responsive UI using Bootstrap 5 grid system

---

## 8. Video Presentation

```
Video Link: [ Paste your Google Drive video link here ]

Note: The video is set to "Anyone with the link can view"
```
