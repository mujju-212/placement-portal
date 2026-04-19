# Full Project Planning Before Code

Let me first show you the complete structure and plan.

---

## Folder Structure

```
placement_portal/
├── app.py                  ← main flask app
├── models.py               ← database models
├── init_db.py             ← creates admin + tables
│
├── templates/
│   ├── base.html           ← common layout
│   ├── login.html
│   ├── register.html
│   │
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── companies.html
│   │   ├── students.html
│   │   ├── drives.html
│   │   └── applications.html
│   │
│   ├── company/
│   │   ├── dashboard.html
│   │   ├── create_drive.html
│   │   ├── edit_drive.html
│   │   └── applications.html
│   │
│   └── student/
│       ├── dashboard.html
│       ├── profile.html
│       ├── drive_detail.html
│       └── history.html
│
└── static/
    ├── css/
    │   └── style.css
    └── uploads/
        └── resumes/        ← student resumes stored here
```

---

## Database Tables Plan

```
User Table
----------
id, username, email, password, role (admin/company/student), is_active

Company Table
-------------
id, user_id(FK), company_name, hr_contact, website, 
description, approval_status (pending/approved/rejected)

Student Table
-------------
id, user_id(FK), full_name, email, phone, department, 
cgpa, resume_filename

PlacementDrive Table
--------------------
id, company_id(FK), drive_name, job_title, job_description,
eligibility, deadline, salary, location,
status (pending/approved/closed)

Application Table
-----------------
id, student_id(FK), drive_id(FK), applied_date,
status (applied/shortlisted/selected/rejected)
```

---

## Routes Plan

```
PUBLIC ROUTES
-------------
GET  /              → redirect to login
GET  /login         → login page
POST /login         → handle login
GET  /register      → register page
POST /register      → handle register
GET  /logout        → logout

ADMIN ROUTES
------------
GET  /admin/dashboard
GET  /admin/companies
POST /admin/company/<id>/approve
POST /admin/company/<id>/reject
POST /admin/company/<id>/blacklist
POST /admin/company/<id>/delete
GET  /admin/students
POST /admin/student/<id>/blacklist
POST /admin/student/<id>/delete
GET  /admin/drives
POST /admin/drive/<id>/approve
POST /admin/drive/<id>/reject
GET  /admin/applications
GET  /admin/search

COMPANY ROUTES
--------------
GET  /company/dashboard
GET  /company/drive/create
POST /company/drive/create
GET  /company/drive/<id>/edit
POST /company/drive/<id>/edit
POST /company/drive/<id>/delete
POST /company/drive/<id>/close
GET  /company/drive/<id>/applications
POST /company/application/<id>/update

STUDENT ROUTES
--------------
GET  /student/dashboard
GET  /student/profile
POST /student/profile
GET  /student/drive/<id>
POST /student/drive/<id>/apply
GET  /student/history
```

---

## What Each Role Sees

### Admin Dashboard Shows
- Total Students count
- Total Companies count
- Total Drives count
- Total Applications count
- Pending company approvals
- Pending drive approvals

### Company Dashboard Shows
- Company details
- Their drives with applicant count
- Pending / Active / Closed drives

### Student Dashboard Shows
- All approved drives
- Their applied drives with status
- Quick link to history and profile

---

## Key Logic Points

```
1. Login checks role → redirects to correct dashboard
2. Company cannot login if not approved
3. Company cannot create drive if not approved
4. Student cannot apply twice to same drive
5. Student sees only approved drives
6. If company blacklisted → all drives closed
7. Admin pre-exists in database via init_db.py
8. Resume stored in static/uploads/resumes/
```

---

## Now Confirm Before I Start Coding

The code will be in **2 Parts**:

**Part 1 will contain:**
- `models.py` - all database tables
- `init_db.py` - creates tables + admin user
- `app.py` - all routes (complete)
- `base.html` - common layout
- `login.html` and `register.html`
- `style.css`

**Part 2 will contain:**
- All Admin templates
- All Company templates
- All Student templates

---

> ✅ Plan looks good?
> 
> Just reply **"yes start part 1"** and I will give complete Part 1 code