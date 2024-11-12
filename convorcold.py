import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text

# Specify the path to your PDF
pdf_path = "/Users/admini/Documents/dev/convorc/KenyaConstitution2010.pdf"

# Extract text from the PDF
constitution_text = extract_text_from_pdf(pdf_path)

# You can now use `constitution_text` for querying or any other processing
print(constitution_text[:1000])  # Print the first 1000 characters to verify extraction

