id = 2

config = {
    1: {
        'trigger_pin': 19,
        'echo_pin': 18,
        'led_pin': 23
    }
}

wifi = {'login': 'Redmi 6', 'password': '12345678'}

CONSTANTS = {
    'distance_if_place_is_taken': 5,
}

MAIN_URL = 'https://zerojeden-web-server.azurewebsites.net'
UPDATE_PARKING_PLACE_STATUS_URL = MAIN_URL + '/api/parking-space/{parking_id}/{space_id}'
