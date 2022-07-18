from config import id, config, CONSTANTS, UPDATE_PARKING_PLACE_STATUS_URL, wifi
from sensor import HCSR04
from time import sleep
from machine import Pin
import network
import ujson
import urequests


class Parking:
    def __init__(self, id, parking_places=None, wifi=None):
        self._id = id
        self._state = {}
        self.set_wifi(wifi)
        if parking_places is not None:
            self._parking_places = parking_places
            for pp in parking_places:
                self._state[pp.get_id()] = pp
    
    def set_wifi(self, wifi):
        if wifi is not None:
            self._wifi = wifi
            self._connect_to_wifi()
            self._wifi['is_connected'] = True
        else:
            self._wifi = {'is_connected': False}

    def _connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        login = self._wifi['login']
        password = self._wifi['password']
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(login, password)
            while not wlan.isconnected():
                sleep(0.05)
        self._wifi['is_connected'] = True

    def check_parking_places(self):
        for pp in self._state.values():
            print(pp.get_status())
            if not pp.get_status() == pp.refresh_status():
                request_url = UPDATE_PARKING_PLACE_STATUS_URL.format(parking_id=self._id, space_id=pp.get_id())
                data = ujson.dumps({'is_taken': not pp.get_status()})
                req = urequests.put(request_url, headers={'content-type': 'application/json'}, data=data)
                req.close()

    # def get_parking_places(self):
    #     return self._parking_places


class ParkingPlace:
    def __init__(self, pins=None, id=None, distance_if_taken=10,
                 max_values_to_skip_number=3, distances_to_save=10):
        self._status = False
        self._id = id
        self._pins = pins if pins is not None else {}
        self._last_distances = []
        self._distance_if_taken = distance_if_taken
        self._max_values_to_skip_number = max_values_to_skip_number
        self._distances_to_save = distances_to_save
        self._led(False)

    def get_id(self):
        return self._id

    def get_status(self):
        return self._status

    def set_status(self, new_status):
        self._status = new_status

    def _get_distance(self):
        trigger_pin = self._pins.get('trigger_pin')
        echo_pin = self._pins.get('echo_pin')
        return HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin).distance_cm()

    def refresh_status(self):
        # the heart of parking place
        distance = self._get_distance()
        if distance > 0:
            self.refresh_last_distances(distance)
        if len(self._last_distances) > self._max_values_to_skip_number:
            curr_status = self._average_distance() > self._distance_if_taken
            print(f'{self._average_distance()}\n')
            if curr_status is not self._status:
                self.set_status(curr_status)
                self._led(curr_status)
        return self._status

    def refresh_last_distances(self, distance):
        # removes the oldest distance and appends the new one
        if len(self._last_distances) > self._distances_to_save:
            self._last_distances.pop(0)
        self._last_distances.append(distance)

    def _led(self, is_available):
        # showing status on led
        led_pin = self._pins.get('led_pin')
        if led_pin:
            led = Pin(led_pin, Pin.OUT)
            led.on() if is_available else led.off()

    def _average_distance(self):
        # average distance skipping n biggest distances
        values = self._last_distances
        n = self._max_values_to_skip_number
        if len(values) <= n:
            raise ValueError('List is too short')
        sorted_values = sorted(values)[:-n]
        return sum(sorted_values)/len(sorted_values)


def main():
    pps = []
    for key, value in config.items():
        pps.append(ParkingPlace(value, key, distance_if_taken=CONSTANTS['distance_if_place_is_taken']))
    parking = Parking(id, pps, wifi)
    while True:
        parking.check_parking_places()
        sleep(0.05)


if __name__ == '__main__':
    main()
