import os, django, json, sys , asyncio
import paho.mqtt.client as mqtt
from tapo import ApiClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(PROJECT_ROOT) 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_energy.settings") 
django.setup() 
from energy.models import SensorReading

BROKER = "localhost"
TOPIC = "esp32/data"

# 🔹 Plug config (set via env vars or hardcode for testing)
PLUG_IP = "10.58.217.225"
TAPO_USERNAME = "sanjaygovind1234@gmail.com"
TAPO_PASSWORD = "Leo@messi1234"
TEMP_THRESHOLD = 30.0  # °C


def on_connect(client, userdata, flags, rc):
    print("Connected with code", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temp = data.get("temperature")
        ldr = data.get("ldr")

        # Save sensor data
        SensorReading.objects.create(temperature=temp, ldr=ldr)
        print(f"Saved: {temp} °C, LDR={ldr}")

        if temp and temp > TEMP_THRESHOLD:
            asyncio.run(update_plug_status(temp,"on"))

        if temp and temp < TEMP_THRESHOLD:
            asyncio.run(update_plug_status(temp,"off"))
        


    except Exception as e:
        print("Error:", e)

async def update_plug_status(temp,status):
    """Async function to turn off the Tapo plug."""
    try:
        client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
        plug = await client.p110(PLUG_IP)
        device_info = await plug.get_device_info()
        # print(f"Device info: {device_info.to_dict()}")
        is_on = device_info.to_dict().get('device_on', False)
        print(f"Device is currently ON: {is_on}")

        if status == "on" and is_on:    # only turn off if currently on
            await plug.off()
            print(f"⚠️ Plug turned OFF due to high temp: {temp}°C")
        elif status == "off" and not is_on:  # only turn on if currently off
            await plug.on()
            print("✅ Plug turned ON")
    except Exception as e:
        print("Error controlling plug:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
