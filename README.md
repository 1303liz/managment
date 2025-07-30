# Django User Management System

This project is a Django-based user management system designed to provide secure authentication, user registration with email verification, profile management, and role-based permissions. It serves as a robust foundation for any web application that requires user accounts and access control.

## What This Project Does

- **Custom User Model:** Uses email as the login field and supports multiple user roles (Admin, Staff, User).
- **Email Verification:** Ensures users verify their email before activating their account.
- **Profile Management:** Allows users to update personal information and upload profile pictures.
- **Role-Based Permissions:** Restricts access to features based on user roles.
- **Admin Dashboard:** Enables administrators to manage users and their permissions.

## How This Project Can Help

- **Security:** Implements best practices for authentication, password management, and email verification.
- **Flexibility:** Easily extendable for additional user attributes or roles.
- **Productivity:** Provides ready-to-use user management features, saving development time for new Django projects.

## How It Works

1. **Registration:** Users sign up with their email and receive a verification link.
2. **Email Verification:** Clicking the link activates their account.
3. **Login:** Users log in using their email and password.
4. **Profile:** Authenticated users can view and edit their profile.
5. **Role Management:** Admins assign roles and manage user permissions via the admin interface.

## Getting Started

1. Clone the repository and install dependencies.
2. Set up environment variables for secret keys and email settings.
3. Run migrations and create a superuser.
4. Start the development server and access the app at `http://localhost:8000`.

## Project Structure

- `users/` – User and profile models, forms, views, and URLs.
- `templates/` – HTML templates for user interfaces.
- `user_management/` – Project settings and main URLs.

---

This project is licensed under the MIT License.
  - User management dashboard
  - Edit user details and permissions
  - Account activation/deactivation
  
- **Security Features**
  - CSRF protection
  - Password hashing
  - Session management
  - Password reset via email

## Project Development Journey

### 1.Setting Up the Django Project



We started by creating a new Django project and configuring the initial settings:

```bash
# Create Django project
django-admin startproject user_management

# Create users app
cd user_management
python manage.py startapp users
```

### 2. Creating Custom User Model

We extended Django's AbstractUser to create a custom user model with email authentication:

```python
# users/models.py
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'Regular User'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    is_email_verified = models.BooleanField(default=False)
    
    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
```

### 3. Implementing User Profile System


We created a Profile model linked to our CustomUser model:

```python
# users/models.py
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(max_length=200, blank=True)
```

## Setting Up the Project

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Basic knowledge of Django and virtual environments

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd user_management
```

### Step 2: Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```


### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:
- django>=4.2.0
- django-crispy-forms>=2.0
- crispy-bootstrap5>=0.7
- pillow>=10.0.0
- python-dotenv>=1.0.0

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```


### Step 6: Create Admin Superuser

```bash
python manage.py createsuperuser
```

## Core Components

### Custom User Model

Our system uses a custom user model that extends Django's AbstractUser:



Key features:
- Email as the username field
- User type field for role-based access
- Email verification flag

### Email Verification System

The registration process includes email verification:

1. User registers with email and password
2. System generates a unique token
3. Verification email is sent to the user
4. User clicks the verification link
5. Account is activated upon verification



### Profile Management

The profile system allows users to:
- Upload profile pictures
- Update personal information
- Manage security settings

## User Interface Walkthrough

### Home Page


The home page provides quick access to login and registration for non-authenticated users, and profile management for authenticated users.

### Registration Form


The registration form includes:
- Email field (used for login)
- Username
- First and last name
- Password with strength validation

### Profile Dashboard


The profile dashboard allows users to:
- View their current profile information
- Update personal details
- Change profile picture
- Manage account settings

### Admin Interface

The Django admin interface is customized to:
- Display user profiles
- Allow user management
- Control user permissions
- Monitor user activities

## Advanced Features

### Password Reset Functionality

The system includes a complete password reset workflow:
1. User requests password reset
2. System sends reset link via email
3. User creates new password
4. System confirms password change

## Running the Project


```bash
python manage.py runserver
```

### Accessing the Application

- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin


## Testing

Run the test suite to ensure everything is working properly:

```bash
python manage.py test
```

The test suite includes:
- User model tests
- Authentication tests
- Form validation tests
- View functionality tests



## Project Structure

```
user_management/
├── manage.py                # Django command-line utility
├── requirements.txt         # Project dependencies
├── media/                   # User uploaded files
├── static/                  # Static assets
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   └── users/              # User-related templates
├── users/                   # User management app
│   ├── models.py           # User and profile models
│   ├── views.py            # View logic
│   ├── forms.py            # User forms
│   ├── urls.py             # URL routing
│   └── tests.py            # Unit tests
└── user_management/         # Project settings
    ├── settings.py         # Configuration
    ├── urls.py             # Main URL routing
    └── wsgi.py             # WSGI configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


