from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Omshiv&123@localhost/States'


db = SQLAlchemy(app)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Taluka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)

class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)

db.create_all()

@app.route('/api/data', methods=['GET'])
def get_all_data():
    districts = District.query.all()
    talukas = Taluka.query.all()
    villages = Village.query.all()

    data = {
        'districts': [district.name for district in districts],
        'talukas': [taluka.name for taluka in talukas],
        'villages': [village.name for village in villages],
        'total_counts': {
            'districts': len(districts),
            'talukas': len(talukas),
            'villages': len(villages),
        }
    }

    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_new_entry():
    data = request.json

    district_name = data.get('district')
    taluka_name = data.get('taluka')
    village_name = data.get('village')

    if district_name:
        new_district = District(name=district_name)
        db.session.add(new_district)

    if taluka_name:
        new_taluka = Taluka(name=taluka_name)
        db.session.add(new_taluka)

    if village_name:
        new_village = Village(name=village_name)
        db.session.add(new_village)

    db.session.commit()

    return jsonify({'message': 'Entries added successfully'})

# DELETE API
@app.route('/api/data/<entity>/<int:entity_id>', methods=['DELETE'])
def delete_entry(entity, entity_id):
    entity_model = None
    if entity == 'district':
        entity_model = District
    elif entity == 'taluka':
        entity_model = Taluka
    elif entity == 'village':
        entity_model = Village

    if entity_model:
        entry = entity_model.query.get(entity_id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({'message': f'{entity.capitalize()} deleted successfully'})
        else:
            return jsonify({'error': f'{entity.capitalize()} not found'}), 404
    else:
        return jsonify({'error': 'Invalid entity type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
