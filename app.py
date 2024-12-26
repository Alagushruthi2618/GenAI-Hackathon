from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',  # Update with your MySQL username
    'password': '',  # Update with your MySQL password
    'database': 'embrace_db'
}

# Configure upload folder with absolute path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
logger.debug(f"Upload folder path: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        logger.debug("Database connection successful")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                class INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                profile_image VARCHAR(255),
                full_image VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        logger.debug("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

# Initialize the database when the app starts
with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index242.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        logger.debug(f"Login attempt for user: {username}")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            logger.debug(f"Registration form data: {request.form}")
            logger.debug(f"Files in request: {request.files}")
            
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['fName']
            last_name = request.form['lName']
            age = request.form['Age']
            class_level = request.form['class']
            gender = request.form['Gender']
            email = request.form['email']
            
            # Handle profile image upload
            profile_image = request.files['profileImage']
            full_image = request.files.get('fullImage')
            
            profile_filename = None
            full_filename = None
            
            if profile_image and allowed_file(profile_image.filename):
                profile_filename = secure_filename(f"profile_{username}_{profile_image.filename}")
                profile_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_filename)
                logger.debug(f"Saving profile image to: {profile_path}")
                profile_image.save(profile_path)
                
            if full_image and allowed_file(full_image.filename):
                full_filename = secure_filename(f"full_{username}_{full_image.filename}")
                full_path = os.path.join(app.config['UPLOAD_FOLDER'], full_filename)
                logger.debug(f"Saving full image to: {full_path}")
                full_image.save(full_path)
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Save to database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            insert_query = '''
                INSERT INTO users 
                (username, password, first_name, last_name, age, class, gender, email, profile_image, full_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = (username, hashed_password, first_name, last_name, age, class_level, 
                     gender, email, profile_filename, full_filename)
            
            logger.debug(f"Executing insert query with values: {values}")
            
            cursor.execute(insert_query, values)
            conn.commit()
            
            logger.debug("Database insert successful")
            
            cursor.close()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('index'))
            
        except mysql.connector.IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            flash('Username or email already exists!', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Registration failed with error: {str(e)}")
            flash('Registration failed! Please try again.', 'error')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
