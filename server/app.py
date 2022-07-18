from flask import Flask, request, render_template, make_response
from database import Database
from datetime import datetime
import json

app = Flask(__name__)
db = Database()

main_url = 'https://zerojeden-web-server.azurewebsites.net'
all_parkings_url = main_url + '/api/parking/'
all_parking_spaces_url = main_url + '/api/parking-space/'

@app.route('/')
def main_page():
    db_data = db.get_all_parkings()
    total_free_spaces = db.get_number_of_all_free_spaces()[0]
    parkings = []
    for row in db_data:
        parking = {}
        for key, val in row.items():
            if key in 'City, Street, Number, ParkingId':
                parking[key] = f'{val}'
            if key == 'ParkingId':
                free_spaces_number = db.get_number_of_free_spaces_by_parking_id(val)[0]
                parking['Free spaces number'] = free_spaces_number
        parkings.append(parking)
    return render_template('index.html', parkings=parkings, total_free_spaces=total_free_spaces)

@app.route('/api/parking/', methods=['GET'])
def get_all_parkings():
    db_data = db.get_all_parkings()
    response_data = format_data(db_data)
    return make_response(response_data, 200)

@app.route('/api/parking/<id>', methods=['GET'])
def get_parking_by_id(id):
    db_data = db.get_parking_by_id(id)
    response_data = format_data(db_data)
    return make_response(response_data, 200)

@app.route('/api/parking-space/<parking_id>', methods=['GET'])
def get_parking_spaces_by_parking_id(parking_id):
    db_data = db.get_parking_spaces_by_parking_id(parking_id)
    response_data = format_data(db_data)
    return make_response(response_data, 200)

@app.route('/api/parking-space/', methods=['GET'])
def get_all_parking_spaces():
    db_data = db.get_all_parking_spaces()
    response_data = format_data(db_data)
    return make_response(response_data, 200)

@app.route('/api/parking-space/<parking_id>/<space_id>', methods=['GET', 'PUT'])
def get_parking_space_by_id(parking_id, space_id):
    if request.method == 'GET':
        db_data = db.get_parking_space_by_id(parking_id, space_id)
        response_data = format_data(db_data)
        return make_response(response_data, 200)

    elif request.method == 'PUT':
        data = request.get_json()
        is_taken = data['is_taken']
        is_taken = 1 if is_taken else 0
        return f'{db.update_parking_space_is_taken(parking_id, space_id, is_taken)}'

@app.route('/api/parking-space/free-spaces/<parking_id>', methods=['GET'])
def get_number_of_free_spaces_by_parking_id(parking_id):
    db_data = db.get_number_of_free_spaces_by_parking_id(parking_id)
    return make_response(json.dumps(db_data[0]), 200)

@app.route('/api/parking-space/free-spaces', methods=['GET'])
def get_number_of_all_free_spaces():
    db_data = db.get_number_of_all_free_spaces()
    return make_response(json.dumps(db_data[0]), 200)

def format_data(data):
    response_data = []
    for row in data:
        space = {}
        for key, value in row.items():
            if isinstance(value, datetime):
                space[key] = datetime.isoformat(value)
                continue
            space[key] = value
        response_data.append(space)
    return json.dumps(response_data)

if __name__ == '__main__':
    app.run(debug=True)
