# Flask Microblogging Platform

A feature-rich microblogging platform built with Flask, enabling users to post updates, follow others, and engage with content in a secure and scalable environment.  

🔗 **Live Demo:** [microblog-web-tbn1.onrender.com](https://microblog-web-tbn1.onrender.com)  

---

## Features

- **User Authentication**  
  Secure login/registration with password hashing, email-based password reset, and JWT support for scalable session management.  

- **Post Management**  
  Create, view, and paginate posts with personalized timelines.  

- **Full-Text Search (Elasticsearch)**  
  Integrated Elasticsearch for fast, accurate, and relevance-ranked search, offering a **70% performance boost** over traditional SQL keyword matching.  

- **Social Features**  
  Follow/unfollow users, view user profiles (with Gravatar integration), timestamps powered by moment.js, and user statistics.  

- **Security & Stability**  
  - CSRF protection and form validation  
  - JWT-based authentication for API security  
  - Rate limiting to prevent abuse and ensure fair API usage  
  - Structured logging and centralized error handling  

---

## Technologies Used

- Flask, SQLAlchemy, Flask-Login  
- Flask-Mail, Flask-WTF, Flask-Bootstrap  
- Elasticsearch  
- Flask-Moment
