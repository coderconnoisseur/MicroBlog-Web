# Flask Microblogging Platform

A feature-rich microblogging platform built with Flask, allowing users to post updates, follow other users, and engage with content.

## Features

- **User Authentication**
  - Secure login and registration
  - Password reset via email
  - Remember me functionality
  - Profile customization

- **Post Management**
  - Create and view posts
  - Pagination support
  - Full-text search using Elasticsearch
  - User timeline with followed posts

- **Social Features**
  - Follow/unfollow users
  - User profiles with avatars (Gravatar integration)
  - Post timestamps with moment.js
  - User statistics

- **Security**
  - Password hashing
  - CSRF protection
  - Form validation
  - Secure password reset tokens

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Login
- Flask-Mail
- Flask-WTF
- Flask-Bootstrap
- Elasticsearch
- Flask-Moment

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/coderconnoisseur/MicroBlog-Web.git
cd <project-directory>

2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
 ```

3. Install dependencies
```bash
pip install -r requirements.txt
 ```
```
4. Set environment variables
```bash
set FLASK_APP=PY2.py
set FLASK_DEBUG=1
 ```
5. Initialize database
```bash
flask db upgrade
 ```
 6. Run the application
```bash
flask run
 ```