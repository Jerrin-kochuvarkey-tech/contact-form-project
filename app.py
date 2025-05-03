from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session-based flash messages

# PostgreSQL connection details
DB_HOST = '192.168.1.5'  # Your host IP
DB_NAME = 'project1_db'  # Your database name
DB_USER = 'postgres'     # Your database username
DB_PASS = '1234'         # Your database password

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
