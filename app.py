import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session-based flash messages

# PostgreSQL connection details (use environment variables or defaults)
DB_HOST = os.environ.get('DB_HOST', '13.127.98.84')  # Replace with your actual DB host IP
DB_NAME = os.environ.get('DB_NAME', 'project1_db')
DB_USER = os.environ.get('DB_USER', 'postgres')  # Adjust with your DB username
DB_PASS = os.environ.get('DB_PASS', '1234')  # Adjust with your DB password

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Route to show the registration form (GET request)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission (POST request)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Insert form data into PostgreSQL
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                (name, email, password))
    conn.commit()
    cur.close()
    conn.close()

    flash('Registration Successful!', 'success')  # Flash a success message
    return redirect(url_for('index'))

# Route to display all registered users (GET request)
@app.route('/display', methods=['GET'])
def display_data():
    # Retrieve all users from the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, email, password FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('display.html', users=users)

if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 and port 80 (for Docker and external access)
    app.run(host='0.0.0.0', port=80, debug=True)
