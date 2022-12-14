from flask import Flask, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

# Ställ in MQTT-klienten
app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5  # Sekunder
app.config['MQTT_TLS_ENABLED'] = False

topic = 'KYH_IoT21_Laboration2'

mqtt_client = Mqtt(app)


# Hantera MQTT-connect
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(topic)
    else:
        print('Something went wrong:', rc)


# On-message-funktion
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    m_payload = message.payload.decode('utf-8')
    print(f'Temp in Celsius: {m_payload}')

    # Spara m_payload till en textfil
    # w = Skriv över hela innehållet varje gång filen öppnas
    # r = Får bara läsa från filer
    # a = Append, lägg till ny text på slutet av filen
    with open(file='storage.txt', mode='a', encoding='utf-8') as file:
        file.write(" Temp: " + m_payload + "ºC \n")


# Gör en route som skriver ut ett sparat meddelande
@app.route('/get/')
def get_message():
    with open(file='storage.txt', mode='r', encoding='utf-8') as file:
        data = file.read()
    return jsonify({'text': data}), 200





@app.route('/')
def temp_sensor():
    show_temp = open("client.html", "r", encoding='utf-8')
    return show_temp


if __name__ == '__main__':
    app.run(debug=True)