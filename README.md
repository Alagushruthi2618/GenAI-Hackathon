**"Inclusive and Participatory design oriented tool to sustain STEAM education".  Here is the overview**

•	The tool is hyper-personalised based on the learners Intelligence type (There are a total of 8 intelligence types - Howard Gardner's Theory of Multiple Intelligences)

•	Once the intelligence type is identified the learner has to upload their subject material (text book, handwritten notes, sample question paper, other relevant materials)

•	The LLM then proceeds to create a visual output in a storyline format with the learner embedded in the learning experience

•	The tool also creates assessments to ensure spaced repetition based on scoring patterns, forgetting curve, and aims to be scaled up (beyond 15 year olds at both ends of the spectrum) based on John Piaget's theory of cognitive development

•	Intends to develop a healthy and sustained curiosity for STEAM subjects among girls/women by integrating women with noteworthy contributions to society as role models in the narrative (Nobel prize, Lasker award etc.)


**Setup instructions (step-by-step)**

Step 1: Download the Files
Begin by downloading the HTML, CSS, and JavaScript files required for the website. Each file should be appropriately named and saved with its respective extension: .html for the HTML file, .css for the CSS file, and .js for the JavaScript file. Ensure the file names are descriptive and relevant to their purpose in the project.

Step 2: Gather the Required Assets
Download all image assets or additional resources used in the website. These files should also be saved in the same directory as the HTML, CSS, and JavaScript files to maintain a simple and efficient project structure.

Step 3: Organize the Files
Create a single folder to store all the components of the website. Place the HTML file, CSS file, JavaScript file, and image assets together in this folder. This organization ensures that all files are accessible from the same directory, allowing the website to function as intended.

Step 4: View the Website
To view the website, open the HTML file (e.g., index.html) in a web browser such as Google Chrome. This action will render the website, allowing you to verify its layout, functionality, and design.

Step 5: Review the Code
For further inspection or editing, open the project folder in a code editor like Visual Studio Code. This tool allows you to view and modify the HTML, CSS, and JavaScript code efficiently while maintaining proper syntax and structure.

#### Step 1: Create a Virtual Environment (Optional but Recommended)
A virtual environment helps to manage your project's dependencies separately from your system Python installation.

1. *Open Command Prompt (CMD) or PowerShell*:
   - Press Win + X and select "Command Prompt" or "Windows PowerShell".

2. *Navigate to your project directory*:
   Use the cd command to go to the folder where you want to set up your environment.
   bash
   cd path\to\your\project
   

3. *Create a virtual environment*:
   Run the following command to create a virtual environment called venv.
   bash
   python -m venv venv
   

#### Step 2: Activate the Virtual Environment

1. *Activate the virtual environment*:
   After creating the virtual environment, run this command to activate it:
   bash
   .\venv\Scripts\activate
   

   After activation, your prompt will change to show (venv) indicating the virtual environment is active.

#### Step 3: Install Required System Dependencies

You need to install system libraries like Tesseract, Poppler, and others.

1. *Download and Install Tesseract OCR*:
   - Go to the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract).
   - Download the Windows installer (e.g., tesseract-ocr-w32-setup-v5.0.0-alpha.20210811.exe).
   - Follow the installation instructions. Make sure to select the option to add Tesseract to your system's PATH during installation.

2. *Install Poppler for PDF processing*:
   - Download Poppler for Windows from [this link](https://github.com/oschwartz10612/poppler-windows/releases/).
   - Extract the files to a directory (e.g., C:\poppler).
   - Add the bin folder (e.g., C:\poppler\bin) to your system's PATH:
     - Right-click on "This PC" > "Properties" > "Advanced system settings" > "Environment Variables".
     - In "System variables", click "New" and add:
       - Variable name: POPPLER_PATH
       - Variable value: C:\poppler\bin

#### Step 4: Install Required Python Packages

1. **Create a requirements.txt file**:
   In your project directory, create a requirements.txt file with the following contents:

   
   google-generativeai
   langchain-google-genai
   chromadb
   pypdf
   urllib3
   pandas
   langchain
   pillow
   

2. *Install the dependencies*:
   With the virtual environment activated, run the following command to install all the required packages:
   bash
   pip install -r requirements.txt
   

#### Step 5: Set Up API Keys for Google Gemini and Hugging Face

To use Google’s Gemini API and Hugging Face models, you’ll need API keys.

##### Google Gemini API Key:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or use an existing one.
3. Enable the Gemini API in your project.
4. Create an API key under "API & Services" > "Credentials".
5. Save your API key securely.

##### Hugging Face API Key:
1. Go to the [Hugging Face website](https://huggingface.co/).
2. Log in or create an account.
3. Go to your account settings and generate an API key.
4. Save your API key securely.

##### Store the API Keys in Environment Variables:
To store the API keys securely, you can set them as environment variables.

1. *Open PowerShell* and run the following commands to set the environment variables temporarily for your session:

   powershell
   $env:GOOGLE_API_KEY="your_google_api_key"
   $env:HUGGINGFACE_API_KEY="your_huggingface_api_key"
   

   Alternatively, you can permanently add them to your environment variables:
   - Right-click on "This PC" > "Properties" > "Advanced system settings" > "Environment Variables".
   - Under "User variables", click "New" and add:
     - Variable name: GOOGLE_API_KEY
     - Variable value: your_google_api_key
   - Similarly, create another entry for the Hugging Face API key.

#### Step 6: Install PIL (Pillow) Library

To handle image processing, you need to install the Pillow library (PIL).

1. *Install Pillow* by running:
   bash
   pip install pillow
   

#### Step 7: Import Necessary Modules in Your Python Script

Now, you can import the necessary modules in your Python script:

python
import urllib
import warnings
from pathlib import Path as p
from pprint import pprint

import pandas as pd
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


#### Step 8: Load and Process PDF Using PyPDF

Use PyPDFLoader from LangChain to load and process PDF files. Here's an example of how to load and process PDF documents:

python
from langchain.document_loaders import PyPDFLoader

# Load PDF document
pdf_path = "path_to_your_pdf_file.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Process the documents further if needed (e.g., splitting text)
text_splitter = RecursiveCharacterTextSplitter()
splitted_docs = text_splitter.split_documents(documents)


#### Step 9: Set Up LangChain for Question Answering

Now that you've set up LangChain and loaded your documents, you can create a question-answering chain.

python
# Create a PromptTemplate for your use case
prompt = PromptTemplate(template="Given the following documents, answer the question: {question}", input_variables=["question"])

# Load a pre-trained model (e.g., using Hugging Face model or Google API)
qa_chain = load_qa_chain(prompt, retriever=Chroma.from_documents(splitted_docs))


#### Step 10: Run Your Application

Once everything is set up, you can run your Python script or Flask application with the following command:

bash
python your_script.py


Ensure that your virtual environment is activated when running the script.

### Step 1: Create a Virtual Environment (Optional but Recommended)
A virtual environment helps isolate project dependencies from your system Python installation.

#### For Windows:
1. Open the Command Prompt (cmd) or PowerShell.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment:
   bash
   python -m venv venv
   

#### For macOS/Linux:
1. Open a terminal.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment:
   bash
   python3 -m venv venv
   

### Step 2: Activate the Virtual Environment

#### For Windows:
1. Run the following command to activate the virtual environment:
   bash
   .\venv\Scripts\activate
   

#### For macOS/Linux:
1. Run the following command to activate the virtual environment:
   bash
   source venv/bin/activate
   

You should see (venv) at the beginning of your terminal prompt, indicating that the virtual environment is activated.

### Step 3: Create the requirements.txt File

1. In your project directory, create a requirements.txt file with the following contents:
   
   Flask
   Flask-SQLAlchemy
   werkzeug
   langchain
   langchain-community
   langchain-google-genai
   pypdf
   chromadb
   transformers
   pillow
   

### Step 4: Install the Dependencies

1. Ensure the virtual environment is activated.
2. Run the following command to install all the dependencies listed in the requirements.txt file:
   bash
   pip install -r requirements.txt
   

### Step 5: Verify the Installation

1. After the installation is complete, verify the installed packages by running:
   bash
   pip freeze
   

   This will list all installed packages and their versions, confirming that the dependencies have been installed successfully.

### Step 6: Run Your Application

1. Now that the dependencies are installed, you can run your application. For example, if you’re using Flask, you can start your Flask application with:
   bash
   flask run
   

   Make sure your virtual environment is activated before running the application.

**Dependencies list**
Flask
Flask-SQLAlchemy
werkzeug
langchain
langchain-community
langchain-google-genai
pypdf
chromadb
transformers
pillow
Install the dependencies using pip:


**Usage Examples**
![WhatsApp Image 2024-12-29 at 17 30 38_3e4a48c7](https://github.com/user-attachments/assets/cafac6b9-4037-4eee-87c5-f57581da6fe7)


**Screenshots or GIFs of the app in action**
was unable to paste during submition faced technical glitch

**Team member details**

•	Kralagushruthi@gmail.com

•	diyaetony@gmail.com

•	nikhitha0920@gmail.com

•	sajalsharma0803@gmail.com

•	venkatesh14518@gmail.com
