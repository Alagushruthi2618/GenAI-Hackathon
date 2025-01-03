from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from huggingface_hub import InferenceClient
import warnings

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    profile_image = db.Column(db.String(120), nullable=False)
    intelligence_type = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    study_materials = db.relationship('StudyMaterial', backref='user', lazy=True)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    intelligence_type = db.Column(db.String(50), nullable=False)
    quiz_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    study_date = db.Column(db.Date, nullable=False)
    day_number = db.Column(db.String(20), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index242.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['username'] = username
            session['user_id'] = user.id
            flash('Successfully logged in!', 'success')
            return redirect(url_for('quiz'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('index'))
        
        # Handle profile image upload
        profile_image = request.files['profileImage']
        if profile_image and allowed_file(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Invalid image format!', 'danger')
            return redirect(url_for('index'))
        
        # Create new user
        new_user = User(
            username=username,
            password=generate_password_hash(request.form['password']),
            email=request.form['email'],
            first_name=request.form['fName'],
            last_name=request.form['lName'],
            profile_image=filename,
            intelligence_type=request.form['intelligence_type'],
            gender=request.form['gender']
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Registration failed! Please try again.', 'danger')
            
        return redirect(url_for('index'))

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('indextest.html')

@app.route('/save_result', methods=['POST'])
def save_result():
    if 'username' not in session or 'user_id' not in session:
        return redirect(url_for('index'))
    
    intelligence_type = request.form.get('intelligence_type')
    quiz_score = request.form.get('quiz_score')
    
    # Store quiz results
    new_result = QuizResult(
        user_id=session['user_id'],
        intelligence_type=intelligence_type,
        quiz_score=float(quiz_score)
    )
    
    try:
        db.session.add(new_result)
        db.session.commit()
        flash('Quiz results saved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to save quiz results!', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('index25.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/results')
def results():
    if 'username' not in session or 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Get the latest quiz result for the user
    latest_result = QuizResult.query.filter_by(user_id=session['user_id']).order_by(QuizResult.created_at.desc()).first()
    
    if latest_result:
        return render_template('results.html',
                            intelligence_type=latest_result.intelligence_type,
                            quiz_score=latest_result.quiz_score,
                            subject="General Knowledge")
    return redirect(url_for('quiz'))

@app.route('/upload_material', methods=['POST'])
def upload_material():
    if 'username' not in session or 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'})
    
    try:
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Read file data
            file_data = file.read()
            filename = secure_filename(file.filename)
            
            # Create new study material record
            new_material = StudyMaterial(
                user_id=session['user_id'],
                subject=request.form['subject'],
                study_date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
                day_number=request.form['day'],
                image_data=file_data,
                filename=filename
            )
            
            db.session.add(new_material)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Material uploaded successfully'})
        else:
            return jsonify({'success': False, 'message': 'Invalid file type'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/start_test', methods=['POST'])
def start_test():
    selected_day = request.form.get('day')
    if selected_day == 'Day 1':
        return redirect(url_for('chem_test_day1'))
    elif selected_day == 'Day 2':
        return redirect(url_for('chem_test_day2'))
    else:
        flash('Invalid day selected', 'danger')
        return redirect(url_for('chem_test_day1'))

@app.route('/chem_test_day1')
def chem_test_day1():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('indexchem.html')

@app.route('/chem_test_day2')
def chem_test_day2():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('indexchem2.html')

# app.py route modifications (add to existing app.py)
@app.route('/get_day_image/<day>')
def get_day_image(day):
    if day == '1':
        return send_from_directory('static', 'Day1_nikdiy.png')
    elif day == '2':
        return send_from_directory('static', 'Day2_Nikdiy.png')
    else:
        return 'Image not found', 404

@app.route('/generate_comic', methods=['POST'])
def generate_comic():
    if 'username' not in session or 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'})
    
    try:
        user = User.query.filter_by(id=session['user_id']).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})

        # LLM logic here
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found. Please set it appropriately.")

        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.2, convert_system_message_to_human=True)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

        pdf_loader = PyPDFLoader("/content/periodic-table.pdf")
        pages = pdf_loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        context = "\n\n".join(str(p.page_content) for p in pages)
        texts = text_splitter.split_text(context)
        vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 5})

        qa_chain = RetrievalQA.from_chain_type(
            model,
            retriever=vector_index,
            return_source_documents=True
        )

        question = "Discuss about 1-10 elements of periodic table provided to a girl with naturalistic intelligence"
        result = qa_chain({"query": question})

        conversation = result["result"]
        exchanges = convert_conversation_to_tuples(conversation)

        avatars = {
            "Sajal": "/content/sajal.png",
            "Teacher": "/content/professor.png"
        }

        # Create the comic panels
        panels = []
        for character, text in exchanges:
            panel = draw_exchange(character, text)
            panels.append(panel)

        # Combine the panels into one image
        total_height = sum(panel.height for panel in panels)
        max_width = max(panel.width for panel in panels)
        combined_image = Image.new('RGBA', (max_width, total_height))

        y_offset = 0
        for panel in panels:
            combined_image.paste(panel, (0, y_offset))
            y_offset += panel.height

        # Save the combined image
        combined_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "comic_conversation.png")
        combined_image.save(combined_image_path)

        # Return the combined image path
        return jsonify({'success': True, 'image_path': combined_image_path})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
