import os
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from app import app
from models import Application, Company, PlacementDrive, Student, User, db


results = []


def add_result(case_id, description, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append((case_id, description, status, detail))


def text(resp):
    return resp.get_data(as_text=True)


def has_text(resp, needle):
    return needle in text(resp)


def is_redirect_to(resp, path_suffix):
    if resp.status_code not in (301, 302, 303, 307, 308):
        return False
    location = resp.headers.get("Location", "")
    return location.endswith(path_suffix)


def login(client, username, password, follow=False):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=follow,
    )


def logout(client, follow=False):
    return client.get("/logout", follow_redirects=follow)


def register_student(client, username, email, password, full_name, phone="", dept="", cgpa=""):
    return client.post(
        "/register",
        data={
            "role": "student",
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name,
            "phone": phone,
            "department": dept,
            "cgpa": cgpa,
        },
        follow_redirects=True,
    )


def register_company(
    client,
    username,
    email,
    password,
    company_name,
    hr_contact,
    website="",
    description="",
):
    return client.post(
        "/register",
        data={
            "role": "company",
            "username": username,
            "email": email,
            "password": password,
            "company_name": company_name,
            "hr_contact": hr_contact,
            "website": website,
            "description": description,
        },
        follow_redirects=True,
    )


def admin_client():
    c = app.test_client()
    login(c, "admin", "admin123")
    return c


def company_client(username, password="test123"):
    c = app.test_client()
    login(c, username, password)
    return c


def student_client(username, password="test123"):
    c = app.test_client()
    login(c, username, password)
    return c


def get_company_id(company_name):
    with app.app_context():
        company = Company.query.filter_by(company_name=company_name).first()
        return company.id if company else None


def get_user_id(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        return user.id if user else None


def get_student_id(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            return None
        student = Student.query.filter_by(user_id=user.id).first()
        return student.id if student else None


def get_drive_by_name(name):
    with app.app_context():
        return PlacementDrive.query.filter_by(drive_name=name).first()


def reset_db_and_run_init():
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

        db_path = Path(db.engine.url.database)
        candidates = [db_path]
        if not db_path.is_absolute():
            candidates.append(Path(app.instance_path) / db_path)
            candidates.append(Path.cwd() / db_path)

        for c in candidates:
            if c.exists():
                try:
                    c.unlink()
                except OSError:
                    pass

    proc = subprocess.run(
        [sys.executable, "init_db.py"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    output = (proc.stdout or "") + (proc.stderr or "")

    with app.app_context():
        admin = User.query.filter_by(username="admin", role="admin").first()
        db_file_path = Path(db.engine.url.database)
        if not db_file_path.is_absolute():
            db_file_path = Path(app.instance_path) / db_file_path
        db_file_exists = db_file_path.exists()

    add_result(
        "TEST 1.1",
        "init_db.py runs and prints DB creation message",
        "Database tables created successfully!" in output,
        output.strip()[-300:],
    )
    add_result(
        "TEST 1.2",
        "Admin user exists after init",
        admin is not None,
        "admin user check",
    )
    add_result(
        "TEST 1.3",
        "SQLite DB file exists",
        db_file_exists,
        str(db_file_path),
    )


def run_core_tests():
    # TEST 2 - Admin Login Test
    c = app.test_client()

    resp = login(c, "admin", "admin123", follow=False)
    add_result("TEST 2.1", "Correct admin login redirects to /admin/dashboard", is_redirect_to(resp, "/admin/dashboard"))

    resp = login(c, "admin", "wrongpass", follow=True)
    add_result("TEST 2.2", "Wrong password shows invalid credentials message", has_text(resp, "Invalid username or password"))

    resp = c.post("/login", data={"username": "", "password": ""}, follow_redirects=True)
    add_result("TEST 2.3", "Empty login fields show validation message", has_text(resp, "Please fill all fields"))

    resp = c.get("/register")
    add_result("TEST 2.4", "Admin cannot self-register from UI dropdown", "value=\"admin\"" not in text(resp))

    # TEST 3 - Student Registration & Login
    resp = register_student(
        c,
        "teststudent1",
        "student1@test.com",
        "test123",
        "Test Student One",
        "9876543210",
        "Computer Science",
        "8.5",
    )
    add_result("TEST 3.1", "Student registration succeeds", has_text(resp, "Student registered successfully!"))

    resp = register_student(
        c,
        "teststudent1",
        "student2@test.com",
        "test123",
        "Another Student",
    )
    add_result("TEST 3.2", "Duplicate username blocked", has_text(resp, "Username already taken"))

    resp = register_student(
        c,
        "teststudent2",
        "student1@test.com",
        "test123",
        "Another Student",
    )
    add_result("TEST 3.3", "Duplicate email blocked", has_text(resp, "Email already registered"))

    resp = login(c, "teststudent1", "test123", follow=False)
    add_result("TEST 3.4", "Student login redirects to /student/dashboard", is_redirect_to(resp, "/student/dashboard"))

    resp = c.get("/admin/dashboard", follow_redirects=True)
    add_result(
        "TEST 3.5",
        "Student cannot access admin dashboard",
        has_text(resp, "Access denied") and has_text(resp, "Login to your account"),
    )

    # TEST 4 - Company Registration & Approval
    resp = register_company(
        c,
        "testcompany1",
        "company1@test.com",
        "test123",
        "Tech Corp",
        "hr@techcorp.com",
        "https://techcorp.com",
        "A tech company",
    )
    add_result("TEST 4.1", "Company registration succeeds", has_text(resp, "Company registered! Wait for admin approval"))

    resp = login(c, "testcompany1", "test123", follow=True)
    add_result("TEST 4.2", "Company cannot login before approval", has_text(resp, "pending admin approval"))

    admin = admin_client()
    company1_id = get_company_id("Tech Corp")
    resp = admin.post(f"/admin/company/{company1_id}/approve", follow_redirects=True)
    add_result("TEST 4.3", "Admin approves company", has_text(resp, "has been approved!"))

    resp = login(c, "testcompany1", "test123", follow=False)
    add_result("TEST 4.4", "Company login works after approval", is_redirect_to(resp, "/company/dashboard"))

    resp = register_company(
        c,
        "badcompany",
        "bad@company.com",
        "test123",
        "Bad Corp",
        "hr@badcorp.com",
    )
    bad_company_id = get_company_id("Bad Corp")
    resp = admin.post(f"/admin/company/{bad_company_id}/reject", follow_redirects=True)
    add_result("TEST 4.5", "Admin rejects another company", has_text(resp, "has been rejected!"))

    # TEST 5 - Admin Dashboard
    resp = admin.get("/admin/dashboard")
    dashboard_ok = all(
        s in text(resp)
        for s in [
            "Total Students",
            "Total Companies",
            "Total Drives",
            "Total Applications",
            "Pending Company Approvals",
            "Pending Drive Approvals",
        ]
    )
    add_result("TEST 5.1", "Admin dashboard shows stat cards and pending sections", dashboard_ok)

    # TEST 8 - Placement Drive Creation
    comp = company_client("testcompany1")
    drive_payload_1 = {
        "drive_name": "Campus Drive 2025",
        "job_title": "Software Developer",
        "job_description": "Building web applications",
        "eligibility": "CGPA > 7.0",
        "deadline": "2025-12-31",
        "salary": "6 LPA",
        "location": "Bangalore",
    }
    resp = comp.post("/company/drive/create", data=drive_payload_1, follow_redirects=True)
    add_result("TEST 8.1", "Company creates new drive", has_text(resp, "Drive created! Waiting for admin approval."))

    d1 = get_drive_by_name("Campus Drive 2025")
    add_result("TEST 8.2", "Created drive status is pending", d1 is not None and d1.status == "pending")

    resp = admin.post(f"/admin/drive/{d1.id}/approve", follow_redirects=True)
    add_result("TEST 8.3", "Admin approves drive", has_text(resp, "approved!"))

    drive_payload_2 = {
        "drive_name": "Campus Drive Reject",
        "job_title": "QA Engineer",
        "job_description": "Testing applications",
        "eligibility": "CGPA > 6.5",
        "deadline": "2025-11-30",
        "salary": "5 LPA",
        "location": "Pune",
    }
    comp.post("/company/drive/create", data=drive_payload_2, follow_redirects=True)
    d2 = get_drive_by_name("Campus Drive Reject")
    resp = admin.post(f"/admin/drive/{d2.id}/reject", follow_redirects=True)
    add_result("TEST 8.4", "Admin rejects drive", has_text(resp, "rejected!"))

    resp = comp.post(
        "/company/drive/create",
        data={
            "drive_name": "",
            "job_title": "No Name Job",
            "job_description": "desc",
            "eligibility": "",
            "deadline": "2025-10-10",
            "salary": "",
            "location": "",
        },
        follow_redirects=True,
    )
    add_result("TEST 8.5", "Empty required fields blocked for drive create", has_text(resp, "Please fill all required fields"))

    # TEST 9 - Company Drive Management
    resp = comp.post(
        f"/company/drive/{d1.id}/edit",
        data={
            "drive_name": "Campus Drive 2025",
            "job_title": "Senior Developer",
            "job_description": "Building web applications",
            "eligibility": "CGPA > 7.0",
            "deadline": "2025-12-31",
            "salary": "8 LPA",
            "location": "Bangalore",
        },
        follow_redirects=True,
    )
    d1_ref = get_drive_by_name("Campus Drive 2025")
    add_result(
        "TEST 9.1",
        "Edit drive updates and resets to pending",
        has_text(resp, "Drive updated! Waiting for admin approval again.") and d1_ref.status == "pending" and d1_ref.job_title == "Senior Developer",
    )

    resp = comp.post(f"/company/drive/{d1.id}/close", follow_redirects=True)
    with app.app_context():
        closed_status = PlacementDrive.query.get(d1.id).status
    add_result("TEST 9.2", "Close drive sets status to closed", has_text(resp, "Drive closed successfully!") and closed_status == "closed")

    comp.post(
        "/company/drive/create",
        data={
            "drive_name": "Delete Me Drive",
            "job_title": "Delete Role",
            "job_description": "Delete test",
            "eligibility": "Any",
            "deadline": "2025-12-15",
            "salary": "4 LPA",
            "location": "Delhi",
        },
        follow_redirects=True,
    )
    del_drive = get_drive_by_name("Delete Me Drive")
    resp = comp.post(f"/company/drive/{del_drive.id}/delete", follow_redirects=True)
    with app.app_context():
        del_exists = PlacementDrive.query.get(del_drive.id) is not None
    add_result("TEST 9.3", "Delete drive removes it", has_text(resp, "Drive deleted successfully!") and not del_exists)

    # Create approved drive for student apply flows
    comp.post(
        "/company/drive/create",
        data={
            "drive_name": "Apply Drive 2025",
            "job_title": "Backend Developer",
            "job_description": "APIs and backend",
            "eligibility": "CGPA > 7.0",
            "deadline": "2025-12-25",
            "salary": "7 LPA",
            "location": "Hyderabad",
        },
        follow_redirects=True,
    )
    apply_drive = get_drive_by_name("Apply Drive 2025")
    admin.post(f"/admin/drive/{apply_drive.id}/approve", follow_redirects=True)

    # TEST 10 - Student Apply
    stu = student_client("teststudent1")
    resp = stu.get("/student/dashboard")
    dash_text = text(resp)
    add_result(
        "TEST 10.1",
        "Student dashboard shows only approved drives",
        ("Backend Developer" in dash_text) and ("QA Engineer" not in dash_text) and ("Senior Developer" not in dash_text),
    )

    resp = stu.get(f"/student/drive/{apply_drive.id}")
    detail_ok = all(
        s in text(resp)
        for s in [
            "Backend Developer",
            "APIs and backend",
            "7 LPA",
            "Hyderabad",
            "Apply Now",
        ]
    ) and (("CGPA > 7.0" in text(resp)) or ("CGPA &gt; 7.0" in text(resp)))
    add_result("TEST 10.2", "Student sees drive details with apply action", detail_ok)

    resp = stu.post(f"/student/drive/{apply_drive.id}/apply", follow_redirects=True)
    add_result("TEST 10.3", "Student can apply for approved drive", has_text(resp, "Application submitted successfully!"))

    resp = stu.get(f"/student/drive/{apply_drive.id}")
    t = text(resp)
    add_result(
        "TEST 10.4",
        "Duplicate application prevented (already applied shown)",
        ("already applied" in t.lower()) and ("Apply Now" not in t),
    )

    resp = stu.get("/student/dashboard")
    add_result("TEST 10.5", "Student dashboard shows applied status", "APPLIED" in text(resp))

    # TEST 11 - Company reviews applications
    with app.app_context():
        app_row = Application.query.filter_by(drive_id=apply_drive.id).first()
    resp = comp.get(f"/company/drive/{apply_drive.id}/applications")
    add_result("TEST 11.1", "Company can view drive applications", has_text(resp, "Received Applications"))

    resp = comp.post(f"/company/application/{app_row.id}/update", data={"status": "shortlisted"}, follow_redirects=True)
    with app.app_context():
        s1 = Application.query.get(app_row.id).status
    add_result("TEST 11.2", "Company can shortlist student", s1 == "shortlisted")

    comp.post(f"/company/application/{app_row.id}/update", data={"status": "selected"}, follow_redirects=True)
    with app.app_context():
        s2 = Application.query.get(app_row.id).status
    add_result("TEST 11.3", "Company can select student", s2 == "selected")

    comp.post(f"/company/application/{app_row.id}/update", data={"status": "rejected"}, follow_redirects=True)
    with app.app_context():
        s3 = Application.query.get(app_row.id).status
    add_result("TEST 11.4", "Company can reject student", s3 == "rejected")

    resp = stu.get("/student/history")
    add_result("TEST 11.5", "Student sees updated application status", "REJECTED" in text(resp))

    # TEST 12 - Student profile and resume
    resp = stu.post(
        "/student/profile",
        data={
            "full_name": "Test Student One Updated",
            "phone": "9999999999",
            "department": "Information Technology",
            "cgpa": "9.1",
        },
        follow_redirects=True,
    )
    with app.app_context():
        sid = get_student_id("teststudent1")
        stu_row = Student.query.get(sid)
    add_result(
        "TEST 12.1",
        "Student can edit profile",
        has_text(resp, "Profile updated successfully!") and stu_row.full_name == "Test Student One Updated" and stu_row.cgpa == 9.1,
    )

    resp = stu.post(
        "/student/profile",
        data={
            "full_name": "Test Student One Updated",
            "phone": "9999999999",
            "department": "Information Technology",
            "cgpa": "9.1",
            "resume": (BytesIO(b"%PDF-1.4 test pdf"), "resume.pdf"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    with app.app_context():
        sid = get_student_id("teststudent1")
        stu_row = Student.query.get(sid)
        resume_name = stu_row.resume_filename
        resume_path = Path(app.config["UPLOAD_FOLDER"]) / resume_name if resume_name else None
    add_result(
        "TEST 12.2",
        "Student can upload resume",
        has_text(resp, "Profile updated successfully!") and resume_name is not None and resume_path.exists(),
    )

    if resume_name:
        resp = stu.get(f"/static/uploads/resumes/{resume_name}")
        add_result("TEST 12.3", "Uploaded resume link is accessible", resp.status_code == 200)
    else:
        add_result("TEST 12.3", "Uploaded resume link is accessible", False, "resume filename missing")

    # TEST 13 - Student history
    comp.post(
        "/company/drive/create",
        data={
            "drive_name": "History Drive 2",
            "job_title": "Data Analyst",
            "job_description": "Analyze data",
            "eligibility": "CGPA > 6.0",
            "deadline": "2025-12-26",
            "salary": "5.5 LPA",
            "location": "Chennai",
        },
        follow_redirects=True,
    )
    h2 = get_drive_by_name("History Drive 2")
    admin.post(f"/admin/drive/{h2.id}/approve", follow_redirects=True)
    stu.post(f"/student/drive/{h2.id}/apply", follow_redirects=True)

    resp = stu.get("/student/history")
    hist_text = text(resp)
    add_result(
        "TEST 13.1",
        "Student history page shows summary and table",
        all(s in hist_text for s in ["Total Applied", "Shortlisted", "Selected", "Rejected", "Complete Application History"]),
    )
    add_result(
        "TEST 13.2",
        "History shows all applications",
        ("Apply Drive 2025" in hist_text) and ("History Drive 2" in hist_text),
    )

    # TEST 14 - Admin search
    resp = admin.get("/admin/search?q=Test+Student&type=student")
    add_result("TEST 14.1", "Admin search students works", "Test Student One Updated" in text(resp))

    resp = admin.get("/admin/search?q=Tech&type=company")
    add_result("TEST 14.2", "Admin search companies works", "Tech Corp" in text(resp))

    resp = admin.get("/admin/search?q=&type=student")
    add_result("TEST 14.3", "Admin empty search handled", resp.status_code == 200)

    # TEST 6 - Admin company management (run here to avoid affecting core company before drive tests)
    resp = admin.get("/admin/companies?search=Tech")
    add_result("TEST 6.1", "Admin can search company by name", "Tech Corp" in text(resp))

    register_company(
        c,
        "blackcompany1",
        "blackcompany1@test.com",
        "test123",
        "Tech Blacklist Corp",
        "hr@techblack.com",
    )
    bl_id = get_company_id("Tech Blacklist Corp")
    admin.post(f"/admin/company/{bl_id}/approve", follow_redirects=True)
    bl_client = company_client("blackcompany1")
    bl_client.post(
        "/company/drive/create",
        data={
            "drive_name": "BL Drive",
            "job_title": "BL Role",
            "job_description": "BL Desc",
            "eligibility": "Any",
            "deadline": "2025-12-27",
            "salary": "4 LPA",
            "location": "Noida",
        },
        follow_redirects=True,
    )
    bl_drive = get_drive_by_name("BL Drive")
    admin.post(f"/admin/drive/{bl_drive.id}/approve", follow_redirects=True)

    resp = admin.post(f"/admin/company/{bl_id}/blacklist", follow_redirects=True)
    with app.app_context():
        bl_company = Company.query.get(bl_id)
        bl_user = User.query.get(bl_company.user_id)
        bl_drives = PlacementDrive.query.filter_by(company_id=bl_id).all()
        drives_closed = all(d.status == "closed" for d in bl_drives)
    add_result(
        "TEST 6.2",
        "Blacklisting company updates status and deactivates user",
        has_text(resp, "blacklisted") and bl_company.approval_status == "blacklisted" and (not bl_user.is_active),
    )

    resp = login(c, "blackcompany1", "test123", follow=True)
    add_result("TEST 6.3", "Blacklisted company cannot login", "deactivated" in text(resp).lower())
    add_result("TEST 6.4", "All blacklisted company drives are closed", drives_closed)

    register_company(
        c,
        "deletecompany1",
        "deletecompany1@test.com",
        "test123",
        "Delete Corp",
        "hr@deletecorp.com",
    )
    del_comp_id = get_company_id("Delete Corp")
    admin.post(f"/admin/company/{del_comp_id}/approve", follow_redirects=True)
    admin.post(f"/admin/company/{del_comp_id}/delete", follow_redirects=True)
    with app.app_context():
        exists = Company.query.get(del_comp_id) is not None
    add_result("TEST 6.5", "Admin can delete company", not exists)

    # TEST 7 - Admin student management
    resp = admin.get("/admin/students")
    add_result("TEST 7.1", "Admin can view all students", "All Students" in text(resp))

    resp = admin.get("/admin/students?search=Test+Student")
    add_result("TEST 7.2", "Admin can search student by name", "Test Student One Updated" in text(resp))

    resp = admin.get("/admin/students?search=student1@test.com")
    add_result("TEST 7.3", "Admin can search student by email", "student1@test.com" in text(resp))

    register_student(c, "blackstudent1", "blackstudent1@test.com", "test123", "Black Student")
    bs_id = get_student_id("blackstudent1")
    admin.post(f"/admin/student/{bs_id}/blacklist", follow_redirects=True)
    resp = login(c, "blackstudent1", "test123", follow=True)
    add_result("TEST 7.4", "Blacklisted student cannot login", "deactivated" in text(resp).lower())

    register_student(c, "deletestudent1", "deletestudent1@test.com", "test123", "Delete Student")
    ds_id = get_student_id("deletestudent1")
    admin.post(f"/admin/student/{ds_id}/delete", follow_redirects=True)
    with app.app_context():
        ds_exists = Student.query.get(ds_id) is not None
    add_result("TEST 7.5", "Admin can delete student", not ds_exists)

    # TEST 15 - URL access control
    sclient = student_client("teststudent1")
    resp = sclient.get("/admin/dashboard", follow_redirects=True)
    add_result("TEST 15.1", "Student cannot access admin URL", "Access denied" in text(resp) and "Login to your account" in text(resp))

    cclient = company_client("testcompany1")
    resp = cclient.get("/admin/students", follow_redirects=True)
    add_result("TEST 15.2", "Company cannot access admin URL", "Login to your account" in text(resp))

    resp = sclient.get("/company/dashboard", follow_redirects=True)
    add_result("TEST 15.3", "Student cannot access company URL", "Access denied" in text(resp) and "Login to your account" in text(resp))

    anon = app.test_client()
    resp = anon.get("/admin/dashboard", follow_redirects=False)
    add_result("TEST 15.4", "Anonymous user redirected from protected route", is_redirect_to(resp, "/login"))

    register_company(
        c,
        "testcompany2",
        "company2@test.com",
        "test123",
        "Second Tech Corp",
        "hr@secondtech.com",
    )
    c2_id = get_company_id("Second Tech Corp")
    admin.post(f"/admin/company/{c2_id}/approve", follow_redirects=True)
    c2 = company_client("testcompany2")
    protected_drive = get_drive_by_name("Apply Drive 2025")
    resp = c2.get(f"/company/drive/{protected_drive.id}/edit", follow_redirects=True)
    add_result("TEST 15.5", "Company cannot edit another company drive", "Access denied" in text(resp))

    # TEST 16 - Route URL existence tests
    route_client = app.test_client()
    resp = route_client.get("/", follow_redirects=False)
    add_result("TEST 16.P1", "GET / redirects to login", is_redirect_to(resp, "/login"))

    resp = route_client.get("/login")
    add_result("TEST 16.P2", "GET /login loads", resp.status_code == 200)

    resp = login(route_client, "admin", "admin123", follow=False)
    add_result("TEST 16.P3", "POST /login works", is_redirect_to(resp, "/admin/dashboard"))

    resp = route_client.get("/register")
    add_result("TEST 16.P4", "GET /register loads", resp.status_code == 200)

    resp = register_student(route_client, "route_student", "route_student@test.com", "test123", "Route Student")
    add_result("TEST 16.P5", "POST /register works", "registered successfully" in text(resp).lower())

    resp = route_client.get("/logout", follow_redirects=False)
    add_result("TEST 16.P6", "GET /logout works", is_redirect_to(resp, "/login"))

    admin_r = admin_client()
    add_result("TEST 16.A1", "GET /admin/dashboard", admin_r.get("/admin/dashboard").status_code == 200)
    add_result("TEST 16.A2", "GET /admin/companies", admin_r.get("/admin/companies").status_code == 200)

    register_company(route_client, "route_company", "route_company@test.com", "test123", "Route Co", "hr@routeco.com")
    rc_id = get_company_id("Route Co")
    add_result("TEST 16.A3", "POST /admin/company/<id>/approve", admin_r.post(f"/admin/company/{rc_id}/approve", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.A4", "POST /admin/company/<id>/reject", admin_r.post(f"/admin/company/{rc_id}/reject", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.A5", "POST /admin/company/<id>/blacklist", admin_r.post(f"/admin/company/{rc_id}/blacklist", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.A6", "POST /admin/company/<id>/delete", admin_r.post(f"/admin/company/{rc_id}/delete", follow_redirects=False).status_code in (301, 302))

    add_result("TEST 16.A7", "GET /admin/students", admin_r.get("/admin/students").status_code == 200)

    register_student(route_client, "route_stu2", "route_stu2@test.com", "test123", "Route Stu2")
    rs2_id = get_student_id("route_stu2")
    add_result("TEST 16.A8", "POST /admin/student/<id>/blacklist", admin_r.post(f"/admin/student/{rs2_id}/blacklist", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.A9", "POST /admin/student/<id>/delete", admin_r.post(f"/admin/student/{rs2_id}/delete", follow_redirects=False).status_code in (301, 302))

    add_result("TEST 16.A10", "GET /admin/drives", admin_r.get("/admin/drives").status_code == 200)

    c1_id = get_company_id("Tech Corp")
    c1_user_id = get_user_id("testcompany1")
    with app.app_context():
        c1 = Company.query.filter_by(user_id=c1_user_id).first()
        d = PlacementDrive(
            company_id=c1.id,
            drive_name="Route Drive",
            job_title="Route Job",
            job_description="Route Desc",
            eligibility="Any",
            deadline="2025-12-30",
            salary="3 LPA",
            location="Route City",
            status="pending",
        )
        db.session.add(d)
        db.session.commit()
        route_drive_id = d.id

    add_result("TEST 16.A11", "POST /admin/drive/<id>/approve", admin_r.post(f"/admin/drive/{route_drive_id}/approve", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.A12", "POST /admin/drive/<id>/reject", admin_r.post(f"/admin/drive/{route_drive_id}/reject", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.A13", "GET /admin/applications", admin_r.get("/admin/applications").status_code == 200)
    add_result("TEST 16.A14", "GET /admin/search", admin_r.get("/admin/search").status_code == 200)

    comp_r = company_client("testcompany1")
    add_result("TEST 16.C1", "GET /company/dashboard", comp_r.get("/company/dashboard").status_code == 200)
    add_result("TEST 16.C2", "GET /company/drive/create", comp_r.get("/company/drive/create").status_code == 200)

    resp = comp_r.post(
        "/company/drive/create",
        data={
            "drive_name": "Route Co Drive",
            "job_title": "Co Route Job",
            "job_description": "Co Route Desc",
            "eligibility": "Any",
            "deadline": "2025-12-29",
            "salary": "4 LPA",
            "location": "Route Town",
        },
        follow_redirects=False,
    )
    add_result("TEST 16.C3", "POST /company/drive/create", resp.status_code in (301, 302))

    route_co_drive = get_drive_by_name("Route Co Drive")
    add_result("TEST 16.C4", "GET /company/drive/<id>/edit", comp_r.get(f"/company/drive/{route_co_drive.id}/edit").status_code == 200)

    resp = comp_r.post(
        f"/company/drive/{route_co_drive.id}/edit",
        data={
            "drive_name": "Route Co Drive",
            "job_title": "Co Route Job Edited",
            "job_description": "Co Route Desc",
            "eligibility": "Any",
            "deadline": "2025-12-29",
            "salary": "4 LPA",
            "location": "Route Town",
        },
        follow_redirects=False,
    )
    add_result("TEST 16.C5", "POST /company/drive/<id>/edit", resp.status_code in (301, 302))

    add_result("TEST 16.C6", "POST /company/drive/<id>/close", comp_r.post(f"/company/drive/{route_co_drive.id}/close", follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.C7", "GET /company/drive/<id>/applications", comp_r.get(f"/company/drive/{route_co_drive.id}/applications").status_code == 200)

    with app.app_context():
        sid = get_student_id("teststudent1")
        app_row2 = Application(student_id=sid, drive_id=route_co_drive.id, status="applied")
        db.session.add(app_row2)
        db.session.commit()
        app_row2_id = app_row2.id

    add_result("TEST 16.C8", "POST /company/application/<id>/update", comp_r.post(f"/company/application/{app_row2_id}/update", data={"status": "shortlisted"}, follow_redirects=False).status_code in (301, 302))
    add_result("TEST 16.C9", "POST /company/drive/<id>/delete", comp_r.post(f"/company/drive/{route_co_drive.id}/delete", follow_redirects=False).status_code in (301, 302))

    stu_r = student_client("teststudent1")
    add_result("TEST 16.S1", "GET /student/dashboard", stu_r.get("/student/dashboard").status_code == 200)
    add_result("TEST 16.S2", "GET /student/profile", stu_r.get("/student/profile").status_code == 200)

    resp = stu_r.post(
        "/student/profile",
        data={"full_name": "Test Student One Updated", "phone": "8888888888", "department": "IT", "cgpa": "9.0"},
        follow_redirects=False,
    )
    add_result("TEST 16.S3", "POST /student/profile", resp.status_code in (301, 302))

    # create one approved drive for route-level student apply tests
    with app.app_context():
        c1 = Company.query.filter_by(user_id=get_user_id("testcompany1")).first()
        route_sd = PlacementDrive(
            company_id=c1.id,
            drive_name="Route Student Drive",
            job_title="Student Route Role",
            job_description="Student Route Desc",
            eligibility="Any",
            deadline="2025-12-28",
            salary="4.5 LPA",
            location="Mysore",
            status="approved",
        )
        db.session.add(route_sd)
        db.session.commit()
        route_sd_id = route_sd.id

    add_result("TEST 16.S4", "GET /student/drive/<id>", stu_r.get(f"/student/drive/{route_sd_id}").status_code == 200)
    resp = stu_r.post(f"/student/drive/{route_sd_id}/apply", follow_redirects=False)
    add_result("TEST 16.S5", "POST /student/drive/<id>/apply", resp.status_code in (301, 302))
    add_result("TEST 16.S6", "GET /student/history", stu_r.get("/student/history").status_code == 200)


def print_report():
    print("\n=== PART A TEST REPORT ===")
    for case_id, description, status, detail in results:
        print(f"{case_id} | {status} | {description}")
        if detail and status == "FAIL":
            print(f"  detail: {detail}")

    total = len(results)
    passed = sum(1 for _, _, status, _ in results if status == "PASS")
    failed = total - passed
    print("\n=== SUMMARY ===")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    reset_db_and_run_init()
    run_core_tests()
    print_report()
