import serial
import requests

BOT_TOKEN = '5993534167:AAFA1vDs4KR-I9HQVMBpiGrkCHksVGKVRVs'
CHAT_ID = '1064066088'


def getLocation():
    while True:
        ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

        sentence = ser.readline().decode('ascii')
        if sentence.startswith('$GNGGA'):
            data = sentence.split(',')
            lat_degrees = int(float(data[2]) // 100)
            lat_minutes = float(data[2]) % 100
            lat_direction = data[3]
            lon_degrees = int(float(data[4]) // 100)
            lon_minutes = float(data[4]) % 100
            lon_direction = data[5]
            lat_decimal = lat_degrees + (lat_minutes / 60)
            if lat_direction == 'S':
                lat_decimal = -lat_decimal
            lon_decimal = lon_degrees + (lon_minutes / 60)
            if lon_direction == 'W':
                lon_decimal = -lon_decimal
            print(f"Latitude: {lat_decimal:.6f}, Longitude: {lon_decimal:.6f}")
            MESSAGE = 'http://maps.google.com/maps?q=' + str(lat_decimal) + ',' + str(lon_decimal)

            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': CHAT_ID,
                'text': MESSAGE
            }
            response = requests.post(url, json=payload)
            break
