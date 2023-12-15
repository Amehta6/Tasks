from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import pytesseract
import re
import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Omshiv&123@localhost/EC-Telanagana'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ExtractedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sl_no = db.Column(db.String(255))

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
    sl_no = extract_value(text, r"Sl\.No\s*:\s*([\w/]+)")
    return {"Sl_No": sl_no}

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

            # Save extracted data to the database
            save_to_database(extracted_data)

            return render_template('result1.html', extracted_data=extracted_data)

    return render_template('index.html')

def save_to_database(extracted_data):
    new_data = ExtractedData(sl_no=extracted_data["Sl_No"])
    db.session.add(new_data)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    app.run(port=1234, debug=True)
