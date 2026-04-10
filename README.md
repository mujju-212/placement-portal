# Placement Portal Application

A multi-role campus placement management system that allows Admin (Institute), Company, and Student users to interact with the placement process through dedicated dashboards and workflows.

## Tech Stack

- **Backend:** Flask 3.1.0, Flask-SQLAlchemy 3.1.1
- **Frontend:** Jinja2 Templating, HTML5, Bootstrap 5, CSS
- **Database:** SQLite (programmatically created via `init_db.py`)
- **Language:** Python 3

## How to Run

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Initialize the database and create admin user:**
   ```
   python init_db.py
   ```

3. **Run the application:**
   ```
   python app.py
   ```

4. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

## Default Admin Credentials

- **Username:** `admin`
- **Password:** `admin123`

> Admin is pre-created via `init_db.py`. There is no admin registration option.

## Roles & Features

### Admin (Institute Placement Cell)
- Dashboard with total counts: Students, Companies, Drives, Applications
- Approve / Reject company registrations
- Approve / Reject placement drives
- View and manage all students, companies, and placement drives
- Search students by name, email, or phone
- Search companies by name
- Blacklist or delete student and company accounts

### Company
- Self-register and await admin approval before login
- Create placement drives (only after admin approval)
- Edit, close, or delete their placement drives
- View student applications for their drives
- Update application status (Shortlisted / Selected / Rejected)

### Student
- Self-register and login
- View all approved placement drives
- View drive details and apply
- Edit profile and upload resume (PDF)
- View application status and complete placement history

## Key Business Rules

- Companies cannot login until approved by admin
- Only approved companies can create placement drives
- Drives require admin approval before students can see them
- Students cannot apply to the same drive twice
- Blacklisting a company closes all its drives and deactivates the account
- Edited drives reset to pending status for re-approval

## Database Schema

| Table | Key Fields |
|---|---|
| **User** | id, username, email, password, role, is_active |
| **Company** | id, user_id (FK), company_name, hr_contact, website, description, approval_status |
| **Student** | id, user_id (FK), full_name, email, phone, department, cgpa, resume_filename |
| **PlacementDrive** | id, company_id (FK), drive_name, job_title, job_description, eligibility, deadline, salary, location, status |
| **Application** | id, student_id (FK), drive_id (FK), applied_date, status |

## Folder Structure

```
placement_portal/
├── app.py                  # Main Flask application with all routes
├── models.py               # SQLAlchemy database models
├── init_db.py              # Database initialization + admin creation
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   ├── base.html           # Common layout (navbar, flash messages)
│   ├── login.html          # Login page
│   ├── register.html       # Registration page (Student / Company)
│   ├── admin/              # Admin dashboard, companies, students, drives, applications, search
│   ├── company/            # Company dashboard, create/edit drive, view applications
│   └── student/            # Student dashboard, profile, drive detail, history
└── static/
    ├── css/style.css        # Custom styles
    └── uploads/resumes/     # Uploaded student resumes
```

## Notes

- Resume uploads are stored in `static/uploads/resumes/`
- Database file is created at `instance/placement.db` by Flask-SQLAlchemy
- All database tables are created programmatically (no manual DB setup)
