# JobBoard

JobBoard is a web-based application built with Django that enables employers to post job listings and job seekers to browse and apply for opportunities. The platform provides role-based access, allowing administrators, employers, and applicants to interact within a structured job management system.

---

## Live Application

https://dijango-project.onrender.com/

---

## Overview

The application is designed to streamline the job posting and application process. Employers can create and manage job listings, applicants can explore and apply for jobs, and administrators can review and moderate job postings.

---

## Core Features

* User authentication and authorization (login, logout, registration)
* Role-based access (Admin, Employer, Job Seeker)
* Job listing and detailed job view
* Job application system
* Employer dashboard for managing job postings
* Admin approval and rejection of job listings
* User profile management
* Media file handling for uploads

---

## Technology Stack

### Backend

* Django (Python web framework)
* SQLite (default database, easily configurable)
* Django Templates for server-side rendering

### Frontend

* HTML5
* CSS3
* Django Template Engine

### Deployment

* Render (Cloud hosting platform)

---

## Project Structure

```bash id="s7p4ak"
jobboard/
├── jobboard/        # Main project configuration
├── jobs/            # Core application (models, views, templates)
├── templates/       # Global templates
├── media/           # Uploaded media files
├── staticfiles/     # Collected static files
└── manage.py
```

---

## Environment Configuration

```env id="0lq3v9"
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=dijango-project.onrender.com
```

---

## Local Development Setup

```bash id="c8txx1"
git clone https://github.com/hello-world123pratik/dijango_project.git
cd dijango_project

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Application Routes Overview

* `/` → Home page
* `/jobs/` → Job listings
* `/job/<id>/` → Job details
* `/job/<id>/apply/` → Apply for a job
* `/employer/jobs/` → Employer dashboard
* `/admin/jobs/` → Admin job approval panel
* `/accounts/` → Authentication routes
* `/profile/` → User profile

---

## Security Considerations

* Built-in Django authentication system
* CSRF protection enabled
* Role-based access control for sensitive routes
* Secure handling of user data and sessions

---

## Deployment

The application is deployed on Render. Static and media files are configured using Django settings, and environment variables are managed through the hosting platform.

---

## License

This project is open-source and available under the MIT License.

