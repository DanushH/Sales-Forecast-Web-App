<h1 align="center">Sales Forecast Web App</h1>

## Overview

This web application allows users to input data and receive sales predictions based on selected criteria, such as date, country, store, and product. It is built with Flask, a Python web framework, and utilizes MySQL for database management. Users can sign up, log in, and view predictions generated through a simple user interface.

> Note: This project is still in progress and subject to changes or improvements.

## Features

- **User Authentication**: Sign up and log in to user account securely.
- **Sales Prediction**: Input data and receive a sales prediction.
- **View Predictions**: View past predictions made by the user, displayed on a separate page.
- **Flash Notifications**: Receive feedback on actions such as successful sign-ups, logins, and errors.

## Tech Stack

- **Backend**: Flask, Python
- **Database**: MySQL
- **User Authentication**: Flask-Session for session management and Flask-Bcrypt for password hashing
- **Debugging**: Logging for debugging and error tracking

## Installation

### Prerequisites

- Python 3.x
- MySQL Server running locally or remotely

### Steps to Run the Project Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/DanushH/Sales-Forecast-Web-App.git 
   cd sales-forecast-web-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Create a MySQL database and execute the required schema.
   - Update the `config.py` file with your MySQL database credentials.

4. Run the Flask app:
   ```bash
   set FLASK_APP=app.app
   flask run
   ```

5. Open your browser and go to `http://127.0.0.1:5000/` to see the app in action.

## Configuration

You can configure various aspects of the app, including database credentials and session settings, in the `config.py` file. 

## Contributions

Feel free to fork this repository, make changes, and submit pull requests. Any improvements or fixes are always welcome!

## Contact

[![LinkedIn][linkedin-shield]][linkedin-url]

## License

This project is licensed under the MIT License.



<br>

<!-- MARKDOWN LINKS & IMAGES -->

[linkedin-shield]: https://img.shields.io/badge/Linkedin-black?style=for-the-badge&logo=linkedin&logoColor=%230277BD
[linkedin-url]: https://linkedin.com/in/danushika-herath
