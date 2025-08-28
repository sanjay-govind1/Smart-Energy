import os, django, json,sys
import paho.mqtt.client as mqtt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_energy.settings")
django.setup()

from energy.models import SensorReading

BROKER = "localhost"
TOPIC = "esp32/data"

def on_connect(client, userdata, flags, rc):
    print("Connected with code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temp = data.get("temperature")
        ldr = data.get("ldr")
        SensorReading.objects.create(temperature=temp, ldr=ldr)
        print(f"Saved: {temp} °C, LDR={ldr}")
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
