from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import fitz  # For PyMuPDF

app = Flask(__name__)
socketio = SocketIO(app)

def extract_text_from_pdf(pdf_path):
    """Extracts text from the specified PDF file."""
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text

def process_query(query, full_text):
    """Processes the user's query and returns relevant text from the PDF."""
    # Lowercase the query for case-insensitive searching
    query_lower = query.lower()
    
    # Check if the query exists in the full text
    if query_lower in full_text.lower():
        # Find the starting index
        start_index = full_text.lower().find(query_lower)
        
        # Extract a portion of text around the query (adjust length as needed)
        surrounding_text_length = 300  # Number of characters to show around the query
        start = max(0, start_index - surrounding_text_length)  # Avoid negative index
        end = min(len(full_text), start_index + len(query_lower) + surrounding_text_length)  # Avoid overflow
        
        return full_text[start:end]  # Return the relevant chunk of text
    
    return "I couldn't find that information in the document."

# Load the PDF content once when the app starts
pdf_path = "/Users/admini/Documents/dev/convorc/KenyaConstitution2010.pdf"
constitution_text = extract_text_from_pdf(pdf_path)
print(constitution_text[:1000])  # Print the first 1000 characters to verify extraction

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    user_query = data['data']  # Extract the user's message
    response = process_query(user_query, constitution_text)  # Process the query
    emit('response', {"data": response})  # Send the response back to the client

if __name__ == '__main__':
    socketio.run(app, debug=True)
