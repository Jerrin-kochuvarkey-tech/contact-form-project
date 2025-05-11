from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# PostgreSQL connection details from environment
DB_HOST = os.environ.get('DB_HOST', '13.127.98.84')
DB_NAME = os.environ.get('DB_NAME', 'project1_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', '1234')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

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
    app.run(host='0.0.0.0', port=80, debug=True)
