# FastAPI Application - User Authentication & CRUD Operations

This project implements a FastAPI-based application that allows user registration, login, and logout functionality. It also supports JWT token-based authentication, MongoDB integration, and Redis for temporary token storage. This README will guide you through the setup and usage of the application.

---

## Project Overview

This project is a simple user authentication service built with FastAPI. It includes the following functionalities:

- **User Registration**: Users can register by providing their details.
- **Login**: Users can authenticate themselves using JWT tokens.
- **Logout**: Users can log out by invalidating their tokens, ensuring they can no longer access protected routes.

The application is designed with modularity in mind, and it includes services for handling user-related business logic, such as login, logout, and user creation. MongoDB is used as the database, and Redis stores JWT tokens temporarily for session management.


## API Routes

| **Route**            | **Method** | **Description**                                             |
|----------------------|------------|-------------------------------------------------------------|
| `/register`          | POST       | Registers a new user.                                       | 
| `/login`             | POST       | Logs in an existing user and returns a JWT token.           | | `/logout`           | POST      | Logs out the authenticated user by invalidating their token.|



## Installation

To install the application and its dependencies, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Arpreetkhare/User_authentication_system.git
   cd TASK-ARPREET-KHARE

2. **Set up a virtual environment:**
     ```bash
     python3 -m venv env
     source env/bin/activate
   
4. **Install dependencies:**
     ```bash
     pip install -r requirements.txt

5. **Run the application:**
      ```bash
      uvicorn main:app --reload
6. **Access the app:** 
   http://127.0.0.1:8000

## Author 
  Arpreet Khare
 
