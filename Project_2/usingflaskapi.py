from flask import Flask, jsonify, request
from PIL import Image
import pytesseract
import re
import cv2
import numpy as np
import io

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def enhance_image(image_data):
    # Convert image data to OpenCV format
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(thresh)
    enhanced_buffer = io.BytesIO()
    cv2.imwrite(enhanced_buffer, enhanced_image)

    return enhanced_buffer.getvalue()

def extract_data_from_image(image_data):
    enhanced_data = enhance_image(image_data)
    enhanced_image = Image.open(io.BytesIO(enhanced_data))

    text = pytesseract.image_to_string(enhanced_image)
    print("Extracted Text:", text)

    application_number = extract_value(text, r"Application\s*Number:\s*(\S+)")
    statement_number = extract_value(text, r"Statement\s*Number:\s*(\S+)")
    village_name = extract_village_name(text)
    survey_number = extract_survey_numbers(text)

    return {
        "application_number": application_number,
        "statement_number": statement_number,
        "Village_name": village_name,
        "survey_number": survey_number
    }

def extract_survey_numbers(text):
    survey_lines = re.findall(r"Survey\s*Number:\s*(.+)", text, re.IGNORECASE)

    survey_numbers = []
    for line in survey_lines:
        numbers = re.findall(r"([\w/]+)", line)
        survey_numbers.extend(numbers)

    return [survey.strip() for survey in survey_numbers if survey.lower() not in ['survey', 'number']]

def extract_village_name(text):
    village_match = re.search(r"Village[^\w\n]*(\w[^\n]*)", text, re.IGNORECASE)
    return village_match.group(1).strip() if village_match else None

def extract_value(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

@app.route('/api/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image_data = uploaded_file.read()
    extracted_data = extract_data_from_image(image_data)

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(port=9999, debug=True)
