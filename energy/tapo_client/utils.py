import asyncio
from tapo import ApiClient
from energy.models import EnergyReading

# Tapo credentials and plug IP
TAPO_USERNAME = "sanjaygovind1234@gmail.com"
TAPO_PASSWORD = "Leo@messi1234"
PLUG_IP = "10.58.217.225"  # Your plug IP


async def fetch_tapo_data_async():
    """
    Fetch energy data from the plug without turning it on/off.
    """
    client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
    device = await client.p110(PLUG_IP)

    device_info = await device.get_device_info()
    energy_usage = await device.get_energy_usage()

    return {
        "device_name": device_info.nickname,
        "current_power": energy_usage.current_power,   # usually in Watts
        "today_energy": energy_usage.today_energy,     # kWh
        "month_energy": energy_usage.month_energy,     # kWh
        "runtime_minutes": energy_usage.today_runtime, # minutes
    }


def collect_reading_sync():
    """
    Synchronous wrapper for Django views.
    Runs async Tapo fetcher, saves result to DB, and returns the saved record.
    """
    data = asyncio.run(fetch_tapo_data_async())
    reading = EnergyReading.objects.create(**data)
    return reading
