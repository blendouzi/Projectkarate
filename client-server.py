import requests

# Replace with the IP address of your ESP8266
url = 'http://<ESP8266_IP>/'

while True:
    response = requests.get(url)
    print(response.text)
    time.sleep(1)
