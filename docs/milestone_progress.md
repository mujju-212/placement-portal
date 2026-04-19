# Placement Portal Milestone Progress (Core)

This file tracks core milestone completion using the current implementation in the repository.

## Milestone: Database Models and Schema Setup

Status: Completed

Evidence from current codebase:
- Models defined for User (admin/company/student role), Company, Student, PlacementDrive, and Application.
- Relationships defined across user-company, user-student, company-drives, student-applications, and drive-applications.
- SQLite schema created programmatically using init_db.py and app startup create_all.
- Admin account bootstrapped via init_db.py (predefined admin as required).

## Milestone: Authentication and Role-Based Access

Status: Completed

Evidence from current codebase:
- Student and company registration available through register route and role-based form fields.
- Login route validates credentials and redirects to role-specific dashboards.
- Predefined admin login supported (no admin registration flow).
- Company login blocked until admin approval.
- Role-based access checks enforced before admin/company/student dashboard access.

## Milestone: Admin Dashboard and Management

Status: Completed

Evidence from current codebase:
- Admin dashboard shows totals for students, companies, drives, and applications.
- Admin can approve/reject company registrations.
- Admin can approve/reject drives and review applications.
- Admin can search students and companies.
- Admin can blacklist/unblacklist/delete students and companies.
