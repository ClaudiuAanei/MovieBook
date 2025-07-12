# MovieBook: Your Personal Movie Catalog
MovieBook is a Flask-based web application that allows users to discover, search, and save their favorite movies and TV series. The application interfaces with The Movie Database (TMDB) API to fetch up-to-date information on films, series, actors, and trailers.

## 🌟 Key Features
### For Users
* Secure Authentication: A complete user registration system with email confirmation and secure login.

* Content Discovery: Browse lists of currently popular movies and TV series.

* Advanced Search: Search for movies by title and get results sorted by popularity.

* Random Suggestions: Get a random movie recommendation, with options to filter by year and genre.

* Full Details: View detailed information for any title, including a synopsis, poster, rating, release date, cast, and the official trailer.

* Personal Watchlist: Save your favorite movies to a custom list on your profile.

* User Profile: A personal space to manage your saved movies and get new suggestions.

## For Administrators
* Admin Panel: An exclusive, protected dashboard for site management.

* User Management: View, edit, and delete registered users on the platform.

*  Updates: Manually trigger updates for the popular movies and series lists from the TMDB API.

* Maintenance: A tool to clean up the database by removing users who have not confirmed their accounts.

## 🛠️ Built With
* Backend: Python, Flask

* Database: SQLAlchemy (with SQLite)

* Authentication: Flask-Login, Werkzeug (for password hashing)

* Forms: Flask-WTF

* Frontend: HTML, CSS, Bootstrap 5

* API: The Movie Database (TMDB)

* Communications: Smtplib (for sending confirmation emails)

* Environment Variables: python-dotenv

## 🚀 Getting Started
Follow these steps to set up and run the project in your local environment.

1. Prerequisites
Python 3.8 or higher

2. Installation
Clone the repository:

   
# For Windows
    python -m venv venv
    .\venv\Scripts\activate

# For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
Install the dependencies:
(Ensure you have a requirements.txt file in your project root)

Bash

    pip install -r requirements.txt
    Configure environment variables:
    Create a file named .env in the project root and add the following variables.

Ini, TOML

# Secret key for the Flask application
    APP_CONFIG="your_super_secret_key_here"

# API Bearer Token from The Movie Database (TMDB)
    API_MB_TOKEN="Bearer your_tmdb_token_here"

# Gmail credentials for sending confirmation emails
    MY_EMAIL="your_email@gmail.com"
    PASSWORD="your_gmail_app_password"

# Base URL for the email confirmation link
    URL_CONFIRMARE="http://127.0.0.1:5000/confirm?code="
Important Note: For PASSWORD, you need to generate an "App Password" from your Google Account's security settings if you have 2-Step Verification enabled.

3. Running the Application
Start the app:
app.py

🕹️ How to Use
### As a User
Register: Create a new account. You will receive an email to confirm your account.

* Confirm your email: Click the link in the email to unlock all features.
* Log in: Access your account.
* Explore: Browse popular movies and series on the home page.
* Search: Use the search bar to find a specific movie.
* Save: Add movies to your personal list from their details page.
* Discover: Go to your profile and use the form to get a random movie that fits your tastes.

### As an Administrator
Access the login panel: Navigate to http://127.0.0.1:5000/adminlogin.

## Log in: Use the credentials defined in the code (admin.py):

### Username: admin
### Password: parola123

Manage: From the dashboard, you can view the user list, edit or delete users, and update the site's content.
