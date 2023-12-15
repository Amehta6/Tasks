from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import re
import cv2
import numpy as np

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def enhance_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(thresh)

    enhanced_path = 'enhanced_image.png'
    cv2.imwrite(enhanced_path, enhanced_image)

    return enhanced_path

def extract_data_from_image(image_path):

    enhanced_path = enhance_image(image_path)
    enhanced_image = Image.open(enhanced_path)

    text = pytesseract.image_to_string(enhanced_image)
    print("Extracted Text:", text)

    application_number = extract_value(text, r"Application\s*Number:\s*(\S+)")
    statement_number = extract_value(text, r"Statement\s*Number:\s*(\S+)")
    village_name =   extract_village_name(text)
    survey_number =  extract_survey_numbers(text)

    return {
        "application_number": application_number,
        "statement_number": statement_number,
        "Village_name":village_name,
        "survey_number":survey_number
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
    
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
           
            image_path = 'uploaded_image.png'
            uploaded_file.save(image_path)
            extracted_data = extract_data_from_image(image_path)

            return render_template('result.html', extracted_data=extracted_data)

    return render_template('index.html')

# output

# Result
# Application Number: 842144
# Statement Number: 149939894
# Village Name: MATOOR, Survey Number: 244AA,248A3,1658/1,
# Survey Numbers: 244AA, 248A3, 1658/1
# Back to Upload

if __name__ == '__main__':
    app.run(port=7777,debug=True)
    
