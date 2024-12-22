from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hackathon'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        f_name = request.form['fName']
        l_name = request.form['lName']
        age = request.form['Age']
        user_class = request.form['Class']
        gender = request.form['Gender']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Insert into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name, age, class, gender, email, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                       (f_name, l_name, age, user_class, gender, email, username, password))
        mysql.connection.commit()
        cursor.close()
        
        flash('Registration Successful! Please log in.', 'success')
        return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        cursor.close()
        
        if account:
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Username or Password!', 'danger')
            return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
