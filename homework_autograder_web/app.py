import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

standard_answers = {
    "4-1": "to help",
    "4-2": "buying",
    "4-3": "to ask",
    "4-4": "being",
    "4-5": "showing",
    "4-6": "talking",
    "5-1": "to show",
    "5-2": "to indicate",
    "5-3": "going",
    "5-4": "to spend",
    "5-5": "to see",
    "5-6": "rising"
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, 300)
    full_text = ""
    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"
    return full_text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.lower().endswith('.pdf'):
                ocr_text = extract_text_from_pdf(filepath)
            else:
                ocr_text = extract_text_from_image(filepath)

            student_text = ocr_text.lower()

            results = []
            for key, correct_answer in standard_answers.items():
                if correct_answer.lower() in student_text:
                    results.append((key, correct_answer, correct_answer, '✔'))
                else:
                    results.append((key, '未知', correct_answer, '✘'))

            return render_template('result.html', results=results)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
