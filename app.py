from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hackathon'

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize MySQL
mysql = MySQL(app)

# Secret key for flash messages
app.secret_key = 'your_secret_key'

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
        user_class = request.form['class']
        gender = request.form['Gender']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Handle profile image upload
        profile_image = request.files['profileImage']
        if profile_image:
            profile_image_filename = secure_filename(profile_image.filename)
            profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_image_filename)
            profile_image.save(profile_image_path)
        else:
            flash('Profile image is required.', 'danger')
            return redirect(url_for('home'))

        # Handle full-length image upload (optional)
        full_image = request.files.get('fullImage')
        if full_image and full_image.filename != '':
            full_image_filename = secure_filename(full_image.filename)
            full_image_path = os.path.join(app.config['UPLOAD_FOLDER'], full_image_filename)
            full_image.save(full_image_path)
        else:
            full_image_path = None

        # Insert data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, age, class, gender, email, username, password, profile_image, full_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (f_name, l_name, age, user_class, gender, email, username, password, profile_image_path, full_image_path))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('home'))

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
