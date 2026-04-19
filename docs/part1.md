# PART 1 - Complete Code

## File 1: `models.py`

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, company, student
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('Company', backref='user', uselist=False)
    student = db.relationship('Student', backref='user', uselist=False)


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    hr_contact = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='pending')  
    # pending, approved, rejected, blacklisted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    drives = db.relationship('PlacementDrive', backref='company', lazy=True)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    resume_filename = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='student', lazy=True)


class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    drive_name = db.Column(db.String(200), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.String(300))
    deadline = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.String(100))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  
    # pending, approved, closed, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='drive', lazy=True)


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied')  
    # applied, shortlisted, selected, rejected

```

---

## File 2: `init_db.py`

```python
from app import app
from models import db, User

with app.app_context():
    db.create_all()

    # Check if admin already exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            username='admin',
            email='admin@placement.com',
            password='admin123',  
            role='admin',
            is_active=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin created successfully!")
        print("Username: admin")
        print("Password: admin123")
    else:
        print("Admin already exists!")

    print("Database tables created successfully!")
```

---

## File 3: `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Company, Student, PlacementDrive, Application
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'placement_portal_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/resumes'

db.init_app(app)

# Make upload folder if not exists
with app.app_context():
    os.makedirs('static/uploads/resumes', exist_ok=True)


# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def login_required(role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash('Access denied', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


# ─────────────────────────────────────────
# PUBLIC ROUTES
# ─────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please fill all fields', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(username=username, password=password).first()

        if not user:
            flash('Invalid username or password', 'danger')
            return render_template('login.html')

        if not user.is_active:
            flash('Your account has been deactivated. Contact admin.', 'danger')
            return render_template('login.html')

        # Company must be approved
        if user.role == 'company':
            company = Company.query.filter_by(user_id=user.id).first()
            if company and company.approval_status != 'approved':
                flash('Your company registration is pending admin approval.', 'warning')
                return render_template('login.html')

        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role

        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'company':
            return redirect(url_for('company_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not all([role, username, email, password]):
            flash('Please fill all fields', 'danger')
            return render_template('register.html')

        # Check username exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken', 'danger')
            return render_template('register.html')

        # Check email exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered', 'danger')
            return render_template('register.html')

        # Create user
        new_user = User(
            username=username,
            email=email,
            password=password,
            role=role,
            is_active=True
        )
        db.session.add(new_user)
        db.session.flush()  # get new_user.id

        if role == 'company':
            company_name = request.form.get('company_name', '').strip()
            hr_contact = request.form.get('hr_contact', '').strip()
            website = request.form.get('website', '').strip()
            description = request.form.get('description', '').strip()

            if not company_name or not hr_contact:
                flash('Company name and HR contact are required', 'danger')
                db.session.rollback()
                return render_template('register.html')

            new_company = Company(
                user_id=new_user.id,
                company_name=company_name,
                hr_contact=hr_contact,
                website=website,
                description=description,
                approval_status='pending'
            )
            db.session.add(new_company)

        elif role == 'student':
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip()
            department = request.form.get('department', '').strip()
            cgpa = request.form.get('cgpa', '').strip()

            if not full_name:
                flash('Full name is required', 'danger')
                db.session.rollback()
                return render_template('register.html')

            new_student = Student(
                user_id=new_user.id,
                full_name=full_name,
                email=email,
                phone=phone,
                department=department,
                cgpa=float(cgpa) if cgpa else None
            )
            db.session.add(new_student)

        db.session.commit()

        if role == 'company':
            flash('Company registered! Wait for admin approval before login.', 'success')
        else:
            flash('Student registered successfully! You can login now.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


# ─────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    pending_companies = Company.query.filter_by(approval_status='pending').all()
    pending_drives = PlacementDrive.query.filter_by(status='pending').all()

    return render_template('admin/dashboard.html',
                           total_students=total_students,
                           total_companies=total_companies,
                           total_drives=total_drives,
                           total_applications=total_applications,
                           pending_companies=pending_companies,
                           pending_drives=pending_drives)


@app.route('/admin/companies')
def admin_companies():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    search = request.args.get('search', '').strip()
    if search:
        companies = Company.query.filter(
            Company.company_name.ilike(f'%{search}%')
        ).all()
    else:
        companies = Company.query.all()

    return render_template('admin/companies.html', companies=companies, search=search)


@app.route('/admin/company/<int:company_id>/approve', methods=['POST'])
def admin_approve_company(company_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    company = Company.query.get_or_404(company_id)
    company.approval_status = 'approved'
    db.session.commit()
    flash(f'{company.company_name} has been approved!', 'success')
    return redirect(url_for('admin_companies'))


@app.route('/admin/company/<int:company_id>/reject', methods=['POST'])
def admin_reject_company(company_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    company = Company.query.get_or_404(company_id)
    company.approval_status = 'rejected'
    db.session.commit()
    flash(f'{company.company_name} has been rejected!', 'warning')
    return redirect(url_for('admin_companies'))


@app.route('/admin/company/<int:company_id>/blacklist', methods=['POST'])
def admin_blacklist_company(company_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    company = Company.query.get_or_404(company_id)
    company.approval_status = 'blacklisted'

    # Close all drives of this company
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    for drive in drives:
        drive.status = 'closed'

    # Deactivate company user account
    user = User.query.get(company.user_id)
    if user:
        user.is_active = False

    db.session.commit()
    flash(f'{company.company_name} has been blacklisted and all drives closed!', 'danger')
    return redirect(url_for('admin_companies'))


@app.route('/admin/company/<int:company_id>/delete', methods=['POST'])
def admin_delete_company(company_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    company = Company.query.get_or_404(company_id)

    # Delete all applications for company drives
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    for drive in drives:
        Application.query.filter_by(drive_id=drive.id).delete()
        db.session.delete(drive)

    user = User.query.get(company.user_id)
    db.session.delete(company)
    if user:
        db.session.delete(user)

    db.session.commit()
    flash('Company deleted successfully!', 'success')
    return redirect(url_for('admin_companies'))


@app.route('/admin/students')
def admin_students():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    search = request.args.get('search', '').strip()
    if search:
        students = Student.query.filter(
            (Student.full_name.ilike(f'%{search}%')) |
            (Student.email.ilike(f'%{search}%')) |
            (Student.phone.ilike(f'%{search}%'))
        ).all()
    else:
        students = Student.query.all()

    return render_template('admin/students.html', students=students, search=search)


@app.route('/admin/student/<int:student_id>/blacklist', methods=['POST'])
def admin_blacklist_student(student_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    if user:
        user.is_active = False
    db.session.commit()
    flash(f'{student.full_name} has been blacklisted!', 'danger')
    return redirect(url_for('admin_students'))


@app.route('/admin/student/<int:student_id>/delete', methods=['POST'])
def admin_delete_student(student_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    student = Student.query.get_or_404(student_id)
    Application.query.filter_by(student_id=student.id).delete()
    user = User.query.get(student.user_id)
    db.session.delete(student)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('admin_students'))


@app.route('/admin/drives')
def admin_drives():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    drives = PlacementDrive.query.all()
    return render_template('admin/drives.html', drives=drives)


@app.route('/admin/drive/<int:drive_id>/approve', methods=['POST'])
def admin_approve_drive(drive_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'approved'
    db.session.commit()
    flash(f'Drive "{drive.drive_name}" approved!', 'success')
    return redirect(url_for('admin_drives'))


@app.route('/admin/drive/<int:drive_id>/reject', methods=['POST'])
def admin_reject_drive(drive_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'rejected'
    db.session.commit()
    flash(f'Drive "{drive.drive_name}" rejected!', 'warning')
    return redirect(url_for('admin_drives'))


@app.route('/admin/applications')
def admin_applications():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    applications = Application.query.all()
    return render_template('admin/applications.html', applications=applications)


@app.route('/admin/search')
def admin_search():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'student')

    students = []
    companies = []

    if query:
        if search_type == 'student':
            students = Student.query.filter(
                (Student.full_name.ilike(f'%{query}%')) |
                (Student.email.ilike(f'%{query}%'))
            ).all()
        else:
            companies = Company.query.filter(
                Company.company_name.ilike(f'%{query}%')
            ).all()

    return render_template('admin/search.html',
                           students=students,
                           companies=companies,
                           query=query,
                           search_type=search_type)


# ─────────────────────────────────────────
# COMPANY ROUTES
# ─────────────────────────────────────────

@app.route('/company/dashboard')
def company_dashboard():
    if 'user_id' not in session or session.get('role') != 'company':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    company = Company.query.filter_by(user_id=session['user_id']).first()
    if not company:
        flash('Company profile not found', 'danger')
        return redirect(url_for('login'))

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    # Count applicants per drive
    drive_data = []
    for drive in drives:
        count = Application.query.filter_by(drive_id=drive.id).count()
        drive_data.append({'drive': drive, 'applicant_count': count})

    return render_template('company/dashboard.html',
                           company=company,
                           drive_data=drive_data)


@app.route('/company/drive/create', methods=['GET', 'POST'])
def company_create_drive():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('login'))

    company = Company.query.filter_by(user_id=session['user_id']).first()

    if company.approval_status != 'approved':
        flash('Only approved companies can create drives', 'danger')
        return redirect(url_for('company_dashboard'))

    if request.method == 'POST':
        drive_name = request.form.get('drive_name', '').strip()
        job_title = request.form.get('job_title', '').strip()
        job_description = request.form.get('job_description', '').strip()
        eligibility = request.form.get('eligibility', '').strip()
        deadline = request.form.get('deadline', '').strip()
        salary = request.form.get('salary', '').strip()
        location = request.form.get('location', '').strip()

        if not all([drive_name, job_title, job_description, deadline]):
            flash('Please fill all required fields', 'danger')
            return render_template('company/create_drive.html', company=company)

        new_drive = PlacementDrive(
            company_id=company.id,
            drive_name=drive_name,
            job_title=job_title,
            job_description=job_description,
            eligibility=eligibility,
            deadline=deadline,
            salary=salary,
            location=location,
            status='pending'
        )
        db.session.add(new_drive)
        db.session.commit()
        flash('Drive created! Waiting for admin approval.', 'success')
        return redirect(url_for('company_dashboard'))

    return render_template('company/create_drive.html', company=company)


@app.route('/company/drive/<int:drive_id>/edit', methods=['GET', 'POST'])
def company_edit_drive(drive_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('login'))

    company = Company.query.filter_by(user_id=session['user_id']).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash('Access denied', 'danger')
        return redirect(url_for('company_dashboard'))

    if request.method == 'POST':
        drive.drive_name = request.form.get('drive_name', '').strip()
        drive.job_title = request.form.get('job_title', '').strip()
        drive.job_description = request.form.get('job_description', '').strip()
        drive.eligibility = request.form.get('eligibility', '').strip()
        drive.deadline = request.form.get('deadline', '').strip()
        drive.salary = request.form.get('salary', '').strip()
        drive.location = request.form.get('location', '').strip()
        drive.status = 'pending'  # reset to pending after edit
        db.session.commit()
        flash('Drive updated! Waiting for admin approval again.', 'success')
        return redirect(url_for('company_dashboard'))

    return render_template('company/edit_drive.html', drive=drive, company=company)


@app.route('/company/drive/<int:drive_id>/delete', methods=['POST'])
def company_delete_drive(drive_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('login'))

    company = Company.query.filter_by(user_id=session['user_id']).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash('Access denied', 'danger')
        return redirect(url_for('company_dashboard'))

    Application.query.filter_by(drive_id=drive.id).delete()
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted successfully!', 'success')
    return redirect(url_for('company_dashboard'))


@app.route('/company/drive/<int:drive_id>/close', methods=['POST'])
def company_close_drive(drive_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('login'))

    company = Company.query.filter_by(user_id=session['user_id']).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash('Access denied', 'danger')
        return redirect(url_for('company_dashboard'))

    drive.status = 'closed'
    db.session.commit()
    flash('Drive closed successfully!', 'success')
    return redirect(url_for('company_dashboard'))


@app.route('/company/drive/<int:drive_id>/applications')
def company_drive_applications(drive_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('login'))

    company = Company.query.filter_by(user_id=session['user_id']).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash('Access denied', 'danger')
        return redirect(url_for('company_dashboard'))

    applications = Application.query.filter_by(drive_id=drive.id).all()
    return render_template('company/applications.html',
                           applications=applications,
                           drive=drive,
                           company=company)


@app.route('/company/application/<int:app_id>/update', methods=['POST'])
def company_update_application(app_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('login'))

    application = Application.query.get_or_404(app_id)
    new_status = request.form.get('status', '').strip()

    if new_status in ['applied', 'shortlisted', 'selected', 'rejected']:
        application.status = new_status
        db.session.commit()
        flash('Application status updated!', 'success')

    return redirect(url_for('company_drive_applications',
                            drive_id=application.drive_id))


# ─────────────────────────────────────────
# STUDENT ROUTES
# ─────────────────────────────────────────

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    student = Student.query.filter_by(user_id=session['user_id']).first()

    # All approved drives
    approved_drives = PlacementDrive.query.filter_by(status='approved').all()

    # Student's applications
    my_applications = Application.query.filter_by(student_id=student.id).all()
    applied_drive_ids = [app.drive_id for app in my_applications]

    return render_template('student/dashboard.html',
                           student=student,
                           approved_drives=approved_drives,
                           my_applications=my_applications,
                           applied_drive_ids=applied_drive_ids)


@app.route('/student/profile', methods=['GET', 'POST'])
def student_profile():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    student = Student.query.filter_by(user_id=session['user_id']).first()

    if request.method == 'POST':
        student.full_name = request.form.get('full_name', '').strip()
        student.phone = request.form.get('phone', '').strip()
        student.department = request.form.get('department', '').strip()
        cgpa = request.form.get('cgpa', '').strip()
        student.cgpa = float(cgpa) if cgpa else None

        # Handle resume upload
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file.filename != '':
                # Simple filename - student id + original name
                filename = f"student_{student.id}_{resume_file.filename}"
                resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                student.resume_filename = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student_profile'))

    return render_template('student/profile.html', student=student)


@app.route('/student/drive/<int:drive_id>')
def student_drive_detail(drive_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    student = Student.query.filter_by(user_id=session['user_id']).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != 'approved':
        flash('This drive is not available', 'warning')
        return redirect(url_for('student_dashboard'))

    # Check if already applied
    already_applied = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    return render_template('student/drive_detail.html',
                           drive=drive,
                           student=student,
                           already_applied=already_applied)


@app.route('/student/drive/<int:drive_id>/apply', methods=['POST'])
def student_apply(drive_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    student = Student.query.filter_by(user_id=session['user_id']).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != 'approved':
        flash('This drive is not available for applications', 'danger')
        return redirect(url_for('student_dashboard'))

    # Check duplicate application
    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing:
        flash('You have already applied for this drive!', 'warning')
        return redirect(url_for('student_drive_detail', drive_id=drive_id))

    new_application = Application(
        student_id=student.id,
        drive_id=drive.id,
        status='applied'
    )
    db.session.add(new_application)
    db.session.commit()
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('student_dashboard'))


@app.route('/student/history')
def student_history():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    student = Student.query.filter_by(user_id=session['user_id']).first()
    applications = Application.query.filter_by(student_id=student.id).all()

    return render_template('student/history.html',
                           student=student,
                           applications=applications)


# ─────────────────────────────────────────
# RUN APP
# ─────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

## File 4: `static/css/style.css`

```css
body {
    background-color: #f8f9fa;
    font-family: Arial, sans-serif;
}

.navbar {
    margin-bottom: 20px;
}

.card {
    margin-bottom: 20px;
    border-radius: 8px;
}

.card-header {
    font-weight: bold;
}

.stat-card {
    text-align: center;
    padding: 20px;
    border-radius: 8px;
    color: white;
}

.stat-card h2 {
    font-size: 2.5rem;
    font-weight: bold;
}

.stat-card p {
    font-size: 1rem;
    margin: 0;
}

.bg-students { background-color: #0d6efd; }
.bg-companies { background-color: #198754; }
.bg-drives { background-color: #ffc107; color: #333 !important; }
.bg-applications { background-color: #dc3545; }

.badge-pending { background-color: #ffc107; color: #333; }
.badge-approved { background-color: #198754; }
.badge-rejected { background-color: #dc3545; }
.badge-blacklisted { background-color: #6c757d; }
.badge-closed { background-color: #6c757d; }
.badge-applied { background-color: #0d6efd; }
.badge-shortlisted { background-color: #ffc107; color: #333; }
.badge-selected { background-color: #198754; }

.table th {
    background-color: #f1f3f4;
}

.flash-messages {
    margin-top: 10px;
}

.drive-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: 0.3s;
}

.sidebar {
    background-color: #343a40;
    min-height: 100vh;
    padding-top: 20px;
}

.sidebar a {
    color: #adb5bd;
    display: block;
    padding: 10px 20px;
    text-decoration: none;
}

.sidebar a:hover {
    color: white;
    background-color: #495057;
}

.sidebar a.active {
    color: white;
    background-color: #0d6efd;
}

.main-content {
    padding: 20px;
}
```

---

## File 5: `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placement Portal - {% block title %}{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>

{% if session.get('user_id') %}
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">
            <i class="bi bi-mortarboard-fill"></i> Placement Portal
        </a>
        <div class="navbar-nav ms-auto">
            <span class="navbar-text text-light me-3">
                Welcome, {{ session.get('username') }} 
                <span class="badge bg-secondary">{{ session.get('role') }}</span>
            </span>
            <a class="nav-link text-light" href="{{ url_for('logout') }}">
                <i class="bi bi-box-arrow-right"></i> Logout
            </a>
        </div>
    </div>
</nav>
{% endif %}

<div class="container-fluid">
    <div class="flash-messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show mt-2" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    {% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## File 6: `templates/login.html`

```html
{% extends 'base.html' %}
{% block title %}Login{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-5">
        <div class="card shadow">
            <div class="card-header bg-dark text-white text-center">
                <h4><i class="bi bi-mortarboard-fill"></i> Placement Portal</h4>
                <p class="mb-0">Login to your account</p>
            </div>
            <div class="card-body p-4">
                <form method="POST" action="{{ url_for('login') }}">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" 
                               name="username" 
                               class="form-control" 
                               placeholder="Enter username"
                               required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" 
                               name="password" 
                               class="form-control" 
                               placeholder="Enter password"
                               required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-dark btn-lg">
                            <i class="bi bi-box-arrow-in-right"></i> Login
                        </button>
                    </div>
                </form>
            </div>
            <div class="card-footer text-center">
                <p class="mb-0">Don't have an account? 
                    <a href="{{ url_for('register') }}">Register here</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 7: `templates/register.html`

```html
{% extends 'base.html' %}
{% block title %}Register{% endblock %}

{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-7">
        <div class="card shadow">
            <div class="card-header bg-dark text-white text-center">
                <h4><i class="bi bi-person-plus-fill"></i> Create Account</h4>
            </div>
            <div class="card-body p-4">
                <form method="POST" action="{{ url_for('register') }}" id="registerForm">

                    <div class="mb-3">
                        <label class="form-label fw-bold">Register As</label>
                        <select name="role" class="form-select" id="roleSelect" required>
                            <option value="">-- Select Role --</option>
                            <option value="student">Student</option>
                            <option value="company">Company</option>
                        </select>
                    </div>

                    <hr>
                    <h6 class="text-muted">Account Details</h6>

                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" 
                               placeholder="Choose a username" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" name="email" class="form-control" 
                               placeholder="Enter email" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" 
                               placeholder="Choose a password" required>
                    </div>

                    <!-- Student Fields -->
                    <div id="studentFields" style="display:none;">
                        <hr>
                        <h6 class="text-muted">Student Details</h6>
                        <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" name="full_name" class="form-control" 
                                   placeholder="Enter full name">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Phone</label>
                            <input type="text" name="phone" class="form-control" 
                                   placeholder="Enter phone number">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Department</label>
                            <input type="text" name="department" class="form-control" 
                                   placeholder="e.g. Computer Science">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">CGPA</label>
                            <input type="number" name="cgpa" class="form-control" 
                                   placeholder="e.g. 8.5" step="0.01" min="0" max="10">
                        </div>
                    </div>

                    <!-- Company Fields -->
                    <div id="companyFields" style="display:none;">
                        <hr>
                        <h6 class="text-muted">Company Details</h6>
                        <div class="mb-3">
                            <label class="form-label">Company Name</label>
                            <input type="text" name="company_name" class="form-control" 
                                   placeholder="Enter company name">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">HR Contact</label>
                            <input type="text" name="hr_contact" class="form-control" 
                                   placeholder="HR email or phone">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Website</label>
                            <input type="text" name="website" class="form-control" 
                                   placeholder="https://yourcompany.com">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Company Description</label>
                            <textarea name="description" class="form-control" 
                                      rows="3" placeholder="About your company"></textarea>
                        </div>
                    </div>

                    <div class="d-grid mt-3">
                        <button type="submit" class="btn btn-dark btn-lg">
                            <i class="bi bi-check-circle"></i> Register
                        </button>
                    </div>

                </form>
            </div>
            <div class="card-footer text-center">
                <p class="mb-0">Already have an account? 
                    <a href="{{ url_for('login') }}">Login here</a>
                </p>
            </div>
        </div>
    </div>
</div>

<script>
    // Show/hide fields based on role selection
    document.getElementById('roleSelect').addEventListener('change', function() {
        var role = this.value;
        document.getElementById('studentFields').style.display = 
            role === 'student' ? 'block' : 'none';
        document.getElementById('companyFields').style.display = 
            role === 'company' ? 'block' : 'none';
    });
</script>
{% endblock %}
```

---

## How To Run Part 1

```bash
# Step 1 - Install requirements
pip install flask flask-sqlalchemy

# Step 2 - Run init to create DB and admin
python init_db.py

# Step 3 - Run app
python app.py

# Step 4 - Open browser
http://127.0.0.1:5000

# Admin Login
Username: admin
Password: admin123
```

---

## Part 1 is Complete ✅

### What Part 1 Contains:
- ✅ `models.py` - All 5 database tables
- ✅ `init_db.py` - Creates DB + Admin user
- ✅ `app.py` - All routes for Admin, Company, Student
- ✅ `style.css` - Clean styling
- ✅ `base.html` - Common layout with navbar
- ✅ `login.html` - Login page
- ✅ `register.html` - Register page with role selection

---

> Reply **"continue part 2"** and I will give all the HTML templates for Admin, Company and Student dashboards