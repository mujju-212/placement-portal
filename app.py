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
    previous_status = company.approval_status
    company.approval_status = 'approved'

    user = User.query.get(company.user_id)
    if user:
        user.is_active = True

    db.session.commit()

    if previous_status == 'blacklisted':
        flash(f'{company.company_name} has been re-approved and unblocked!', 'success')
    else:
        flash(f'{company.company_name} has been approved!', 'success')

    return redirect(url_for('admin_companies'))


@app.route('/admin/company/<int:company_id>/reject', methods=['POST'])
def admin_reject_company(company_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    company = Company.query.get_or_404(company_id)
    company.approval_status = 'rejected'

    user = User.query.get(company.user_id)
    if user:
        user.is_active = True

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


@app.route('/admin/student/<int:student_id>/unblacklist', methods=['POST'])
def admin_unblacklist_student(student_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    if user:
        user.is_active = True

    db.session.commit()
    flash(f'{student.full_name} has been re-approved and unblocked!', 'success')
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
