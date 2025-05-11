import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session-based flash messages

# PostgreSQL connection details
DB_HOST = os.environ.get('DB_HOST', '13.127.98.84')  # Replace 'your-db-host-ip' with your actual DB host IP
DB_NAME = os.environ.get('DB_NAME', 'project1_db')
DB_USER = os.environ.get('DB_USER', 'project_user')  # Use the correct DB user
DB_PASS = os.environ.get('DB_PASS', 'your_password')  # Use the correct password

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Route to show your form
@app.route('/')
def index():
    return render_template('index.html')

# Route to receive form submission (POST)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                (name, email, password))
    conn.commit()
    cur.close()
    conn.close()

    flash('Registration Successful!', 'success')
    return redirect(url_for('index'))

# Route to display the data (GET)
@app.route('/display', methods=['GET'])
def display_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, email, password FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('display.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # ✅ Updated for Docker
