# Contact List API (Flask)

This project is part of the **backend learning portfolio with Flask**.

A RESTful API built with **Flask** to manage a list of personal contacts. It allows authenticated users to create, view, update, and delete contacts associated with their account. The project is designed to be scalable and secure.

---

## 📁 Documentation

https://documenter.getpostman.com/view/36791092/2sB2j1gXiV

---

## 📁 Project Structure

```
contacts_list_flask/          # Main project
├── contacts_list/            # Main project configuration
│   ├── __init__.py           # Flask application initialization
│   ├── api/                  # API logic
│   │   ├── __init__.py       # API initialization
│   │   ├── models.py         # Contact model
│   │   ├── views.py          # API views
│   │   └── migrations/       # Database migrations
│   ├── config.py             # Main configurations (database, JWT, etc.)
│   ├── db.py                 # Database initialization
│   └── requirements.txt      # Project dependencies
├── migrations/               # Migration files
├── venv/                     # Virtual environment
├── README.md                 # Project documentation
└── function.txt              # Additional function or script files
└── app.py                    # Script to server the project
```

---

## 🔐 Features

- **User Authentication** with **JWT** (`/api/token/`)
- Full **CRUD** for managing personal contacts
- Access restriction: each user can only view their own contacts
- **Serialization** with custom validations
- Clear RESTful routes for managing contacts
- Using **Flask-SQLAlchemy** for database management
- **Flask-Migrate** to handle database migrations

---

## ⚙️ Technologies

- **Python 3.x**
- **Flask 3.1.0**
- **Flask-SQLAlchemy 3.1.1**
- **Flask-Migrate 4.1.0**
- **psycopg2-binary 2.9.10** (for PostgreSQL)
- **PyJWT 2.10.1** (for JWT authentication)
- **python-dotenv 1.1.0** (for environment variables)

---

## 🚀 How to Use This Project

1. **Clone the repository**:

   ```bash
   git clone git@github.com:LSCasas/contacts_list_flask.git
   cd contacts_list_flask
   ```

2. **Create a virtual environment and install dependencies**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Apply migrations and create a superuser** (if necessary):

   ```bash
   flask db upgrade
   ```

4. **Run the server**:

   ```bash
   flask run
   ```

5. **Use Postman or curl to authenticate and access the endpoints**:

   - `POST /api/token/` to obtain an authentication token
   - `GET /api/contacts/` to view your contacts
   - `POST /api/contacts/` to create a new contact

---

## 🧪 Authentication Example

1. Request the token:

   ```
   POST http://127.0.0.1:5000/api/token/
   Content-Type: application/json

   {
     "email": "test@example.com",
     "password": "test123"
   }
   ```

2. Use the token to access the API:

   ```
   GET http://127.0.0.1:5000/api/contacts/
   Authorization: Bearer <access_token>
   ```

---

## 📌 Requirements

- Python 3.8+
- pip
- Flask >= 3.1.0
- Flask-SQLAlchemy
- Flask-Migrate
- psycopg2
- PyJWT
- python-dotenv
