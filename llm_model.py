!sudo apt -y -qq install tesseract-ocr libtesseract-dev

!sudo apt-get -y -qq install poppler-utils libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

!pip install langchain

!pip install -U langchain-community # Install the langchain-community package

# Now, import PyPDFLoader
from langchain.document_loaders import PyPDFLoader

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



warnings.filterwarnings("ignore")
# restart python kernal if issues with langchain import.

!pip install -U langchain-community

!pip install -U langchain-google-genai # Install the langchain-google-genai package

from langchain_google_genai import ChatGoogleGenerativeAI

import os
from google.colab import userdata

# Attempt to get the API key from userdata
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')

# If not found in userdata, try environment variable
if GOOGLE_API_KEY is None:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# If still not found, raise an error or prompt the user for input
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found in userdata or environment variables. Please set it appropriately.")

# Now you can use the GOOGLE_API_KEY variable in your code
model = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key=GOOGLE_API_KEY,
                             temperature=0.2,convert_system_message_to_human=True)

"""### Extract text from the PDF"""

!pip install pypdf

pdf_loader = PyPDFLoader("/content/periodic-table.pdf")
pages = pdf_loader.load_and_split()
print(pages[1].page_content)

len(pages)

"""### RAG Pipeline: Embedding + Gemini (LLM)"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

!pip install chromadb

vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})

qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index,
    return_source_documents=True

)

# ... other imports ...

import os
from google.colab import userdata

# Attempt to get the API key from userdata
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')

# If not found in userdata, try environment variable
if GOOGLE_API_KEY is None:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# If still not found, raise an error or prompt the user for input
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found in userdata or environment variables. Please set it appropriately.")

# Use gemini-1.5-flash instead of the deprecated gemini-pro-vision
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY,
                             temperature=0.2,convert_system_message_to_human=True)


# ... (rest of your code, including re-initializing qa_chain) ...
qa_chain = RetrievalQA.from_chain_type(
    model, # using the updated 'model'
    retriever=vector_index,
    return_source_documents=True

)
# ...

# Import necessary libraries
from langchain.vectorstores import Chroma # Assuming Chroma is used for the vectorstore

# Placeholder functions for document management (you'll need to implement these)
def check_new_document_indexed(document_path="/content/periodic-table.pdf"):
  """Checks if a new document has been indexed.

  Args:
      document_path: Path to the document to check.

  Returns:
      True if the document is indexed, False otherwise.
  """
  # Placeholder implementation - replace with your logic to check index status
  # This could involve checking the vectorstore's metadata or comparing the document
  # contents with the indexed data.
  return False # Replace with your actual check

def index_new_document(document_path="/content/periodic-table.pdf"):
  """Indexes a new document.

  Args:
      document_path: Path to the document to index.
  """
  # Load and split the document
  pdf_loader = PyPDFLoader(document_path)
  pages = pdf_loader.load_and_split()

  # Add the document to the existing vectorstore
  global vector_index
  vector_index.add_documents(pages)

def clear_cache():
  """Clears any relevant cache."""
  # Placeholder implementation - replace with your logic to clear cache
  # This could involve deleting temporary files, resetting internal variables, etc.
  pass  # Replace with your cache-clearing logic

def upload_document(document_path="/content/periodic-table.pdf"):
  """Reconfigures and re-uploads the document.

  Args:
      document_path: Path to the document to upload.
  """
  # Placeholder implementation - replace with your logic to upload/reconfigure
  # This could involve calling an external API or updating your local setup.
  pass  # Replace with your upload logic


# ... rest of your code ...

# Check indexing status
if not check_new_document_indexed():
  index_new_document()

# Clear cache (if applicable)
clear_cache()

# Reconfigure and re-upload the document
upload_document()

# Example quetablery
question = "Explain about all the 1-5 elements of periodic "
result = qa_chain({"query": question})
print(result["result"])

# ...

question = "Explain about 1-5 elements of periodic table"
result = qa_chain({"query": question})
print(result["result"])

import os
from google.colab import userdata

# Attempt to get the API key from userdata
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')

# If not found in userdata, try environment variable
if GOOGLE_API_KEY is None:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# If still not found, raise an error or prompt the user for input
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found in userdata or environment variables. Please set it appropriately.")

# Now you can use the GOOGLE_API_KEY variable in your code
# Use gemini-1.5-flash instead of the deprecated gemini-pro-vision
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY,
                             temperature=0.2,convert_system_message_to_human=True)

# Import necessary libraries
from IPython.display import Markdown
# ... other code ...
# Then you can use the Markdown function
Markdown(result["result"])

Markdown(result["result"])

# Assuming a function clear_cache exists
clear_cache()

result["source_documents"]

template = """Generate a conversation between a student and a Teacher named Teacher discussing about the elements with atomic number 6-10 of the periodic table, conversing the topic of [insert specific topic from RAG output here]The specific topic here include elemet's atomic number,atomic weight and it's state.Also include element's respective atomic number,atomic weight. Ensure that the dialogue is informative, engaging, and free of gender bias.Make sure the characters are distinct in their personalities.Make sure student asks questions respectfuly. Highly prioritise that boy can understand only when discussed in naturalistic way.
Student: A 9th grade boy named Sajal willing to learn chemistry with Naturalistic intelligence who has the ability to recognize, identify, understand, and work with elements of the natural world. she has a keen sense of observation and excel at spotting relationships and patterns in nature.
Teacher : A teacher , renowned for their groundbreaking research, has a passion for sharing knowledge with students. Known for their friendly demeanor and clear communication, they excel at breaking down complex concepts into simple, relatable terms using analogies and practical examples. Their interactive teaching style involves hands-on experiments and engaging demonstrations. Always patient and empathetic, they listen to students' questions and provide thoughtful explanations, making learning accessible and exciting for everyone.
The conversation should contain only 6 exchanges, with each exchange containing exactly 1 line of dialogue. dialogue should be short and have to be understandable by boy with naturalist intelligence. Use the dialogue to highlight key points from the retrieved text in an engaging and respectful manner.Make sure it is being taught to a boy with naturalist intelligence.Diaglogues must be able to understand by a boy with naturalist intelligence.

Here's some information to help you: {context}
""" # Added {context} here
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index,
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# Import necessary libraries
from langchain.vectorstores import Chroma # Assuming Chroma is used for the vectorstore

# Placeholder functions for document management (you'll need to implement these)
def check_new_document_indexed(document_path="/content/periodic-table.pdf"):
  """Checks if a new document has been indexed.

  Args:
      document_path: Path to the document to check.

  Returns:
      True if the document is indexed, False otherwise.
  """
  # Placeholder implementation - replace with your logic to check index status
  # This could involve checking the vectorstore's metadata or comparing the document
  # contents with the indexed data.
  return False # Replace with your actual check

def index_new_document(document_path="/content/periodic-table.pdf"):
  """Indexes a new document.

  Args:
      document_path: Path to the document to index.
  """
  # Load and split the document
  pdf_loader = PyPDFLoader(document_path)
  pages = pdf_loader.load_and_split()

  # Add the document to the existing vectorstore
  global vector_index
  vector_index.add_documents(pages)

def clear_cache():
  """Clears any relevant cache."""
  # Placeholder implementation - replace with your logic to clear cache
  # This could involve deleting temporary files, resetting internal variables, etc.
  pass  # Replace with your cache-clearing logic

def upload_document(document_path="/content/periodic-table.pdf"):
  """Reconfigures and re-uploads the document.

  Args:
      document_path: Path to the document to upload.
  """
  # Placeholder implementation - replace with your logic to upload/reconfigure
  # This could involve calling an external API or updating your local setup.
  pass  # Replace with your upload logic


# ... rest of your code ...

# Check indexing status
if not check_new_document_indexed():
  index_new_document()

# Clear cache (if applicable)
clear_cache()

# Reconfigure and re-upload the document
upload_document()

question = "Discuss about 1-10 elements of periodic table provided to a girl with naturalistic intelligence"
result = qa_chain({"query": question})
result["result"]

Markdown(result["result"])

from huggingface_hub import InferenceClient
from PIL import Image

# Initialize the InferenceClient with your model and token
client = InferenceClient("black-forest-labs/FLUX.1-dev", token="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")

# Assuming result is a dictionary containing the text
result = {
    "result": result["result"]
}

# Define the text prompt for the comic panel
text_prompt = f"""
Generate a comic like image having 4 sections with a theme learning chemistry outdoor with naturalist intelligence. Each of the 4 sections should include the same person with the same outfit with the following description - 14 year old Indian female student, height 5 feet.  The person should be learning chemistry performing different actions and engaging with different chemistry lab related objects. Do not include any text or callouts in any section. Please avoid errors in the image
"""

# Generate the image based on the text prompt
image = client.text_to_image(text_prompt)

image.save("genimage5.png")

# Display the generated image
display(image)

from huggingface_hub import InferenceClient
from PIL import Image

# Initialize the InferenceClient with your model and token
client = InferenceClient("black-forest-labs/FLUX.1-dev", token="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")

# Assuming result is a dictionary containing the text
result = {
    "result": result["result"]
}

# Define the text prompt for the comic panel
text_prompt = f"""
Generate a comic like image having 4 sections with a theme learning chemistry outdoor with naturalist intelligence. Each of the 4 sections should include the same person with the same outfit with the following description - 14 year old Indian male student, height 5 feet.  The person should be learning chemistry performing different actions and engaging with different chemistry lab related objects. Never Do not include any text or callouts in any section. Please avoid errors in the image
"""

# Generate the image based on the text prompt
image = client.text_to_image(text_prompt)

image.save("genimage6.png")

# Display the generated image
display(image)

from huggingface_hub import InferenceClient
from PIL import Image

# Initialize the InferenceClient with your model and token
client = InferenceClient("black-forest-labs/FLUX.1-dev", token="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")

# Define the text prompt for the comic panel
text_prompt = """
Generate a comic like image having 4 sections with a theme learning chemistry outdoor with naturalist intelligence. Each of the 4 sections should include the same person with the same outfit with the following description - 14 year old Indian female student, height 5 feet. The person should be learning chemistry performing different actions and engaging with different chemistry lab related objects. Do not include any text or callouts in any section. Please avoid errors in the image.
"""

# Generate the image based on the text prompt
image = client.text_to_image(text_prompt)

# Display the generated image size
width, height = image.size
print(f"The size of the generated image is {width}x{height} pixels.")

# Save the generated image
image.save("genimage5.png")

# Display the generated image
image.show()

def convert_conversation_to_tuples(conversation):
    lines = conversation.split('\n')
    conversation_tuples = []
    for line in lines:
        if line.strip() and ':' in line:  # Check if the line contains ':'
            speaker, text = line.split(':', 1)
            conversation_tuples.append((speaker.strip(), text.strip()))
    return conversation_tuples

# Example usage:
conversation = result["result"]

# Store the output tuples in the exchanges variable
exchanges = convert_conversation_to_tuples(conversation)

# Print the exchanges variable to verify the output
for item in exchanges:
    print(item)

def convert_conversation_to_tuples(conversation):
    lines = conversation.split('\n')
    conversation_tuples = []
    for line in lines:
        if line.strip() and ':' in line:  # Check if the line contains ':'
            speaker, text = line.split(':', 1)
            speaker = speaker.replace('**', '').strip()  # Remove '**' and trim spaces
            text = text.replace('**', '').strip()  # Remove '**' and trim spaces
            conversation_tuples.append((speaker, text))
    return conversation_tuples

# Example usage:
conversation = result["result"]
# Store the output tuples in the exchanges variable
exchanges = convert_conversation_to_tuples(conversation)

# Print the exchanges variable to verify the output
for item in exchanges:
    print(item)

def convert_conversation_to_tuples(conversation):
    lines = conversation.split('\n')
    conversation_tuples = []
    for line in lines:
        if line.strip() and ':' in line:  # Check if the line contains ':'
            speaker, text = line.split(':', 1)
            # Extract the character name without the leading number and period
            character_name = speaker.split(". ", 1)[-1].strip() if ". " in speaker else speaker.strip()
            character_name = character_name.replace('**', '').strip()  # Remove '**' and trim spaces
            text = text.replace('**', '').strip()  # Remove '**' and trim spaces
            conversation_tuples.append((character_name, text))  # Use character_name here
    return conversation_tuples

def convert_conversation_to_tuples(conversation):
    lines = conversation.split('\n')
    conversation_tuples = []
    for line in lines:
        if line.strip() and ':' in line:  # Check if the line contains ':'
            speaker, text = line.split(':', 1)
            # Extract the character name without the leading number and period
            character_name = speaker.split(". ", 1)[-1].strip() if ". " in speaker else speaker.strip()
            character_name = character_name.replace('**', '').strip()  # Remove '**' and trim spaces
            text = text.replace('**', '').strip()  # Remove '**' and trim spaces

            # Check if the character name is in the avatars dictionary
            if character_name in avatars:
                conversation_tuples.append((character_name, text))  # Use character_name here
    return conversation_tuples

def convert_conversation_to_tuples(conversation):
    lines = conversation.split('\n')
    conversation_tuples = []
    for line in lines:
        if line.strip() and ':' in line:  # Check if the line contains ':'
            speaker, text = line.split(':', 1)
            # Extract the character name without the leading number and period
            character_name = speaker.split(". ", 1)[-1].strip() if ". " in speaker else speaker.strip()
            character_name = character_name.replace('**', '').strip()  # Remove '**' and trim spaces
            text = text.replace('**', '').strip()  # Remove '**' and trim spaces

            # Check if the character name is in the avatars dictionary
            if character_name in avatars:
                conversation_tuples.append((character_name, text))  # Use character_name here
    return conversation_tuples

pip install transformers pillow

from PIL import Image, ImageDraw, ImageFont

# Sample dialogue exchanges
# Assuming 'result["result"]' contains the entire conversation text:
conversation_text = result["result"]
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Example font path on Linux

# Split the conversation into exchanges based on a pattern (e.g., newline)
exchanges = [line.split(": ", 1) for line in conversation_text.split("\n") if ": " in line]

# Create a function to draw each exchange
def draw_exchange(character, text, image_size=(1024,1024)):
    img = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    # Draw character name
    draw.text((10, 10), f"{character}:", fill=(0, 0, 0), font=font)

    # Draw text (speech bubble)
    draw.text((10, 50), text, fill=(0, 0, 0), font=font)

    return img

# Generate images for each exchange and save them
for i, (character, text) in enumerate(exchanges):
    img = draw_exchange(character, text)
    img.save(f"exchange_{i+1}.png")

print("Comic panels created successfully!")

# Define the avatars dictionary before calling convert_conversation_to_tuples
avatars = { # Define avatars dictionary before using it
    "Sajal": "/content/sajal.png",
    "Teacher": "/content/shruthi.png"  # Assuming "Professor" is the actual name used in your dialogue
}

# Now call the function
exchanges = convert_conversation_to_tuples(conversation)

from PIL import Image, ImageDraw

def make_image_circular(image_path, output_path, size=(100, 100)):
    # Open the image
    img = Image.open(image_path)

    # Resize image to the specified size
    img = img.resize(size, Image.Resampling.LANCZOS)

    # Create a circular mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img = img.convert("RGBA")

    # Apply the circular mask to the image
    img.putalpha(mask)

    # Save the image with transparency as a PNG
    img.save(output_path)

# Example usage:
avatars = {
    "Sajal": "/content/sajal.png",
    "Teacher": "/content/shruthi.png"
}

# Create circular images for both avatars
make_image_circular(avatars["Sajal"], "/content/sajal_circle.png")
make_image_circular(avatars["Teacher"], "/content/professor_circle.png")

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Sample dialogue exchanges (ensure this function returns the correct data)
exchanges = convert_conversation_to_tuples(conversation)
print("Exchanges:", exchanges)  # Debugging statement

# Character avatar paths (ensure all characters have corresponding avatars)
avatars = {
    "Nikhitha": "/content/nikhitha_circle.png",
    "Teacher": "/content/diya_circle.png"
}

# Define the path to the TTF font file
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Replace with the path to your TTF file

# Create a function to draw each exchange
def draw_exchange(character, text, image_size=(1800, 200), font_size=40):
    img = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load and resize character avatar (ensure it's in RGBA mode to preserve transparency)
    if character in avatars:
        avatar = Image.open(avatars[character]).convert("RGBA").resize((100, 100))
        # Create a mask from the avatar image and paste it with transparency
        img.paste(avatar, (10, 50), avatar)
    else:
        print(f"Avatar not found for character: {character}")  # Debugging statement

    # Load a font with the desired size
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        font = ImageFont.load_default()

    # Wrap text to fit within a specified width
    max_text_width = image_size[0] - 0  # Subtract space for avatar and margin
    wrapped_text = textwrap.fill(text, width=int(max_text_width / (font_size / 1.8)))

    # Calculate the height needed for the wrapped text
    lines = wrapped_text.split('\n')
    text_height = (font_size + 10) * len(lines)

    # Create a new image with adjusted height if needed
    if text_height + 70 > image_size[1]:
        img = Image.new('RGB', (image_size[0], text_height + 70), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        if character in avatars:
            img.paste(avatar, (10, 50), avatar)

    # Draw character name and text (speech bubble)
    draw.text((120, 10), f"{character}:", fill=(0, 0, 0), font=font)
    draw.text((120, 50), wrapped_text, fill=(0, 0, 0), font=font)

    return img

# Generate images for each exchange and combine them
panels = []
for character, text in exchanges:
    print(f"Drawing exchange for {character}")  # Debugging statement
    panel = draw_exchange(character, text)
    panels.append(panel)

# Calculate the total height for the final image
total_height = sum(panel.height for panel in panels)
max_width = max(panel.width for panel in panels)

# Create a new image with the appropriate size
combined_image = Image.new('RGB', (max_width, total_height))

# Paste each panel into the combined image
y_offset = 0
for panel in panels:
    combined_image.paste(panel, (0, y_offset))
    y_offset += panel.height

# Save the combined image
combined_image.save("comic_conversation.png")

print("Comic conversation created successfully!")

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Sample dialogue exchanges (ensure this function returns the correct data)
exchanges = convert_conversation_to_tuples(conversation)
print("Exchanges:", exchanges)  # Debugging statement

# Character avatar paths (ensure all characters have corresponding avatars)
avatars = {
    "Nikhitha": "/content/nikhitha_circle.png",
    "Teacher": "/content/professor_circle.png"
}

# Define the path to the TTF font file
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Replace with the path to your TTF file

# Path to the background image
background_image_path = "/content/bgreen.png"  # Replace with the path to your background image

# Create a function to draw each exchange
def draw_exchange(character, text, image_size=(1800, 200), font_size=40):
    # Load the background image and resize it to fit the panel size
    background = Image.open(background_image_path).convert("RGBA").resize(image_size)

    # Create a new image with RGBA mode to support transparency
    img = Image.new('RGBA', image_size, color=(255, 255, 255, 0))

    # Paste the background image onto the new image
    img.paste(background, (0, 0))

    draw = ImageDraw.Draw(img)

    # Load and resize character avatar (ensure it's in RGBA mode to preserve transparency)
    if character in avatars:
        avatar = Image.open(avatars[character]).convert("RGBA").resize((100, 100))
        # Create a mask from the avatar image and paste it with transparency
        img.paste(avatar, (10, 50), avatar)
    else:
        print(f"Avatar not found for character: {character}")  # Debugging statement

    # Load a font with the desired size
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        font = ImageFont.load_default()

    # Wrap text to fit within a specified width
    max_text_width = image_size[0] - 130  # Subtract space for avatar and margin
    wrapped_text = textwrap.fill(text, width=int(max_text_width / (font_size / 1.8)))

    # Calculate the height needed for the wrapped text
    lines = wrapped_text.split('\n')
    text_height = (font_size + 10) * len(lines)

    # Create a new image with adjusted height if needed
    if text_height + 70 > image_size[1]:
        img = Image.new('RGBA', (image_size[0], text_height + 70), color=(255, 255, 255, 0))
        img.paste(background.resize((image_size[0], text_height + 70)), (0, 0))
        draw = ImageDraw.Draw(img)
        if character in avatars:
            img.paste(avatar, (10, 50), avatar)

    # Draw character name and text (speech bubble)
    draw.text((120, 10), f"{character}:", fill=(0, 0, 0), font=font)
    draw.text((120, 50), wrapped_text, fill=(0, 0, 0), font=font)

    return img

# Generate images for each exchange and combine them
panels = []
for character, text in exchanges:
    print(f"Drawing exchange for {character}")  # Debugging statement
    panel = draw_exchange(character, text)
    panels.append(panel)

# Calculate the total height for the final image
total_height = sum(panel.height for panel in panels)
max_width = max(panel.width for panel in panels)

# Create a new image with the appropriate size
combined_image = Image.new('RGBA', (max_width, total_height))

# Paste each panel into the combined image
y_offset = 0
for panel in panels:
    combined_image.paste(panel, (0, y_offset))
    y_offset += panel.height

# Save the combined image
combined_image.save("comic_conversation.png")

print("Comic conversation created successfully!")

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Sample dialogue exchanges (ensure this function returns the correct data)
exchanges = convert_conversation_to_tuples(conversation)
print("Exchanges:", exchanges)  # Debugging statement

# Character avatar paths (ensure all characters have corresponding avatars)
avatars = {
    "Nikhitha": "/content/nikhitha_circle.png",
    "Professor": "/content/professor_circle.png"
}

# Define the path to the TTF font file
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Replace with the path to your TTF file

# Path to the background image
background_image_path = "/content/bgreen.png"  # Replace with the path to your background image

# Color dictionary for the character names
name_colors = {
    "Nikhitha": (0, 100, 0),  # Dark green for Nikhitha
    "Professor": (0, 100, 0)  # Blue for Professor
}

# Define offsets for the position of names
name_positions = {
    "Nikhitha": (20, 1),  # Adjust x, y position of Nikhitha's name
    "Professor": (20, 1)   # Adjust x, y position of Professor's name
}

# Create a function to draw each exchange
def draw_exchange(character, text, image_size=(1800, 200), font_size=40):
    # Load the background image and resize it to fit the panel size
    background = Image.open(background_image_path).convert("RGBA").resize(image_size)

    # Create a new image with RGBA mode to support transparency
    img = Image.new('RGBA', image_size, color=(255, 255, 255, 0))

    # Paste the background image onto the new image
    img.paste(background, (0, 0))

    draw = ImageDraw.Draw(img)

    # Load and resize character avatar (ensure it's in RGBA mode to preserve transparency)
    if character in avatars:
        avatar = Image.open(avatars[character]).convert("RGBA").resize((100, 100))
        # Create a mask from the avatar image and paste it with transparency
        img.paste(avatar, (10, 50), avatar)
    else:
        print(f"Avatar not found for character: {character}")  # Debugging statement

    # Load a font with the desired size
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        font = ImageFont.load_default()

    # Wrap text to fit within a specified width
    max_text_width = image_size[0] - 130  # Subtract space for avatar and margin
    wrapped_text = textwrap.fill(text, width=int(max_text_width / (font_size / 1.8)))

    # Calculate the height needed for the wrapped text
    lines = wrapped_text.split('\n')
    text_height = (font_size + 10) * len(lines)

    # Create a new image with adjusted height if needed
    if text_height + 70 > image_size[1]:
        img = Image.new('RGBA', (image_size[0], text_height + 70), color=(255, 255, 255, 0))
        img.paste(background.resize((image_size[0], text_height + 70)), (0, 0))
        draw = ImageDraw.Draw(img)
        if character in avatars:
            img.paste(avatar, (10, 50), avatar)

    # Draw character name with custom position
    name_color = name_colors.get(character, (0, 0, 0))  # Default to black if character not in dictionary
    name_position = name_positions.get(character, (120, 10))  # Get custom position for the name
    draw.text(name_position, f"{character}:", fill=name_color, font=font)

    # Draw character dialogue (speech bubble)
    draw.text((120, 50), wrapped_text, fill=(0, 0, 0), font=font)

    return img

# Generate images for each exchange and combine them
panels = []
for character, text in exchanges:
    print(f"Drawing exchange for {character}")  # Debugging statement
    panel = draw_exchange(character, text)
    panels.append(panel)

# Calculate the total height for the final image
total_height = sum(panel.height for panel in panels)
max_width = max(panel.width for panel in panels)

# Create a new image with the appropriate size
combined_image = Image.new('RGBA', (max_width, total_height))

# Paste each panel into the combined image
y_offset = 0
for panel in panels:
    combined_image.paste(panel, (0, y_offset))
    y_offset += panel.height

# Save the combined image
combined_image.save("comic_conversation.png")

print("Comic conversation created successfully!")

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Sample dialogue exchanges (ensure this function returns the correct data)
exchanges = convert_conversation_to_tuples(conversation)
print("Exchanges:", exchanges)  # Debugging statement

# Character avatar paths (ensure all characters have corresponding avatars)
avatars = {
    "Nikhitha": "/content/nikhitha_circle.png",
    "Teacher": "/content/professor_circle.png"
}

# Define the path to the TTF font files
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Regular font
bold_font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"  # Bold font

# Path to the background image
background_image_path = "/content/Backgroundgreen.png"  # Replace with the path to your background image

# Color dictionary for the character names
name_colors = {
    "Nikhitha": (0, 100, 0),  # Dark green for Nikhitha
    "Teacher": (0, 100, 0)  # Blue for Professor
}

# Define offsets for the position of names
name_positions = {
    "Nikhitha": (20, 0),  # Adjust x, y position of Nikhitha's name
    "Teacher": (20, 0)   # Adjust x, y position of Professor's name
}

# Define font sizes for the names of characters
name_font_sizes = {
    "Nikhitha": 45,  # Larger font size for Nikhitha's name
    "Teacher": 45,  # Larger font size for Professor's name
}

# Line spacing value (increase this to add more space between lines)
LINE_SPACING = 10  # Adjust this value to control the spacing

# Create a function to draw each exchange
def draw_exchange(character, text, image_size=(1800, 200), font_size=40):
    # Load the background image and resize it to fit the panel size
    background = Image.open(background_image_path).convert("RGBA").resize(image_size)

    # Create a new image with RGBA mode to support transparency
    img = Image.new('RGBA', image_size, color=(255, 255, 255, 0))

    # Paste the background image onto the new image
    img.paste(background, (0, 0))

    draw = ImageDraw.Draw(img)

    # Load and resize character avatar (ensure it's in RGBA mode to preserve transparency)
    if character in avatars:
        avatar = Image.open(avatars[character]).convert("RGBA").resize((100, 100))
        # Create a mask from the avatar image and paste it with transparency
        img.paste(avatar, (10, 50), avatar)
    else:
        print(f"Avatar not found for character: {character}")  # Debugging statement

    # Load a font for dialogue text
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        font = ImageFont.load_default()

    # Wrap text to fit within a specified width
    max_text_width = image_size[0] - 130  # Subtract space for avatar and margin
    wrapped_text = textwrap.fill(text, width=int(max_text_width / (font_size / 1.8)))

    # Calculate the height needed for the wrapped text with custom line spacing
    lines = wrapped_text.split('\n')
    text_height = (font_size + LINE_SPACING) * len(lines)  # Use custom line spacing here

    # Create a new image with adjusted height if needed
    if text_height + 70 > image_size[1]:
        img = Image.new('RGBA', (image_size[0], text_height + 70), color=(255, 255, 255, 0))
        img.paste(background.resize((image_size[0], text_height + 70)), (0, 0))
        draw = ImageDraw.Draw(img)
        if character in avatars:
            img.paste(avatar, (10, 50), avatar)

    # Set the font size for character names and load the bold font for specific characters
    name_font_size = name_font_sizes.get(character, 40)  # Default to 40 if character not in dictionary
    try:
        # Use bold font for Nikhitha and Professor
        if character in ["Nikhitha", "Teacher"]:
            name_font = ImageFont.truetype(bold_font_path, name_font_size)
        else:
            name_font = ImageFont.truetype(font_path, name_font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        name_font = ImageFont.load_default()

    # Draw character name with custom position and font size
    name_color = name_colors.get(character, (0, 0, 0))  # Default to black if character not in dictionary
    name_position = name_positions.get(character, (120, 10))  # Get custom position for the name
    draw.text(name_position, f"{character}:", fill=name_color, font=name_font)

    # Draw character dialogue (speech bubble) with adjusted line spacing
    current_y = 50  # Starting Y position for the dialogue text
    for line in lines:
        draw.text((120, current_y), line, fill=(0, 0, 0), font=font)
        current_y += font_size + LINE_SPACING  # Increase Y position based on line height and spacing

    return img

# Generate images for each exchange and combine them
panels = []
for character, text in exchanges:
    print(f"Drawing exchange for {character}")  # Debugging statement
    panel = draw_exchange(character, text)
    panels.append(panel)

# Calculate the total height for the final image
total_height = sum(panel.height for panel in panels)
max_width = max(panel.width for panel in panels)

# Create a new image with the appropriate size
combined_image = Image.new('RGBA', (max_width, total_height))

# Paste each panel into the combined image
y_offset = 0
for panel in panels:
    combined_image.paste(panel, (0, y_offset))
    y_offset += panel.height

# Save the combined image
combined_image.save("comic_conversation.png")

print("Comic conversation created successfully!")

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Sample dialogue exchanges (ensure this function returns the correct data)
exchanges = convert_conversation_to_tuples(conversation)
print("Exchanges:", exchanges)  # Debugging statement

# Character avatar paths (ensure all characters have corresponding avatars)
avatars = {
    "Sajal": "/content/sajal_circle.png",
    "Teacher": "/content/professor_circle.png"
}

# Define the path to the TTF font files
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Regular font
bold_font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"  # Bold font

# Path to the background image
background_image_path = "/content/Backgroundgreen.png"  # Replace with the path to your background image

# Color dictionary for the character names
name_colors = {
    "Sajal": (0, 100, 0),  # Dark green for Nikhitha
    "Teacher": (0, 100, 0)  # Blue for Professor
}

# Define offsets for the position of names
name_positions = {
    "Sajal": (20, 0),  # Adjust x, y position of Nikhitha's name
    "Teacher": (20, 0)   # Adjust x, y position of Professor's name
}

# Define font sizes for the names of characters
name_font_sizes = {
    "Sajal": 45,  # Larger font size for Nikhitha's name
    "Teacher": 45,  # Larger font size for Professor's name
}

# Line spacing value (increase this to add more space between lines)
LINE_SPACING = 10  # Adjust this value to control the spacing

# Create a function to draw each exchange
def draw_exchange(character, text, image_size=(1800, 200), font_size=40):
    # Load the background image and resize it to fit the panel size
    background = Image.open(background_image_path).convert("RGBA").resize(image_size)

    # Create a new image with RGBA mode to support transparency
    img = Image.new('RGBA', image_size, color=(255, 255, 255, 0))

    # Paste the background image onto the new image
    img.paste(background, (0, 0))

    draw = ImageDraw.Draw(img)

    # Load and resize character avatar (ensure it's in RGBA mode to preserve transparency)
    if character in avatars:
        avatar = Image.open(avatars[character]).convert("RGBA").resize((100, 100))
        # Create a mask from the avatar image and paste it with transparency
        img.paste(avatar, (10, 50), avatar)
    else:
        print(f"Avatar not found for character: {character}")  # Debugging statement

    # Load a font for dialogue text
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        font = ImageFont.load_default()

    # Wrap text to fit within a specified width
    max_text_width = image_size[0] - 130  # Subtract space for avatar and margin
    wrapped_text = textwrap.fill(text, width=int(max_text_width / (font_size / 1.8)))

    # Calculate the height needed for the wrapped text with custom line spacing
    lines = wrapped_text.split('\n')
    text_height = (font_size + LINE_SPACING) * len(lines)  # Use custom line spacing here

    # Create a new image with adjusted height if needed
    if text_height + 70 > image_size[1]:
        img = Image.new('RGBA', (image_size[0], text_height + 70), color=(255, 255, 255, 0))
        img.paste(background.resize((image_size[0], text_height + 70)), (0, 0))
        draw = ImageDraw.Draw(img)
        if character in avatars:
            img.paste(avatar, (10, 50), avatar)

    # Set the font size for character names and load the bold font for specific characters
    name_font_size = name_font_sizes.get(character, 40)  # Default to 40 if character not in dictionary
    try:
        # Use bold font for Nikhitha and Teacher
        if character in ["Sajal", "Teacher"]:
            name_font = ImageFont.truetype(bold_font_path, name_font_size)
        else:
            name_font = ImageFont.truetype(font_path, name_font_size)
    except IOError:
        print("Font file not found, using default font.")  # Debugging statement
        name_font = ImageFont.load_default()

    # Draw character name with custom position and font size
    name_color = name_colors.get(character, (0, 0, 0))  # Default to black if character not in dictionary
    name_position = name_positions.get(character, (120, 10))  # Get custom position for the name

    # Draw character name without the colon for Nikhitha and Teacher
    if character in ["Sajal", "Teacher"]:
        draw.text(name_position, f"{character}", fill=name_color, font=name_font)
    else:
        draw.text(name_position, f"{character}:", fill=name_color, font=name_font)

    # Draw character dialogue (speech bubble) with adjusted line spacing
    current_y = 50  # Starting Y position for the dialogue text
    for line in lines:
        draw.text((120, current_y), line, fill=(0, 0, 0), font=font)
        current_y += font_size + LINE_SPACING  # Increase Y position based on line height and spacing

    return img

# Generate images for each exchange and combine them
panels = []
for character, text in exchanges:
    print(f"Drawing exchange for {character}")  # Debugging statement
    panel = draw_exchange(character, text)
    panels.append(panel)

# Calculate the total height for the final image
total_height = sum(panel.height for panel in panels)
max_width = max(panel.width for panel in panels)

# Create a new image with the appropriate size
combined_image = Image.new('RGBA', (max_width, total_height))

# Paste each panel into the combined image
y_offset = 0
for panel in panels:
    combined_image.paste(panel, (0, y_offset))
    y_offset += panel.height

# Save the combined image
combined_image.save("comic_conversation.png")

print("Comic conversation created successfully!")

from PIL import Image

# Load the images
image1 = Image.open("/content/comic_conversation.png")
image2 = Image.open("/content/genimage5.png")

# Get the dimensions of the images
width1, height1 = image1.size
width2, height2 = image2.size

# Create a new image with a width equal to the sum of both image widths and a height equal to the max height
total_width = width1 + width2
max_height = max(height1, height2)

new_image = Image.new("RGB", (total_width, max_height), (255, 255, 255))

# Paste the two images onto the new image
new_image.paste(image1, (0, 0))
new_image.paste(image2, (width1, 0))

# Save the new image
new_image.save("/content/combinedimg.png")

print("Combined image created successfully!")

from PIL import Image

# Load the images
image1 = Image.open("/content/comic_conversation.png")
image2 = Image.open("/content/genimage6.png")

# Get the maximum height
max_height = max(image1.height, image2.height)

# Resize both images to have the same height
image1 = image1.resize((int(image1.width * max_height / image1.height), max_height))
image2 = image2.resize((int(image2.width * max_height / image2.height), max_height))

# Calculate the new width for each image to occupy half of the final image
half_width = (image1.width + image2.width) // 2
image1 = image1.resize((half_width, max_height))
image2 = image2.resize((half_width, max_height))

# Create a new image with a width equal to the sum of both image widths and a height equal to the max height
total_width = image1.width + image2.width

new_image = Image.new("RGB", (total_width, max_height), (255, 255, 255))

# Paste the two images onto the new image
new_image.paste(image1, (0, 0))
new_image.paste(image2, (image1.width, 0))

# Save the new image
new_image.save("/content/combinedimg.png")

print("Combined image created successfully!")

# Load the image
image = Image.open("/content/combinedimg.png")

# Desired dimensions
desired_width = 3530
desired_height = 1730

# Resize the image
resized_image = image.resize((desired_width, desired_height))

# Save the resized image to the current directory (or specify a valid path)
resized_image.save("resized_image.png") # Changed the save path

print("Image resized successfully!")
