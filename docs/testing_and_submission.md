# Complete Testing Document & Submission Guide

---

## PART A - HOW TO TEST EVERYTHING

---

### Step 1 - Setup Before Testing

```
1. Open terminal/command prompt
2. Go to your project folder
3. Run these commands:

pip install flask flask-sqlalchemy
python init_db.py
python app.py

4. Open browser → http://127.0.0.1:5000
```

---

## TEST 1 - Database Creation Test

```
WHAT TO CHECK:
After running init_db.py, check if these files exist:

placement_portal/
└── instance/
    └── placement.db    ← this file must be created

HOW TO VERIFY:
Run python init_db.py
You should see:
  "Admin created successfully!"
  "Username: admin"
  "Password: admin123"
  "Database tables created successfully!"

PASS = File placement.db exists in instance folder
FAIL = Error message or file not created
```

---

## TEST 2 - Admin Login Test

```
URL: http://127.0.0.1:5000/login

TEST CASE 1 - Correct Admin Login
--------------------------------
Username: admin
Password: admin123
Expected: Redirects to /admin/dashboard
Result: PASS / FAIL

TEST CASE 2 - Wrong Password
--------------------------------
Username: admin
Password: wrongpass
Expected: Shows "Invalid username or password" message
Result: PASS / FAIL

TEST CASE 3 - Empty Fields
--------------------------------
Username: (empty)
Password: (empty)
Expected: Shows "Please fill all fields" message
Result: PASS / FAIL

TEST CASE 4 - Admin Cannot Register
--------------------------------
Go to /register
Try to register with role = admin
Expected: No admin option in dropdown
Result: PASS / FAIL
```

---

## TEST 3 - Student Registration & Login Test

```
URL: http://127.0.0.1:5000/register

TEST CASE 1 - New Student Registration
----------------------------------------
Select Role: Student
Username: teststudent1
Email: student1@test.com
Password: test123
Full Name: Test Student One
Phone: 9876543210
Department: Computer Science
CGPA: 8.5
Click Register
Expected: Success message + redirect to login
Result: PASS / FAIL

TEST CASE 2 - Duplicate Username
----------------------------------------
Try registering again with:
Username: teststudent1 (same as above)
Expected: "Username already taken" error
Result: PASS / FAIL

TEST CASE 3 - Duplicate Email
----------------------------------------
Username: teststudent2
Email: student1@test.com (same email)
Expected: "Email already registered" error
Result: PASS / FAIL

TEST CASE 4 - Student Login
----------------------------------------
Username: teststudent1
Password: test123
Expected: Redirects to /student/dashboard
Result: PASS / FAIL

TEST CASE 5 - Student Cannot Access Admin Page
----------------------------------------
While logged in as student, go to:
http://127.0.0.1:5000/admin/dashboard
Expected: "Access denied" + redirect to login
Result: PASS / FAIL
```

---

## TEST 4 - Company Registration & Approval Test

```
URL: http://127.0.0.1:5000/register

TEST CASE 1 - New Company Registration
----------------------------------------
Select Role: Company
Username: testcompany1
Email: company1@test.com
Password: test123
Company Name: Tech Corp
HR Contact: hr@techcorp.com
Website: https://techcorp.com
Description: A tech company
Click Register
Expected: "Company registered! Wait for admin approval" message
Result: PASS / FAIL

TEST CASE 2 - Company Cannot Login Before Approval
----------------------------------------
Username: testcompany1
Password: test123
Expected: "Your company registration is pending admin approval" message
Result: PASS / FAIL

TEST CASE 3 - Admin Approves Company
----------------------------------------
Login as admin (admin / admin123)
Go to /admin/companies
Find Tech Corp → Click Approve
Expected: "Tech Corp has been approved!" success message
Status changes to APPROVED
Result: PASS / FAIL

TEST CASE 4 - Company Login After Approval
----------------------------------------
Logout admin
Login as testcompany1 / test123
Expected: Redirects to /company/dashboard
Result: PASS / FAIL

TEST CASE 5 - Admin Rejects Company
----------------------------------------
Register another company:
Username: badcompany
Email: bad@company.com
Password: test123
Company Name: Bad Corp

Login as admin → Go to companies
Click Reject on Bad Corp
Expected: Status changes to REJECTED
Result: PASS / FAIL
```

---

## TEST 5 - Admin Dashboard Test

```
URL: http://127.0.0.1:5000/admin/dashboard
Login: admin / admin123

TEST CASE 1 - Dashboard Counts Show Correctly
----------------------------------------
Check these 4 numbers are visible:
- Total Students count
- Total Companies count
- Total Drives count
- Total Applications count
Expected: All 4 stat cards visible with correct numbers
Result: PASS / FAIL

TEST CASE 2 - Pending Approvals Visible
----------------------------------------
Check Pending Company Approvals section
Check Pending Drive Approvals section
Expected: Pending items show with Approve/Reject buttons
Result: PASS / FAIL
```

---

## TEST 6 - Admin Company Management Test

```
URL: http://127.0.0.1:5000/admin/companies
Login: admin / admin123

TEST CASE 1 - Search Company by Name
----------------------------------------
Type "Tech" in search box → Click Search
Expected: Tech Corp appears in results
Result: PASS / FAIL

TEST CASE 2 - Blacklist Company
----------------------------------------
Find Tech Corp → Click Blacklist → Confirm
Expected: 
- "Tech Corp has been blacklisted" message
- Status changes to BLACKLISTED
- Company user cannot login anymore
Result: PASS / FAIL

TEST CASE 3 - All Drives Closed When Blacklisted
----------------------------------------
After blacklisting Tech Corp:
Go to /admin/drives
Check if all Tech Corp drives are CLOSED
Expected: All drives show CLOSED status
Result: PASS / FAIL

TEST CASE 4 - Delete Company
----------------------------------------
Register a new dummy company
Admin approves it
Admin deletes it from companies page
Expected: Company removed from list
Result: PASS / FAIL
```

---

## TEST 7 - Admin Student Management Test

```
URL: http://127.0.0.1:5000/admin/students
Login: admin / admin123

TEST CASE 1 - View All Students
----------------------------------------
Expected: List of all registered students visible
Result: PASS / FAIL

TEST CASE 2 - Search Student by Name
----------------------------------------
Type "Test Student" in search → Click Search
Expected: Matching students appear
Result: PASS / FAIL

TEST CASE 3 - Search Student by Email
----------------------------------------
Type "student1@test.com" in search
Expected: That student appears
Result: PASS / FAIL

TEST CASE 4 - Blacklist Student
----------------------------------------
Find teststudent1 → Click Blacklist → Confirm
Expected: Status shows "Blacklisted"
Try to login as that student
Expected: "Your account has been deactivated" message
Result: PASS / FAIL

TEST CASE 5 - Delete Student
----------------------------------------
Find a student → Click Delete → Confirm
Expected: Student removed from list
Result: PASS / FAIL
```

---

## TEST 8 - Placement Drive Creation Test

```
First: Make sure a company is approved and logged in

URL: http://127.0.0.1:5000/company/drive/create
Login: testcompany1 / test123

TEST CASE 1 - Create New Drive
----------------------------------------
Drive Name: Campus Drive 2025
Job Title: Software Developer
Job Description: Building web applications
Eligibility: CGPA > 7.0
Deadline: 2025-12-31
Salary: 6 LPA
Location: Bangalore
Click Create Drive
Expected: "Drive created! Waiting for admin approval" message
Result: PASS / FAIL

TEST CASE 2 - Drive Shows as Pending
----------------------------------------
Go to /company/dashboard
Drive should show status: PENDING
Expected: Drive visible with PENDING badge
Result: PASS / FAIL

TEST CASE 3 - Admin Approves Drive
----------------------------------------
Login as admin
Go to /admin/drives or dashboard
Find "Campus Drive 2025" → Click Approve
Expected: Status changes to APPROVED
Result: PASS / FAIL

TEST CASE 4 - Admin Rejects Drive
----------------------------------------
Create another drive
Admin goes to drives → Click Reject
Expected: Status changes to REJECTED
Result: PASS / FAIL

TEST CASE 5 - Empty Required Fields
----------------------------------------
Try creating drive with empty Drive Name
Expected: Form validation error, drive not created
Result: PASS / FAIL
```

---

## TEST 9 - Company Drive Management Test

```
Login: testcompany1 / test123

TEST CASE 1 - Edit Drive
----------------------------------------
Go to dashboard → Click Edit on a drive
Change Job Title to "Senior Developer"
Click Save Changes
Expected: 
- Drive updated
- Status goes back to PENDING (needs re-approval)
Result: PASS / FAIL

TEST CASE 2 - Close Drive
----------------------------------------
Go to dashboard → Click Close on approved drive
Confirm
Expected: Drive status changes to CLOSED
Result: PASS / FAIL

TEST CASE 3 - Delete Drive
----------------------------------------
Create a test drive
Go to dashboard → Click Delete → Confirm
Expected: Drive removed from list
Result: PASS / FAIL

TEST CASE 4 - Applicant Count Shows
----------------------------------------
After students apply (see TEST 10)
Go to company dashboard
Expected: Number next to each drive shows correct count
Result: PASS / FAIL
```

---

## TEST 10 - Student Apply Test

```
Login: teststudent1 / test123
(First make sure there is an approved drive)

TEST CASE 1 - View Approved Drives
----------------------------------------
Go to /student/dashboard
Expected: Only APPROVED drives visible
PENDING/REJECTED/CLOSED drives should NOT appear
Result: PASS / FAIL

TEST CASE 2 - View Drive Details
----------------------------------------
Click "View & Apply" on any drive
Expected: Drive detail page shows:
- Job Title
- Job Description
- Eligibility
- Salary
- Location
- Deadline
- Company Name
- Apply Now button
Result: PASS / FAIL

TEST CASE 3 - Apply for Drive
----------------------------------------
Click "Apply Now" → Confirm
Expected: 
- "Application submitted successfully!" message
- Redirects to dashboard
- Drive now shows "Already Applied" badge
Result: PASS / FAIL

TEST CASE 4 - Prevent Duplicate Application
----------------------------------------
Try to apply for same drive again
Go to drive detail page
Expected: 
- "Apply Now" button NOT visible
- Shows "You have already applied" message with current status
Result: PASS / FAIL

TEST CASE 5 - View Application Status on Dashboard
----------------------------------------
Go to student dashboard
Check "My Applications" section
Expected: Applied drive shows with status "APPLIED"
Result: PASS / FAIL
```

---

## TEST 11 - Company Review Applications Test

```
Login: testcompany1 / test123
(After student has applied)

TEST CASE 1 - View Applications for Drive
----------------------------------------
Go to dashboard → Click "View Apps" on drive
Expected: List of students who applied shown
Result: PASS / FAIL

TEST CASE 2 - Shortlist Student
----------------------------------------
Find a student application
Change status dropdown to "Shortlisted"
Click Save
Expected: Status badge changes to SHORTLISTED
Result: PASS / FAIL

TEST CASE 3 - Select Student
----------------------------------------
Change status to "Selected" → Click Save
Expected: Status badge changes to SELECTED
Result: PASS / FAIL

TEST CASE 4 - Reject Student
----------------------------------------
Change status to "Rejected" → Click Save
Expected: Status badge changes to REJECTED
Result: PASS / FAIL

TEST CASE 5 - Student Sees Updated Status
----------------------------------------
Logout → Login as teststudent1
Go to dashboard or history
Expected: Application status shows updated value
(Shortlisted / Selected / Rejected)
Result: PASS / FAIL
```

---

## TEST 12 - Student Profile & Resume Test

```
Login: teststudent1 / test123

TEST CASE 1 - Edit Profile
----------------------------------------
Go to /student/profile
Change Full Name, Phone, Department, CGPA
Click Save Profile
Expected: 
- "Profile updated successfully!" message
- Form shows updated values
Result: PASS / FAIL

TEST CASE 2 - Upload Resume
----------------------------------------
Go to /student/profile
Click Choose File → Select a PDF file
Click Save Profile
Expected:
- "Profile updated successfully!" message
- Shows "Resume uploaded: filename.pdf" in green
- View link appears
Result: PASS / FAIL

TEST CASE 3 - View Resume Link
----------------------------------------
Click View link next to resume
Expected: PDF opens in new tab
Result: PASS / FAIL
```

---

## TEST 13 - Student History Test

```
Login: teststudent1 / test123

TEST CASE 1 - View History Page
----------------------------------------
Go to /student/history
Expected:
- Summary cards show correct counts
  (Total Applied, Shortlisted, Selected, Rejected)
- Full history table with all applications
Result: PASS / FAIL

TEST CASE 2 - History Shows All Applications
----------------------------------------
Apply to multiple drives
Check history page
Expected: All applied drives appear in history table
Result: PASS / FAIL
```

---

## TEST 14 - Admin Search Test

```
Login: admin / admin123

TEST CASE 1 - Search Student
----------------------------------------
Go to /admin/search
Select "Search Students"
Type student name → Click Search
Expected: Matching students shown in table
Result: PASS / FAIL

TEST CASE 2 - Search Company
----------------------------------------
Select "Search Companies"
Type company name → Click Search
Expected: Matching companies shown in table
Result: PASS / FAIL

TEST CASE 3 - Empty Search
----------------------------------------
Leave search box empty → Click Search
Expected: No results shown or all results shown
Result: PASS / FAIL
```

---

## TEST 15 - URL Access Control Test

```
These are IMPORTANT security tests

TEST CASE 1 - Student Cannot Access Admin URLs
----------------------------------------
Login as student
Try: http://127.0.0.1:5000/admin/dashboard
Expected: "Access denied" + redirect to login
Result: PASS / FAIL

TEST CASE 2 - Company Cannot Access Admin URLs
----------------------------------------
Login as company
Try: http://127.0.0.1:5000/admin/students
Expected: "Access denied" + redirect to login
Result: PASS / FAIL

TEST CASE 3 - Student Cannot Access Company URLs
----------------------------------------
Login as student
Try: http://127.0.0.1:5000/company/dashboard
Expected: "Access denied" + redirect to login
Result: PASS / FAIL

TEST CASE 4 - Cannot Access Any Page Without Login
----------------------------------------
Logout completely
Try: http://127.0.0.1:5000/admin/dashboard
Expected: Redirect to login page
Result: PASS / FAIL

TEST CASE 5 - Company Cannot Edit Other Company Drive
----------------------------------------
Login as company2 (create second company)
Try to edit company1's drive by URL:
http://127.0.0.1:5000/company/drive/1/edit
Expected: "Access denied" message
Result: PASS / FAIL
```

---

## TEST 16 - All Route URLs Test

```
Test every route exists and works

PUBLIC ROUTES
--------------
GET  /                    → Redirects to login         ✅/❌
GET  /login               → Login page loads           ✅/❌
POST /login               → Login works               ✅/❌
GET  /register            → Register page loads        ✅/❌
POST /register            → Registration works         ✅/❌
GET  /logout              → Logout works               ✅/❌

ADMIN ROUTES
--------------
GET  /admin/dashboard              → Dashboard loads   ✅/❌
GET  /admin/companies              → Companies list    ✅/❌
POST /admin/company/1/approve      → Approves company  ✅/❌
POST /admin/company/1/reject       → Rejects company   ✅/❌
POST /admin/company/1/blacklist    → Blacklists        ✅/❌
POST /admin/company/1/delete       → Deletes company   ✅/❌
GET  /admin/students               → Students list     ✅/❌
POST /admin/student/1/blacklist    → Blacklists student ✅/❌
POST /admin/student/1/delete       → Deletes student   ✅/❌
GET  /admin/drives                 → Drives list       ✅/❌
POST /admin/drive/1/approve        → Approves drive    ✅/❌
POST /admin/drive/1/reject         → Rejects drive     ✅/❌
GET  /admin/applications           → All applications  ✅/❌
GET  /admin/search                 → Search page       ✅/❌

COMPANY ROUTES
--------------
GET  /company/dashboard            → Dashboard loads   ✅/❌
GET  /company/drive/create         → Create form       ✅/❌
POST /company/drive/create         → Creates drive     ✅/❌
GET  /company/drive/1/edit         → Edit form loads   ✅/❌
POST /company/drive/1/edit         → Updates drive     ✅/❌
POST /company/drive/1/delete       → Deletes drive     ✅/❌
POST /company/drive/1/close        → Closes drive      ✅/❌
GET  /company/drive/1/applications → Applications list ✅/❌
POST /company/application/1/update → Updates status    ✅/❌

STUDENT ROUTES
--------------
GET  /student/dashboard            → Dashboard loads   ✅/❌
GET  /student/profile              → Profile loads     ✅/❌
POST /student/profile              → Updates profile   ✅/❌
GET  /student/drive/1              → Drive detail      ✅/❌
POST /student/drive/1/apply        → Applies           ✅/❌
GET  /student/history              → History loads     ✅/❌
```

---

## Quick Test Checklist

```
BEFORE DEMO - RUN THROUGH THIS LIST

SETUP
□ python init_db.py runs without error
□ placement.db file created
□ python app.py runs without error
□ http://127.0.0.1:5000 opens in browser

LOGIN/REGISTER
□ Admin login works (admin/admin123)
□ Student registration works
□ Student login works
□ Company registration works
□ Company cannot login before approval
□ Company can login after admin approves

ADMIN FUNCTIONS
□ Dashboard shows 4 stat counts
□ Can approve company
□ Can reject company
□ Can blacklist company (drives close too)
□ Can delete company
□ Can approve drive
□ Can reject drive
□ Can view all applications
□ Search students works
□ Search companies works

COMPANY FUNCTIONS
□ Dashboard shows drives with applicant counts
□ Can create drive
□ Drive goes to pending after create
□ Can edit drive
□ Can close drive
□ Can delete drive
□ Can view student applications
□ Can shortlist student
□ Can select student
□ Can reject student

STUDENT FUNCTIONS
□ Dashboard shows only approved drives
□ Can view drive details
□ Can apply for drive
□ Cannot apply twice (duplicate blocked)
□ Can see application status
□ Can edit profile
□ Can upload resume
□ History page shows all applications
□ History summary counts correct

SECURITY
□ Student cannot access admin pages
□ Company cannot access admin pages
□ Cannot access pages without login
```

---

# PART B - SUBMISSION INSTRUCTIONS

---

## What Files To Include In ZIP

```
placement_portal/          ← THIS IS YOUR ROOT FOLDER
│
├── app.py                 ✅ MUST HAVE
├── models.py              ✅ MUST HAVE
├── init_db.py             ✅ MUST HAVE
│
├── static/
│   ├── css/
│   │   └── style.css      ✅ MUST HAVE
│   └── uploads/
│       └── resumes/       ✅ MUST HAVE (keep folder, empty is ok)
│
├── templates/
│   ├── base.html          ✅ MUST HAVE
│   ├── login.html         ✅ MUST HAVE
│   ├── register.html      ✅ MUST HAVE
│   │
│   ├── admin/
│   │   ├── dashboard.html     ✅ MUST HAVE
│   │   ├── companies.html     ✅ MUST HAVE
│   │   ├── students.html      ✅ MUST HAVE
│   │   ├── drives.html        ✅ MUST HAVE
│   │   ├── applications.html  ✅ MUST HAVE
│   │   └── search.html        ✅ MUST HAVE
│   │
│   ├── company/
│   │   ├── dashboard.html     ✅ MUST HAVE
│   │   ├── create_drive.html  ✅ MUST HAVE
│   │   ├── edit_drive.html    ✅ MUST HAVE
│   │   └── applications.html  ✅ MUST HAVE
│   │
│   └── student/
│       ├── dashboard.html     ✅ MUST HAVE
│       ├── profile.html       ✅ MUST HAVE
│       ├── drive_detail.html  ✅ MUST HAVE
│       └── history.html       ✅ MUST HAVE
│
└── Project Report.pdf     ✅ MUST HAVE
```

---

## What NOT To Include

```
❌ DO NOT include these:
- instance/placement.db    (database file)
- __pycache__/ folder
- .env files
- venv/ or env/ folder
- Any .pyc files
- node_modules (if any)
- .git folder
```

---

## How To Create ZIP File

### On Windows:
```
1. Go to your project folder location
2. Right click on "placement_portal" folder
3. Click "Send to" → "Compressed (zipped) folder"
4. Rename zip to: placement_portal_2XfX00XXXX.zip
   (replace 2XfX00XXXX with your actual roll number)
```

### On Mac:
```
1. Right click on "placement_portal" folder
2. Click "Compress placement_portal"
3. Rename to: placement_portal_2XfX00XXXX.zip
```

### On Linux:
```
cd .. (go one folder above placement_portal)
zip -r placement_portal_2XfX00XXXX.zip placement_portal/
```

---

## ZIP File Structure Must Look Like This

```
placement_portal_2XfX00XXXX.zip
└── placement_portal/           ← ONE root folder only
    ├── app.py
    ├── models.py
    ├── init_db.py
    ├── static/
    │   └── css/
    │       └── style.css
    ├── templates/
    │   ├── base.html
    │   └── ... all templates
    └── Project Report.pdf
```

---

## Common ZIP Mistakes That Cause U Grade

```
❌ MISTAKE 1 - Files directly in ZIP (no root folder)
placement_portal.zip
├── app.py          ← WRONG, no root folder
├── models.py
└── templates/

✅ CORRECT
placement_portal.zip
└── placement_portal/   ← root folder exists
    ├── app.py
    └── models.py

❌ MISTAKE 2 - Multiple folders in root
placement_portal.zip
├── placement_portal/
├── extra_folder/       ← WRONG, extra folder
└── report.pdf          ← WRONG, file outside root folder

✅ CORRECT
placement_portal.zip
└── placement_portal/   ← ONLY ONE folder
    ├── app.py
    └── Project Report.pdf   ← report INSIDE root folder

❌ MISTAKE 3 - No .py file
placement_portal.zip
└── placement_portal/
    └── Project Report.pdf   ← WRONG, no .py file

❌ MISTAKE 4 - Corrupted or wrong format
submission.rar    ← WRONG, must be .zip only
```

---

## Project Report Must Contain

```
Page 1 - Student Details
------------------------
□ Full Name
□ Roll Number
□ Email
□ Course Name

Page 2 - Project Details
------------------------
□ Project name
□ Problem statement summary
□ How you approached the problem
□ What features you implemented

Page 3 - Technical Details
------------------------
□ Frameworks used (Flask, SQLAlchemy, Bootstrap etc.)
□ Libraries used
□ AI/LLM declaration (if you used any)

Page 4 - ER Diagram
------------------------
□ All 5 tables shown
□ Relationships shown with arrows
□ Primary keys marked
□ Foreign keys marked

Tables to show:
- User (id, username, email, password, role, is_active)
- Company (id, user_id→User, company_name, hr_contact, approval_status)
- Student (id, user_id→User, full_name, email, phone, department, cgpa)
- PlacementDrive (id, company_id→Company, drive_name, job_title, status)
- Application (id, student_id→Student, drive_id→PlacementDrive, status)

Page 5 - Video Link
------------------------
□ Google Drive video link
□ Link must be accessible to anyone with the link
```

---

## Video Recording Guide

```
TOTAL TIME: 5-10 minutes max

SECTION 1 (30 seconds) - Introduction
--------------------------------------
Say:
- Your name and roll number
- Project name: Placement Portal Application

SECTION 2 (30 seconds) - Approach
--------------------------------------
Say:
- 3 roles: Admin, Company, Student
- Flask backend, SQLite database, Bootstrap UI
- How data flows between roles

SECTION 3 (90 seconds) - Feature Demo
--------------------------------------
Show in this order:
1. Register as student → login
2. Register as company → show pending message
3. Login as admin → approve company
4. Login as company → create drive
5. Login as admin → approve drive
6. Login as student → apply for drive
7. Login as company → update application status
8. Login as student → check updated status in history

SECTION 4 (30 seconds) - Extra Features
--------------------------------------
Show anything extra you added:
- Resume upload
- Search functionality
- Application history summary cards
- Blacklist feature
```

---

## Final Submission Checklist

```
BEFORE SUBMITTING - CHECK ALL OF THESE

CODE CHECKS
□ python init_db.py runs without error
□ python app.py runs without error
□ All pages load correctly
□ Admin login works (admin/admin123)
□ Student registration works
□ Company registration works
□ All core features working

ZIP FILE CHECKS
□ ZIP file named correctly with roll number
□ Only ONE root folder inside ZIP
□ Root folder contains app.py
□ Root folder contains models.py
□ Root folder contains all templates
□ No database file (placement.db) in ZIP
□ No __pycache__ folders in ZIP
□ No venv folder in ZIP

REPORT CHECKS
□ Report is PDF format
□ Not more than 5 pages
□ Contains student details
□ Contains ER diagram
□ Contains video link
□ AI declaration included

VIDEO CHECKS
□ Video is 5-10 minutes max
□ Uploaded to Google Drive
□ Sharing set to "Anyone with link"
□ Link added to report

VALIDATION CHECK
□ Submit to validation Google Form FIRST
□ Got success email from validation
□ Only THEN submit to actual portal

FINAL SUBMIT
□ Submit ZIP to portal (ONLY ONCE)
□ Submit PDF report to portal
□ Cannot change after submission
```

---

## Things To Remember For Viva

```
PREPARE THESE ANSWERS

1. What is Flask and why did you use it?
   → Python web framework, easy routing and templating

2. What is SQLAlchemy?
   → ORM for Python, converts Python classes to DB tables

3. How does session work in your app?
   → Stores user_id and role after login, checked on every route

4. How do you prevent duplicate applications?
   → Query Application table for same student_id + drive_id before inserting

5. How is admin created?
   → Pre-created in init_db.py, not through registration

6. What happens when company is blacklisted?
   → All drives set to closed, user.is_active = False

7. How does role-based access work?
   → Every route checks session role before allowing access

8. What tables are in your database?
   → User, Company, Student, PlacementDrive, Application

9. What is Jinja2?
   → Template engine for Flask, renders HTML with Python data

10. How does resume upload work?
    → file saved to static/uploads/resumes/ folder
```

---

> That is the complete testing document and submission guide.
> You are ready to test, submit and present your project!