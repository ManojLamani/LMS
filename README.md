# Simple LMS

A minimal Learning Management System with just the essentials.

## Features

- User registration and login (Student/Instructor roles)
- Student dashboard to browse and enroll in courses
- Instructor dashboard to create and manage courses
- User profile page

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run migrations:
```
python manage.py migrate
```

3. Create superuser (optional):
```
python manage.py createsuperuser
```

4. Run server:
```
python manage.py runserver
```

5. Visit http://localhost:8000

## Usage

- Register as a student or instructor
- Instructors can create courses
- Students can browse and enroll in courses
- Update your profile anytime
