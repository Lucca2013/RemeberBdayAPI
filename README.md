# RememberBdayAPI 🧠⚙️

**RememberBdayAPI** is a RESTful API developed to serve as the backend ecosystem for the [rememberBday](https://github.com/lucca2013/rememberBday) mobile app. It manages the data lifecycle, user authentication, and the event-checking logic required to trigger notifications.

---

## ✨ Features

* **JWT Authentication:** Secure access control using *JSON Web Tokens* to protect CRUD routes.
* **Birthday Management (CRUD):** Structured endpoints to Create, Read, Update, and Delete birthday records linked to each user.
* **Cloud Database:** Native integration with a PostgreSQL database hosted on the [Neon](https://neon.tech/) platform.
* **Notification Scheduler:** An intelligent routine that checks for birthdays scheduled within the next 3 days and interfaces with Firebase Cloud Messaging (FCM) to send push notifications to mobile devices.

---

## 🛠️ Technologies Used

* **[Python](https://www.python.org/)**: The project's primary programming language.
* **[Flask](https://flask.palletsprojects.com/)**: A web micro-framework used to build API routes and logic.
* **[PostgreSQL (Neon)](https://neon.tech/)**: A serverless relational database for secure data storage.
* **[PyJWT](https://pyjwt.readthedocs.io/)**: A library for generating and validating JWT authentication tokens.
* **[Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)**: A tool used to communicate with Firebase and automatically trigger push notifications.

---
