from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from huggingface_hub import InferenceClient
import PIL.Image
import warnings

# Initialize Flask application
app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'embrace_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configure upload folders
UPLOAD_FOLDER = 'static/uploads'
COMIC_FOLDER = 'static/comics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMIC_FOLDER'] = COMIC_FOLDER

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# Initialize MySQL
mysql = MySQL(app)

# Configure API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# Initialize Hugging Face client
client = InferenceClient("black-forest-labs/FLUX.1-dev", token=HUGGINGFACE_TOKEN)

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMIC_FOLDER, exist_ok=True)

warnings.filterwarnings("ignore")

def save_file(file):
    """Helper function to save uploaded files"""
    if file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename, file_path
    return None, None

def get_user_details(user_id):
    """Fetch user details and intelligence type from database"""
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT u.gender, tr.intelligence_type 
        FROM users u 
        LEFT JOIN test_results tr ON u.id = tr.user_id 
        WHERE u.id = %s 
        ORDER BY tr.test_date DESC 
        LIMIT 1
    ''', (user_id,))
    result = cur.fetchone()
    cur.close()
    return result

@app.route('/')
def index():
    """Route for the main login/registration page"""
    if 'user_id' in session:
        return redirect(url_for('intelligence_test'))
    return render_template('index242.html')  # Your login page template

@app.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        try:
            # Get form data
            fname = request.form['fName']
            lname = request.form['lName']
            age = request.form['age']
            user_class = request.form['class']
            gender = request.form['gender']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            
            # Handle file uploads
            profile_image = request.files['profileImage']
            full_image = request.files['fullImage']
            
            # Save images and get filenames
            profile_image_filename, _ = save_file(profile_image)
            full_image_filename, _ = save_file(full_image) if full_image else (None, None)
            
            cur = mysql.connection.cursor()
            
            # Check if username already exists
            cur.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cur.fetchone()
            
            if user:
                flash('Username already exists!', 'danger')
                return redirect(url_for('index'))
            
            # Hash the password
            hashed_password = generate_password_hash(password)
            
            # Insert user data into database
            cur.execute('''
                INSERT INTO users 
                (first_name, last_name, age, class, gender, email, username, password, 
                profile_image, full_image) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (fname, lname, age, user_class, gender, email, username, 
                  hashed_password, profile_image_filename, full_image_filename))
            
            mysql.connection.commit()
            cur.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'An error occurred during registration: {str(e)}', 'danger')
            return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        
        if user:
            if check_password_hash(user['password'], password_candidate):
                # Set up user session
                session['user_id'] = user['id']
                session['username'] = user['username']
                
                flash('Successfully logged in!', 'success')
                return redirect(url_for('intelligence_test'))
            else:
                flash('Invalid password', 'danger')
                return redirect(url_for('index'))
        else:
            flash('Username not found', 'danger')
            return redirect(url_for('index'))
        
        cur.close()

@app.route('/intelligence_test')
def intelligence_test():
    """Route for the intelligence test page"""
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('index'))
    return render_template('indextest.html')  # Using your test page template

@app.route('/save_result', methods=['POST'])
def save_result():
    """Save the intelligence test results"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    intelligence_type = request.form.get('intelligence_type')
    quiz_score = request.form.get('quiz_score')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO test_results (user_id, intelligence_type, quiz_score)
            VALUES (%s, %s, %s)
        ''', (session['user_id'], intelligence_type, quiz_score))
        
        mysql.connection.commit()
        cur.close()
        
        flash('Test results saved successfully!', 'success')
        return redirect(url_for('view_results'))
    except Exception as e:
        flash(f'Error saving results: {str(e)}', 'danger')
        return redirect(url_for('intelligence_test'))

@app.route('/view_results')
def view_results():
    """View test results"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT tr.*, u.username 
        FROM test_results tr 
        JOIN users u ON tr.user_id = u.id 
        WHERE tr.user_id = %s 
        ORDER BY tr.test_date DESC
    ''', (session['user_id'],))
    
    results = cur.fetchall()
    cur.close()
    
    return render_template('results.html', results=results)

@app.route('/dashboard')
def dashboard():
    """Route for the subject selection dashboard"""
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('index'))
    return render_template('index25.html')

@app.route('/process_material', methods=['POST'])
def process_material_route():
    """Handle study material processing and comic generation"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401

    try:
        # Get file and subject
        if 'material' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['material']
        subject = request.form.get('subject')
        selected_date = request.form.get('date')
        selected_day = request.form.get('day')
        
        if not all([file, subject, selected_date, selected_day]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Save file
        filename, file_path = save_file(file)
        if not filename:
            return jsonify({'error': 'Error saving file'}), 500

        # Get user details
        user_details = get_user_details(session['user_id'])
        if not user_details:
            return jsonify({'error': 'User details not found'}), 404

        # Load and process document
        pdf_loader = PyPDFLoader(file_path)
        pages = pdf_loader.load_and_split()
        
        # Extract text content
        text_content = "\n".join(page.page_content for page in pages)
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        texts = text_splitter.split_text(text_content)
        
        # Initialize Gemini model
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.2,
            convert_system_message_to_human=True
        )
        
        # Create embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
        vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 5})
        
        # Create conversation template
        template = f"""Generate a conversation between a student and a Teacher discussing about the elements 
        from the study material, specifically tailored for a {user_details['gender']} student with 
        {user_details['intelligence_type']} intelligence. Ensure the dialogue is informative, engaging, 
        and uses examples that resonate with {user_details['intelligence_type']} learners.
        
        The conversation should contain 6 exchanges, with each exchange containing 1 line of dialogue.
        Make sure the characters are distinct in their personalities and the student asks questions respectfully.
        
        Here's the context: {{context}}
        """
        
        qa_chain_prompt = PromptTemplate.from_template(template)
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            model,
            retriever=vector_index,
            return_source_documents=True,
            chain_type_kwargs={"prompt": qa_chain_prompt}
        )
        
        # Generate conversation
        result = qa_chain({"query": f"Explain the main concepts in this {subject} material"})
        
        # Generate comic image using Hugging Face
        text_prompt = f"""
        Generate a comic like image having 4 sections with a theme learning {subject} with {user_details['intelligence_type']} intelligence. 
        Each section should include a {user_details['gender']} student, age 14, learning and engaging with different {subject} related objects. 
        Do not include any text or callouts in the sections.
        """
        
        comic_image = client.text_to_image(text_prompt)
        
        # Save comic image
        comic_filename = f"comic_{session['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        comic_path = os.path.join(app.config['COMIC_FOLDER'], comic_filename)
        comic_image.save(comic_path)
        
        # Save to database
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO study_materials 
            (user_id, subject, study_date, day, filename, conversation, comic_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (session['user_id'], subject, selected_date, selected_day, 
              filename, result['result'], comic_filename))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            'success': True,
            'conversation': result['result'],
            'comic_image': url_for('static', filename=f'comics/{comic_filename}')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view_material/<int:material_id>')
def view_material(material_id):
    """View generated study material"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT * FROM study_materials 
        WHERE id = %s AND user_id = %s
    ''', (material_id, session['user_id']))
    material = cur.fetchone()
    cur.close()

    if not material:
        flash('Material not found', 'error')
        return redirect(url_for('dashboard'))

    return render_template('view_material.html', material=material)

if __name__ == '__main__':
    app.run(debug=True)
