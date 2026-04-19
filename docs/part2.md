# PART 2 - All HTML Templates

## File 8: `templates/admin/dashboard.html`

```html
{% extends 'base.html' %}
{% block title %}Admin Dashboard{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Admin Panel</h6>
        <a href="{{ url_for('admin_dashboard') }}" class="active">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('admin_companies') }}">
            <i class="bi bi-building"></i> Companies
        </a>
        <a href="{{ url_for('admin_students') }}">
            <i class="bi bi-people"></i> Students
        </a>
        <a href="{{ url_for('admin_drives') }}">
            <i class="bi bi-briefcase"></i> Drives
        </a>
        <a href="{{ url_for('admin_applications') }}">
            <i class="bi bi-file-text"></i> Applications
        </a>
        <a href="{{ url_for('admin_search') }}">
            <i class="bi bi-search"></i> Search
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-speedometer2"></i> Admin Dashboard
        </h3>

        <!-- Stat Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="stat-card bg-students">
                    <h2>{{ total_students }}</h2>
                    <p><i class="bi bi-people-fill"></i> Total Students</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card bg-companies">
                    <h2>{{ total_companies }}</h2>
                    <p><i class="bi bi-building"></i> Total Companies</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card bg-drives">
                    <h2>{{ total_drives }}</h2>
                    <p><i class="bi bi-briefcase"></i> Total Drives</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card bg-applications">
                    <h2>{{ total_applications }}</h2>
                    <p><i class="bi bi-file-text"></i> Total Applications</p>
                </div>
            </div>
        </div>

        <!-- Pending Company Approvals -->
        <div class="card mb-4">
            <div class="card-header bg-warning text-dark">
                <i class="bi bi-clock"></i> 
                Pending Company Approvals ({{ pending_companies|length }})
            </div>
            <div class="card-body">
                {% if pending_companies %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Company Name</th>
                            <th>HR Contact</th>
                            <th>Website</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for company in pending_companies %}
                        <tr>
                            <td>{{ company.company_name }}</td>
                            <td>{{ company.hr_contact }}</td>
                            <td>{{ company.website or 'N/A' }}</td>
                            <td>
                                <form method="POST" 
                                      action="{{ url_for('admin_approve_company', company_id=company.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-success btn-sm">
                                        <i class="bi bi-check"></i> Approve
                                    </button>
                                </form>
                                <form method="POST" 
                                      action="{{ url_for('admin_reject_company', company_id=company.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-danger btn-sm">
                                        <i class="bi bi-x"></i> Reject
                                    </button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted mb-0">No pending company approvals</p>
                {% endif %}
            </div>
        </div>

        <!-- Pending Drive Approvals -->
        <div class="card">
            <div class="card-header bg-info text-white">
                <i class="bi bi-briefcase"></i> 
                Pending Drive Approvals ({{ pending_drives|length }})
            </div>
            <div class="card-body">
                {% if pending_drives %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Drive Name</th>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Deadline</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for drive in pending_drives %}
                        <tr>
                            <td>{{ drive.drive_name }}</td>
                            <td>{{ drive.company.company_name }}</td>
                            <td>{{ drive.job_title }}</td>
                            <td>{{ drive.deadline }}</td>
                            <td>
                                <form method="POST" 
                                      action="{{ url_for('admin_approve_drive', drive_id=drive.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-success btn-sm">
                                        <i class="bi bi-check"></i> Approve
                                    </button>
                                </form>
                                <form method="POST" 
                                      action="{{ url_for('admin_reject_drive', drive_id=drive.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-danger btn-sm">
                                        <i class="bi bi-x"></i> Reject
                                    </button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted mb-0">No pending drive approvals</p>
                {% endif %}
            </div>
        </div>

    </div>
</div>
{% endblock %}
```

---

## File 9: `templates/admin/companies.html`

```html
{% extends 'base.html' %}
{% block title %}Manage Companies{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Admin Panel</h6>
        <a href="{{ url_for('admin_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('admin_companies') }}" class="active">
            <i class="bi bi-building"></i> Companies
        </a>
        <a href="{{ url_for('admin_students') }}">
            <i class="bi bi-people"></i> Students
        </a>
        <a href="{{ url_for('admin_drives') }}">
            <i class="bi bi-briefcase"></i> Drives
        </a>
        <a href="{{ url_for('admin_applications') }}">
            <i class="bi bi-file-text"></i> Applications
        </a>
        <a href="{{ url_for('admin_search') }}">
            <i class="bi bi-search"></i> Search
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-building"></i> Manage Companies
        </h3>

        <!-- Search -->
        <div class="card mb-4">
            <div class="card-body">
                <form method="GET" action="{{ url_for('admin_companies') }}" 
                      class="row g-2">
                    <div class="col-md-9">
                        <input type="text" name="search" class="form-control"
                               placeholder="Search by company name..."
                               value="{{ search }}">
                    </div>
                    <div class="col-md-3">
                        <button type="submit" class="btn btn-dark w-100">
                            <i class="bi bi-search"></i> Search
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Companies Table -->
        <div class="card">
            <div class="card-header bg-dark text-white">
                All Companies ({{ companies|length }})
            </div>
            <div class="card-body">
                {% if companies %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Company Name</th>
                            <th>HR Contact</th>
                            <th>Website</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for company in companies %}
                        <tr>
                            <td>{{ company.id }}</td>
                            <td>{{ company.company_name }}</td>
                            <td>{{ company.hr_contact }}</td>
                            <td>{{ company.website or 'N/A' }}</td>
                            <td>
                                <span class="badge badge-{{ company.approval_status }}">
                                    {{ company.approval_status | upper }}
                                </span>
                            </td>
                            <td>
                                {% if company.approval_status == 'pending' %}
                                <form method="POST" 
                                      action="{{ url_for('admin_approve_company', company_id=company.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-success btn-sm">
                                        Approve
                                    </button>
                                </form>
                                <form method="POST" 
                                      action="{{ url_for('admin_reject_company', company_id=company.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-warning btn-sm">
                                        Reject
                                    </button>
                                </form>
                                {% endif %}

                                {% if company.approval_status != 'blacklisted' %}
                                <form method="POST" 
                                      action="{{ url_for('admin_blacklist_company', company_id=company.id) }}" 
                                      style="display:inline;"
                                      onsubmit="return confirm('Blacklist this company?')">
                                    <button class="btn btn-secondary btn-sm">
                                        Blacklist
                                    </button>
                                </form>
                                {% endif %}

                                <form method="POST" 
                                      action="{{ url_for('admin_delete_company', company_id=company.id) }}" 
                                      style="display:inline;"
                                      onsubmit="return confirm('Delete this company permanently?')">
                                    <button class="btn btn-danger btn-sm">
                                        Delete
                                    </button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">No companies found.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 10: `templates/admin/students.html`

```html
{% extends 'base.html' %}
{% block title %}Manage Students{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Admin Panel</h6>
        <a href="{{ url_for('admin_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('admin_companies') }}">
            <i class="bi bi-building"></i> Companies
        </a>
        <a href="{{ url_for('admin_students') }}" class="active">
            <i class="bi bi-people"></i> Students
        </a>
        <a href="{{ url_for('admin_drives') }}">
            <i class="bi bi-briefcase"></i> Drives
        </a>
        <a href="{{ url_for('admin_applications') }}">
            <i class="bi bi-file-text"></i> Applications
        </a>
        <a href="{{ url_for('admin_search') }}">
            <i class="bi bi-search"></i> Search
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-people"></i> Manage Students
        </h3>

        <!-- Search -->
        <div class="card mb-4">
            <div class="card-body">
                <form method="GET" action="{{ url_for('admin_students') }}" 
                      class="row g-2">
                    <div class="col-md-9">
                        <input type="text" name="search" class="form-control"
                               placeholder="Search by name, email or phone..."
                               value="{{ search }}">
                    </div>
                    <div class="col-md-3">
                        <button type="submit" class="btn btn-dark w-100">
                            <i class="bi bi-search"></i> Search
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Students Table -->
        <div class="card">
            <div class="card-header bg-dark text-white">
                All Students ({{ students|length }})
            </div>
            <div class="card-body">
                {% if students %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Department</th>
                            <th>CGPA</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for student in students %}
                        <tr>
                            <td>{{ student.id }}</td>
                            <td>{{ student.full_name }}</td>
                            <td>{{ student.email }}</td>
                            <td>{{ student.phone or 'N/A' }}</td>
                            <td>{{ student.department or 'N/A' }}</td>
                            <td>{{ student.cgpa or 'N/A' }}</td>
                            <td>
                                {% if student.user.is_active %}
                                    <span class="badge bg-success">Active</span>
                                {% else %}
                                    <span class="badge bg-danger">Blacklisted</span>
                                {% endif %}
                            </td>
                            <td>
                                {% if student.user.is_active %}
                                <form method="POST" 
                                      action="{{ url_for('admin_blacklist_student', student_id=student.id) }}" 
                                      style="display:inline;"
                                      onsubmit="return confirm('Blacklist this student?')">
                                    <button class="btn btn-secondary btn-sm">
                                        Blacklist
                                    </button>
                                </form>
                                {% endif %}
                                <form method="POST" 
                                      action="{{ url_for('admin_delete_student', student_id=student.id) }}" 
                                      style="display:inline;"
                                      onsubmit="return confirm('Delete this student permanently?')">
                                    <button class="btn btn-danger btn-sm">
                                        Delete
                                    </button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">No students found.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 11: `templates/admin/drives.html`

```html
{% extends 'base.html' %}
{% block title %}Manage Drives{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Admin Panel</h6>
        <a href="{{ url_for('admin_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('admin_companies') }}">
            <i class="bi bi-building"></i> Companies
        </a>
        <a href="{{ url_for('admin_students') }}">
            <i class="bi bi-people"></i> Students
        </a>
        <a href="{{ url_for('admin_drives') }}" class="active">
            <i class="bi bi-briefcase"></i> Drives
        </a>
        <a href="{{ url_for('admin_applications') }}">
            <i class="bi bi-file-text"></i> Applications
        </a>
        <a href="{{ url_for('admin_search') }}">
            <i class="bi bi-search"></i> Search
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-briefcase"></i> Manage Placement Drives
        </h3>

        <div class="card">
            <div class="card-header bg-dark text-white">
                All Placement Drives ({{ drives|length }})
            </div>
            <div class="card-body">
                {% if drives %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Drive Name</th>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Deadline</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for drive in drives %}
                        <tr>
                            <td>{{ drive.id }}</td>
                            <td>{{ drive.drive_name }}</td>
                            <td>{{ drive.company.company_name }}</td>
                            <td>{{ drive.job_title }}</td>
                            <td>{{ drive.deadline }}</td>
                            <td>
                                <span class="badge badge-{{ drive.status }}">
                                    {{ drive.status | upper }}
                                </span>
                            </td>
                            <td>
                                {% if drive.status == 'pending' %}
                                <form method="POST" 
                                      action="{{ url_for('admin_approve_drive', drive_id=drive.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-success btn-sm">
                                        Approve
                                    </button>
                                </form>
                                <form method="POST" 
                                      action="{{ url_for('admin_reject_drive', drive_id=drive.id) }}" 
                                      style="display:inline;">
                                    <button class="btn btn-danger btn-sm">
                                        Reject
                                    </button>
                                </form>
                                {% elif drive.status == 'approved' %}
                                <span class="text-success">
                                    <i class="bi bi-check-circle"></i> Approved
                                </span>
                                {% elif drive.status == 'closed' %}
                                <span class="text-secondary">
                                    <i class="bi bi-lock"></i> Closed
                                </span>
                                {% elif drive.status == 'rejected' %}
                                <span class="text-danger">
                                    <i class="bi bi-x-circle"></i> Rejected
                                </span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">No placement drives found.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 12: `templates/admin/applications.html`

```html
{% extends 'base.html' %}
{% block title %}All Applications{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Admin Panel</h6>
        <a href="{{ url_for('admin_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('admin_companies') }}">
            <i class="bi bi-building"></i> Companies
        </a>
        <a href="{{ url_for('admin_students') }}">
            <i class="bi bi-people"></i> Students
        </a>
        <a href="{{ url_for('admin_drives') }}">
            <i class="bi bi-briefcase"></i> Drives
        </a>
        <a href="{{ url_for('admin_applications') }}" class="active">
            <i class="bi bi-file-text"></i> Applications
        </a>
        <a href="{{ url_for('admin_search') }}">
            <i class="bi bi-search"></i> Search
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-file-text"></i> All Applications
        </h3>

        <div class="card">
            <div class="card-header bg-dark text-white">
                Total Applications ({{ applications|length }})
            </div>
            <div class="card-body">
                {% if applications %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>App ID</th>
                            <th>Student Name</th>
                            <th>Department</th>
                            <th>Drive Name</th>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Applied Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for app in applications %}
                        <tr>
                            <td>{{ app.id }}</td>
                            <td>{{ app.student.full_name }}</td>
                            <td>{{ app.student.department or 'N/A' }}</td>
                            <td>{{ app.drive.drive_name }}</td>
                            <td>{{ app.drive.company.company_name }}</td>
                            <td>{{ app.drive.job_title }}</td>
                            <td>{{ app.applied_date.strftime('%d-%m-%Y') }}</td>
                            <td>
                                <span class="badge badge-{{ app.status }}">
                                    {{ app.status | upper }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">No applications found.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 13: `templates/admin/search.html`

```html
{% extends 'base.html' %}
{% block title %}Search{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Admin Panel</h6>
        <a href="{{ url_for('admin_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('admin_companies') }}">
            <i class="bi bi-building"></i> Companies
        </a>
        <a href="{{ url_for('admin_students') }}">
            <i class="bi bi-people"></i> Students
        </a>
        <a href="{{ url_for('admin_drives') }}">
            <i class="bi bi-briefcase"></i> Drives
        </a>
        <a href="{{ url_for('admin_applications') }}">
            <i class="bi bi-file-text"></i> Applications
        </a>
        <a href="{{ url_for('admin_search') }}" class="active">
            <i class="bi bi-search"></i> Search
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-search"></i> Search
        </h3>

        <div class="card mb-4">
            <div class="card-body">
                <form method="GET" action="{{ url_for('admin_search') }}" 
                      class="row g-2">
                    <div class="col-md-5">
                        <input type="text" name="q" class="form-control"
                               placeholder="Enter search term..."
                               value="{{ query }}">
                    </div>
                    <div class="col-md-4">
                        <select name="type" class="form-select">
                            <option value="student" 
                                {% if search_type == 'student' %}selected{% endif %}>
                                Search Students
                            </option>
                            <option value="company" 
                                {% if search_type == 'company' %}selected{% endif %}>
                                Search Companies
                            </option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <button type="submit" class="btn btn-dark w-100">
                            <i class="bi bi-search"></i> Search
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Student Results -->
        {% if search_type == 'student' and query %}
        <div class="card">
            <div class="card-header bg-dark text-white">
                Student Results ({{ students|length }})
            </div>
            <div class="card-body">
                {% if students %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Department</th>
                            <th>CGPA</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for student in students %}
                        <tr>
                            <td>{{ student.id }}</td>
                            <td>{{ student.full_name }}</td>
                            <td>{{ student.email }}</td>
                            <td>{{ student.phone or 'N/A' }}</td>
                            <td>{{ student.department or 'N/A' }}</td>
                            <td>{{ student.cgpa or 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">No students found for "{{ query }}"</p>
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- Company Results -->
        {% if search_type == 'company' and query %}
        <div class="card">
            <div class="card-header bg-dark text-white">
                Company Results ({{ companies|length }})
            </div>
            <div class="card-body">
                {% if companies %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Company Name</th>
                            <th>HR Contact</th>
                            <th>Website</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for company in companies %}
                        <tr>
                            <td>{{ company.id }}</td>
                            <td>{{ company.company_name }}</td>
                            <td>{{ company.hr_contact }}</td>
                            <td>{{ company.website or 'N/A' }}</td>
                            <td>
                                <span class="badge badge-{{ company.approval_status }}">
                                    {{ company.approval_status | upper }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">No companies found for "{{ query }}"</p>
                {% endif %}
            </div>
        </div>
        {% endif %}

    </div>
</div>
{% endblock %}
```

---

## File 14: `templates/company/dashboard.html`

```html
{% extends 'base.html' %}
{% block title %}Company Dashboard{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Company Panel</h6>
        <a href="{{ url_for('company_dashboard') }}" class="active">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('company_create_drive') }}">
            <i class="bi bi-plus-circle"></i> Create Drive
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-2">
            <i class="bi bi-building"></i> {{ company.company_name }}
        </h3>

        <!-- Company Info Card -->
        <div class="card mb-4">
            <div class="card-header bg-dark text-white">
                Company Profile
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>
                        <p><strong>Website:</strong> 
                            {{ company.website or 'Not provided' }}
                        </p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Status:</strong>
                            <span class="badge badge-{{ company.approval_status }}">
                                {{ company.approval_status | upper }}
                            </span>
                        </p>
                        <p><strong>Description:</strong> 
                            {{ company.description or 'Not provided' }}
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create Drive Button -->
        <div class="mb-3">
            <a href="{{ url_for('company_create_drive') }}" 
               class="btn btn-dark">
                <i class="bi bi-plus-circle"></i> Create New Drive
            </a>
        </div>

        <!-- Drives Table -->
        <div class="card">
            <div class="card-header bg-dark text-white">
                <i class="bi bi-briefcase"></i> 
                My Placement Drives ({{ drive_data|length }})
            </div>
            <div class="card-body">
                {% if drive_data %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Drive Name</th>
                            <th>Job Title</th>
                            <th>Deadline</th>
                            <th>Applicants</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in drive_data %}
                        <tr>
                            <td>{{ item.drive.drive_name }}</td>
                            <td>{{ item.drive.job_title }}</td>
                            <td>{{ item.drive.deadline }}</td>
                            <td>
                                <span class="badge bg-primary">
                                    {{ item.applicant_count }}
                                </span>
                            </td>
                            <td>
                                <span class="badge badge-{{ item.drive.status }}">
                                    {{ item.drive.status | upper }}
                                </span>
                            </td>
                            <td>
                                <a href="{{ url_for('company_drive_applications', drive_id=item.drive.id) }}" 
                                   class="btn btn-info btn-sm text-white">
                                    <i class="bi bi-eye"></i> View Apps
                                </a>
                                <a href="{{ url_for('company_edit_drive', drive_id=item.drive.id) }}" 
                                   class="btn btn-warning btn-sm">
                                    <i class="bi bi-pencil"></i> Edit
                                </a>
                                {% if item.drive.status != 'closed' %}
                                <form method="POST" 
                                      action="{{ url_for('company_close_drive', drive_id=item.drive.id) }}" 
                                      style="display:inline;"
                                      onsubmit="return confirm('Close this drive?')">
                                    <button class="btn btn-secondary btn-sm">
                                        <i class="bi bi-lock"></i> Close
                                    </button>
                                </form>
                                {% endif %}
                                <form method="POST" 
                                      action="{{ url_for('company_delete_drive', drive_id=item.drive.id) }}" 
                                      style="display:inline;"
                                      onsubmit="return confirm('Delete this drive?')">
                                    <button class="btn btn-danger btn-sm">
                                        <i class="bi bi-trash"></i> Delete
                                    </button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="text-center py-4">
                    <p class="text-muted">No drives created yet.</p>
                    <a href="{{ url_for('company_create_drive') }}" 
                       class="btn btn-dark">
                        Create Your First Drive
                    </a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 15: `templates/company/create_drive.html`

```html
{% extends 'base.html' %}
{% block title %}Create Drive{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Company Panel</h6>
        <a href="{{ url_for('company_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('company_create_drive') }}" class="active">
            <i class="bi bi-plus-circle"></i> Create Drive
        </a>
    </div>

    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-plus-circle"></i> Create New Placement Drive
        </h3>

        <div class="card">
            <div class="card-header bg-dark text-white">
                Drive Details
            </div>
            <div class="card-body">
                <form method="POST" action="{{ url_for('company_create_drive') }}">

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">
                                Drive Name <span class="text-danger">*</span>
                            </label>
                            <input type="text" name="drive_name" 
                                   class="form-control"
                                   placeholder="e.g. Campus Hiring 2025" 
                                   required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">
                                Job Title <span class="text-danger">*</span>
                            </label>
                            <input type="text" name="job_title" 
                                   class="form-control"
                                   placeholder="e.g. Software Developer" 
                                   required>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-bold">
                            Job Description <span class="text-danger">*</span>
                        </label>
                        <textarea name="job_description" class="form-control" 
                                  rows="4"
                                  placeholder="Describe the job role and responsibilities"
                                  required></textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Eligibility Criteria</label>
                        <input type="text" name="eligibility" 
                               class="form-control"
                               placeholder="e.g. CGPA > 7.0, CSE/IT students only">
                    </div>

                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">
                                Application Deadline <span class="text-danger">*</span>
                            </label>
                            <input type="date" name="deadline" 
                                   class="form-control" required>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Salary Package</label>
                            <input type="text" name="salary" 
                                   class="form-control"
                                   placeholder="e.g. 6 LPA">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Location</label>
                            <input type="text" name="location" 
                                   class="form-control"
                                   placeholder="e.g. Bangalore">
                        </div>
                    </div>

                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-dark">
                            <i class="bi bi-check-circle"></i> Create Drive
                        </button>
                        <a href="{{ url_for('company_dashboard') }}" 
                           class="btn btn-secondary">
                            Cancel
                        </a>
                    </div>

                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 16: `templates/company/edit_drive.html`

```html
{% extends 'base.html' %}
{% block title %}Edit Drive{% endblock %}

{% block content %}
<div class="row mt-3">
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Company Panel</h6>
        <a href="{{ url_for('company_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('company_create_drive') }}">
            <i class="bi bi-plus-circle"></i> Create Drive
        </a>
    </div>

    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-pencil"></i> Edit Drive
        </h3>

        <div class="card">
            <div class="card-header bg-dark text-white">
                Edit: {{ drive.drive_name }}
            </div>
            <div class="card-body">
                <form method="POST" 
                      action="{{ url_for('company_edit_drive', drive_id=drive.id) }}">

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Drive Name</label>
                            <input type="text" name="drive_name" 
                                   class="form-control"
                                   value="{{ drive.drive_name }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Job Title</label>
                            <input type="text" name="job_title" 
                                   class="form-control"
                                   value="{{ drive.job_title }}" required>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Job Description</label>
                        <textarea name="job_description" class="form-control" 
                                  rows="4" required>{{ drive.job_description }}</textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Eligibility Criteria</label>
                        <input type="text" name="eligibility" 
                               class="form-control"
                               value="{{ drive.eligibility or '' }}">
                    </div>

                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Deadline</label>
                            <input type="date" name="deadline" 
                                   class="form-control"
                                   value="{{ drive.deadline }}" required>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Salary</label>
                            <input type="text" name="salary" 
                                   class="form-control"
                                   value="{{ drive.salary or '' }}">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Location</label>
                            <input type="text" name="location" 
                                   class="form-control"
                                   value="{{ drive.location or '' }}">
                        </div>
                    </div>

                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i>
                        After editing, the drive will go back to 
                        <strong>Pending</strong> status for admin approval.
                    </div>

                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-dark">
                            <i class="bi bi-check-circle"></i> Save Changes
                        </button>
                        <a href="{{ url_for('company_dashboard') }}" 
                           class="btn btn-secondary">
                            Cancel
                        </a>
                    </div>

                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 17: `templates/company/applications.html`

```html
{% extends 'base.html' %}
{% block title %}Drive Applications{% endblock %}

{% block content %}
<div class="row mt-3">
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Company Panel</h6>
        <a href="{{ url_for('company_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('company_create_drive') }}">
            <i class="bi bi-plus-circle"></i> Create Drive
        </a>
    </div>

    <div class="col-md-10 main-content">
        <h3 class="mb-2">
            <i class="bi bi-people"></i> Applications for: {{ drive.drive_name }}
        </h3>
        <p class="text-muted mb-4">
            Job Title: {{ drive.job_title }} | 
            Deadline: {{ drive.deadline }} |
            Status: 
            <span class="badge badge-{{ drive.status }}">
                {{ drive.status | upper }}
            </span>
        </p>

        <div class="card">
            <div class="card-header bg-dark text-white">
                Received Applications ({{ applications|length }})
            </div>
            <div class="card-body">
                {% if applications %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Student Name</th>
                            <th>Department</th>
                            <th>CGPA</th>
                            <th>Phone</th>
                            <th>Applied Date</th>
                            <th>Resume</th>
                            <th>Status</th>
                            <th>Update Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for app in applications %}
                        <tr>
                            <td>{{ app.student.full_name }}</td>
                            <td>{{ app.student.department or 'N/A' }}</td>
                            <td>{{ app.student.cgpa or 'N/A' }}</td>
                            <td>{{ app.student.phone or 'N/A' }}</td>
                            <td>{{ app.applied_date.strftime('%d-%m-%Y') }}</td>
                            <td>
                                {% if app.student.resume_filename %}
                                <a href="{{ url_for('static', filename='uploads/resumes/' + app.student.resume_filename) }}" 
                                   target="_blank" class="btn btn-outline-dark btn-sm">
                                    <i class="bi bi-file-pdf"></i> View
                                </a>
                                {% else %}
                                <span class="text-muted">No resume</span>
                                {% endif %}
                            </td>
                            <td>
                                <span class="badge badge-{{ app.status }}">
                                    {{ app.status | upper }}
                                </span>
                            </td>
                            <td>
                                <form method="POST" 
                                      action="{{ url_for('company_update_application', app_id=app.id) }}">
                                    <div class="d-flex gap-1">
                                        <select name="status" class="form-select form-select-sm">
                                            <option value="applied" 
                                                {% if app.status == 'applied' %}selected{% endif %}>
                                                Applied
                                            </option>
                                            <option value="shortlisted" 
                                                {% if app.status == 'shortlisted' %}selected{% endif %}>
                                                Shortlisted
                                            </option>
                                            <option value="selected" 
                                                {% if app.status == 'selected' %}selected{% endif %}>
                                                Selected
                                            </option>
                                            <option value="rejected" 
                                                {% if app.status == 'rejected' %}selected{% endif %}>
                                                Rejected
                                            </option>
                                        </select>
                                        <button type="submit" class="btn btn-dark btn-sm">
                                            Save
                                        </button>
                                    </div>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="text-center py-4">
                    <p class="text-muted">No applications received yet for this drive.</p>
                </div>
                {% endif %}
            </div>
        </div>

        <div class="mt-3">
            <a href="{{ url_for('company_dashboard') }}" class="btn btn-secondary">
                <i class="bi bi-arrow-left"></i> Back to Dashboard
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 18: `templates/student/dashboard.html`

```html
{% extends 'base.html' %}
{% block title %}Student Dashboard{% endblock %}

{% block content %}
<div class="row mt-3">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Student Panel</h6>
        <a href="{{ url_for('student_dashboard') }}" class="active">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('student_profile') }}">
            <i class="bi bi-person"></i> My Profile
        </a>
        <a href="{{ url_for('student_history') }}">
            <i class="bi bi-clock-history"></i> History
        </a>
    </div>

    <!-- Main Content -->
    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            Welcome, {{ student.full_name }}!
        </h3>

        <!-- Available Drives -->
        <div class="card mb-4">
            <div class="card-header bg-dark text-white">
                <i class="bi bi-briefcase"></i> 
                Available Placement Drives ({{ approved_drives|length }})
            </div>
            <div class="card-body">
                {% if approved_drives %}
                <div class="row">
                    {% for drive in approved_drives %}
                    <div class="col-md-6 mb-3">
                        <div class="card drive-card h-100">
                            <div class="card-body">
                                <h5 class="card-title">{{ drive.job_title }}</h5>
                                <h6 class="text-muted">
                                    {{ drive.company.company_name }}
                                </h6>
                                <p class="mb-1">
                                    <i class="bi bi-geo-alt"></i> 
                                    {{ drive.location or 'Not specified' }}
                                </p>
                                <p class="mb-1">
                                    <i class="bi bi-currency-rupee"></i> 
                                    {{ drive.salary or 'Not specified' }}
                                </p>
                                <p class="mb-2">
                                    <i class="bi bi-calendar"></i> 
                                    Deadline: {{ drive.deadline }}
                                </p>

                                {% if drive.id in applied_drive_ids %}
                                <span class="badge bg-success">
                                    <i class="bi bi-check-circle"></i> Already Applied
                                </span>
                                {% else %}
                                <a href="{{ url_for('student_drive_detail', drive_id=drive.id) }}" 
                                   class="btn btn-dark btn-sm">
                                    View & Apply
                                </a>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <p class="text-muted">No approved placement drives available right now.</p>
                {% endif %}
            </div>
        </div>

        <!-- My Applications -->
        <div class="card">
            <div class="card-header bg-dark text-white">
                <i class="bi bi-file-text"></i> 
                My Applications ({{ my_applications|length }})
            </div>
            <div class="card-body">
                {% if my_applications %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Drive Name</th>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Applied Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for app in my_applications %}
                        <tr>
                            <td>{{ app.drive.drive_name }}</td>
                            <td>{{ app.drive.company.company_name }}</td>
                            <td>{{ app.drive.job_title }}</td>
                            <td>{{ app.applied_date.strftime('%d-%m-%Y') }}</td>
                            <td>
                                <span class="badge badge-{{ app.status }}">
                                    {{ app.status | upper }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted">You have not applied to any drives yet.</p>
                {% endif %}
            </div>
        </div>

    </div>
</div>
{% endblock %}
```

---

## File 19: `templates/student/profile.html`

```html
{% extends 'base.html' %}
{% block title %}My Profile{% endblock %}

{% block content %}
<div class="row mt-3">
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Student Panel</h6>
        <a href="{{ url_for('student_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('student_profile') }}" class="active">
            <i class="bi bi-person"></i> My Profile
        </a>
        <a href="{{ url_for('student_history') }}">
            <i class="bi bi-clock-history"></i> History
        </a>
    </div>

    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-person-circle"></i> My Profile
        </h3>

        <div class="card">
            <div class="card-header bg-dark text-white">
                Edit Profile
            </div>
            <div class="card-body">
                <form method="POST" 
                      action="{{ url_for('student_profile') }}" 
                      enctype="multipart/form-data">

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Full Name</label>
                            <input type="text" name="full_name" 
                                   class="form-control"
                                   value="{{ student.full_name }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Email</label>
                            <input type="email" class="form-control"
                                   value="{{ student.email }}" disabled>
                            <small class="text-muted">Email cannot be changed</small>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Phone</label>
                            <input type="text" name="phone" 
                                   class="form-control"
                                   value="{{ student.phone or '' }}"
                                   placeholder="Enter phone number">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Department</label>
                            <input type="text" name="department" 
                                   class="form-control"
                                   value="{{ student.department or '' }}"
                                   placeholder="e.g. Computer Science">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">CGPA</label>
                            <input type="number" name="cgpa" 
                                   class="form-control"
                                   value="{{ student.cgpa or '' }}"
                                   step="0.01" min="0" max="10"
                                   placeholder="e.g. 8.5">
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Upload Resume (PDF)</label>
                        <input type="file" name="resume" 
                               class="form-control" accept=".pdf">
                        {% if student.resume_filename %}
                        <small class="text-success">
                            <i class="bi bi-check-circle"></i>
                            Resume uploaded: {{ student.resume_filename }}
                            <a href="{{ url_for('static', filename='uploads/resumes/' + student.resume_filename) }}" 
                               target="_blank" class="ms-2">View</a>
                        </small>
                        {% else %}
                        <small class="text-muted">No resume uploaded yet</small>
                        {% endif %}
                    </div>

                    <button type="submit" class="btn btn-dark">
                        <i class="bi bi-check-circle"></i> Save Profile
                    </button>

                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 20: `templates/student/drive_detail.html`

```html
{% extends 'base.html' %}
{% block title %}Drive Details{% endblock %}

{% block content %}
<div class="row mt-3">
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Student Panel</h6>
        <a href="{{ url_for('student_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('student_profile') }}">
            <i class="bi bi-person"></i> My Profile
        </a>
        <a href="{{ url_for('student_history') }}">
            <i class="bi bi-clock-history"></i> History
        </a>
    </div>

    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-briefcase"></i> Drive Details
        </h3>

        <div class="card">
            <div class="card-header bg-dark text-white">
                {{ drive.drive_name }}
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <h4>{{ drive.job_title }}</h4>
                        <h6 class="text-muted mb-3">
                            {{ drive.company.company_name }}
                        </h6>

                        <table class="table table-borderless">
                            <tr>
                                <td class="fw-bold" style="width:200px;">
                                    Job Description
                                </td>
                                <td>{{ drive.job_description }}</td>
                            </tr>
                            <tr>
                                <td class="fw-bold">Eligibility</td>
                                <td>{{ drive.eligibility or 'Open to all' }}</td>
                            </tr>
                            <tr>
                                <td class="fw-bold">Salary Package</td>
                                <td>{{ drive.salary or 'Not disclosed' }}</td>
                            </tr>
                            <tr>
                                <td class="fw-bold">Location</td>
                                <td>{{ drive.location or 'Not specified' }}</td>
                            </tr>
                            <tr>
                                <td class="fw-bold">Application Deadline</td>
                                <td>{{ drive.deadline }}</td>
                            </tr>
                        </table>

                        <div class="mt-3">
                            {% if already_applied %}
                            <div class="alert alert-success">
                                <i class="bi bi-check-circle-fill"></i>
                                You have already applied for this drive!
                                <br>
                                Status: 
                                <strong>{{ already_applied.status | upper }}</strong>
                            </div>
                            {% else %}
                            <form method="POST" 
                                  action="{{ url_for('student_apply', drive_id=drive.id) }}"
                                  onsubmit="return confirm('Apply for this drive?')">
                                <button type="submit" class="btn btn-dark btn-lg">
                                    <i class="bi bi-send"></i> Apply Now
                                </button>
                            </form>
                            {% endif %}
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <i class="bi bi-building" 
                                   style="font-size:3rem;color:#333;"></i>
                                <h5 class="mt-2">
                                    {{ drive.company.company_name }}
                                </h5>
                                {% if drive.company.website %}
                                <a href="{{ drive.company.website }}" 
                                   target="_blank" class="btn btn-outline-dark btn-sm">
                                    Visit Website
                                </a>
                                {% endif %}
                                <hr>
                                <p class="text-muted small">
                                    {{ drive.company.description or '' }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="mt-3">
            <a href="{{ url_for('student_dashboard') }}" 
               class="btn btn-secondary">
                <i class="bi bi-arrow-left"></i> Back to Dashboard
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## File 21: `templates/student/history.html`

```html
{% extends 'base.html' %}
{% block title %}Application History{% endblock %}

{% block content %}
<div class="row mt-3">
    <div class="col-md-2 sidebar">
        <h6 class="text-white text-center mb-3">Student Panel</h6>
        <a href="{{ url_for('student_dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{{ url_for('student_profile') }}">
            <i class="bi bi-person"></i> My Profile
        </a>
        <a href="{{ url_for('student_history') }}" class="active">
            <i class="bi bi-clock-history"></i> History
        </a>
    </div>

    <div class="col-md-10 main-content">
        <h3 class="mb-4">
            <i class="bi bi-clock-history"></i> 
            Application History - {{ student.full_name }}
        </h3>

        <!-- Summary Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-center p-3 border-primary">
                    <h4 class="text-primary">{{ applications|length }}</h4>
                    <p class="mb-0">Total Applied</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center p-3 border-warning">
                    <h4 class="text-warning">
                        {{ applications | selectattr('status','eq','shortlisted') | list | length }}
                    </h4>
                    <p class="mb-0">Shortlisted</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center p-3 border-success">
                    <h4 class="text-success">
                        {{ applications | selectattr('status','eq','selected') | list | length }}
                    </h4>
                    <p class="mb-0">Selected</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center p-3 border-danger">
                    <h4 class="text-danger">
                        {{ applications | selectattr('status','eq','rejected') | list | length }}
                    </h4>
                    <p class="mb-0">Rejected</p>
                </div>
            </div>
        </div>

        <!-- History Table -->
        <div class="card">
            <div class="card-header bg-dark text-white">
                Complete Application History
            </div>
            <div class="card-body">
                {% if applications %}
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Drive Name</th>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Location</th>
                            <th>Salary</th>
                            <th>Applied Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for app in applications %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td>{{ app.drive.drive_name }}</td>
                            <td>{{ app.drive.company.company_name }}</td>
                            <td>{{ app.drive.job_title }}</td>
                            <td>{{ app.drive.location or 'N/A' }}</td>
                            <td>{{ app.drive.salary or 'N/A' }}</td>
                            <td>{{ app.applied_date.strftime('%d-%m-%Y') }}</td>
                            <td>
                                <span class="badge badge-{{ app.status }}">
                                    {{ app.status | upper }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size:3rem;color:#ccc;"></i>
                    <p class="text-muted mt-2">
                        No application history yet. 
                        <a href="{{ url_for('student_dashboard') }}">
                            Browse drives
                        </a>
                    </p>
                </div>
                {% endif %}
            </div>
        </div>

    </div>
</div>
{% endblock %}
```

---

## Final Folder Structure Check

```
placement_portal/
├── app.py                        ✅
├── models.py                     ✅
├── init_db.py                    ✅
├── static/
│   ├── css/
│   │   └── style.css             ✅
│   └── uploads/
│       └── resumes/              ✅ (auto created)
└── templates/
    ├── base.html                 ✅
    ├── login.html                ✅
    ├── register.html             ✅
    ├── admin/
    │   ├── dashboard.html        ✅
    │   ├── companies.html        ✅
    │   ├── students.html         ✅
    │   ├── drives.html           ✅
    │   ├── applications.html     ✅
    │   └── search.html           ✅
    ├── company/
    │   ├── dashboard.html        ✅
    │   ├── create_drive.html     ✅
    │   ├── edit_drive.html       ✅
    │   └── applications.html     ✅
    └── student/
        ├── dashboard.html        ✅
        ├── profile.html          ✅
        ├── drive_detail.html     ✅
        └── history.html          ✅
```

---

## How To Run Complete Project

```bash
# Step 1 - Install
pip install flask flask-sqlalchemy

# Step 2 - Initialize database
python init_db.py

# Step 3 - Run
python app.py

# Step 4 - Open browser
http://127.0.0.1:5000

# Admin credentials
Username: admin
Password: admin123
```

---

## All Core Features Covered ✅

```
✅ Login/Logout for all 3 roles
✅ Registration for Company and Student
✅ Admin pre-exists in DB
✅ Admin dashboard with counts
✅ Admin approve/reject companies
✅ Admin approve/reject drives
✅ Admin blacklist company (closes all drives)
✅ Admin blacklist/delete students
✅ Admin search students and companies
✅ Company login only after approval
✅ Company create/edit/delete/close drives
✅ Company view applications
✅ Company update application status
✅ Student register and login
✅ Student view only approved drives
✅ Student apply for drives
✅ Prevent duplicate applications
✅ Student view application status
✅ Student view history with summary
✅ Student edit profile and upload resume
✅ Role based access control
✅ Flash messages for all actions
✅ Bootstrap responsive UI
```