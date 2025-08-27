

#"""P110, P110M and P115 Example"""
#
#import asyncio
#import os
#from datetime import datetime

#from tapo import ApiClient
#from tapo.requests import EnergyDataInterval


#async def main():
#    tapo_username = "**********"
#    tapo_password = "**********"
#    ip_address = "************"
#
#    client = ApiClient(tapo_username, tapo_password)
#    device = await client.p110(ip_address)
#
#    print("Turning device on...")
#    await device.on()
#
#    print("Waiting 2 seconds...")
#    await asyncio.sleep(2)
#
#    print("Turning device off...")
#    await device.off()
#
#    device_info = await device.get_device_info()
#    print(f"Device info: {device_info.to_dict()}")
#
#    device_usage = await device.get_device_usage()
#    print(f"Device usage: {device_usage.to_dict()}")
#
#    current_power = await device.get_current_power()
#    print(f"Current power: {current_power.to_dict()}")
#
#    energy_usage = await device.get_energy_usage()
#    print(f"Energy usage: {energy_usage.to_dict()}")
#
#    today = datetime.today()
#    energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
#    print(f"Energy data (hourly): {energy_data_hourly.to_dict()}")
#
#    energy_data_daily = await device.get_energy_data(
#        EnergyDataInterval.Daily,
#        datetime(today.year, get_quarter_start_month(today), 1),
#    )
#    print(f"Energy data (daily): {energy_data_daily.to_dict()}")
#
#    energy_data_monthly = await device.get_energy_data(
#        EnergyDataInterval.Monthly,
#        datetime(today.year, 1, 1),
#    )
#    print(f"Energy data (monthly): {energy_data_monthly.to_dict()}")
#
#
#def get_quarter_start_month(today: datetime) -> int:
#    return 3 * ((today.month - 1) // 3) + 1
#
#
#if __name__ == "__main__":
#    asyncio.run(main())
"""
Tapo P110 Energy Monitoring Script
Works with: P110, P110M, P115
"""

import asyncio
import os
from datetime import datetime
from tapo import ApiClient
from tapo.requests import EnergyDataInterval


# ====== CONFIG ======
TAPO_USERNAME = "sanjaygovind1234@gmail.com"
TAPO_PASSWORD = "Leo@messi1234"
PLUG_IP = "10.58.217.225"   


async def main():
    # Create API client
    client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
    device = await client.p110(PLUG_IP)

    
    print("Turning device ON...")
    await device.on()
    await asyncio.sleep(2)

    #print("Turning device OFF...")
    #await device.off()

    
    device_info = await device.get_device_info()
    print("\n== Device Info ==")
    print(device_info.to_dict())

    
    device_usage = await device.get_device_usage()
    print("\n== Device Usage ==")
    print(device_usage.to_dict())

    # Current power
    current_power = await device.get_current_power()
    print("\n== Current Power ==")
    print(current_power.to_dict())

    #  Energy usage (today)
    energy_usage = await device.get_energy_usage()
    print("\n== Energy Usage ==")
    print(energy_usage.to_dict())

    #  Energy data (hourly/daily/monthly)
    today = datetime.today()

    hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
    print("\n== Hourly Data ==")
    print(hourly.to_dict())

    daily = await device.get_energy_data(
        EnergyDataInterval.Daily,
        datetime(today.year, get_quarter_start_month(today), 1),
    )
    print("\n== Daily Data ==")
    print(daily.to_dict())

    monthly = await device.get_energy_data(
        EnergyDataInterval.Monthly,
        datetime(today.year, 1, 1),
    )
    print("\n== Monthly Data ==")
    print(monthly.to_dict())


def get_quarter_start_month(today: datetime) -> int:
    """Helper function to calculate first month of current quarter"""
    return 3 * ((today.month - 1) // 3) + 1


if __name__ == "__main__":
    asyncio.run(main())
