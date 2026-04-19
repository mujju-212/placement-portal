# Placement Portal Milestone Progress (Core)

This file tracks core milestone completion using the current implementation in the repository.

## Milestone: Database Models and Schema Setup

Status: Completed

Evidence from current codebase:
- Models defined for User (admin/company/student role), Company, Student, PlacementDrive, and Application.
- Relationships defined across user-company, user-student, company-drives, student-applications, and drive-applications.
- SQLite schema created programmatically using init_db.py and app startup create_all.
- Admin account bootstrapped via init_db.py (predefined admin as required).
