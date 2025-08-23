# import asyncio
# from pprint import pprint
# from tapo import ApiClient

# TAPO_EMAIL = "**********"   
# TAPO_PASSWORD = "*********"        
# PLUG_IP = "*********"                    

# async def main():
#     client = ApiClient(TAPO_EMAIL, TAPO_PASSWORD)

#     plug = await client.p110(PLUG_IP)

#     # Device info
#     info = await plug.get_device_info()
#     print("== Device Info ==")
#     print(f"Model: {info.model}")
#     print(f"Nickname: {info.nickname}")
#     print(f"Device On?: {info.device_on}")
#     print(f"Firmware version: {info.fw_ver}")

#     # Live power (Watts)
#     current_power_w = await plug.get_current_power()
#     print("\n== Current Power (W) ==")
#     print(current_power_w.__dict__)

#     # Energy usage (kWh)
#     usage = await plug.get_energy_usage()
#     print("\n== Energy Usage ==")
#     print(f"Today: {usage.today_energy} kWh")
#     print(f"Month: {usage.month_energy} kWh")

# if __name__ == "__main__":
#     asyncio.run(main())

"""P110, P110M and P115 Example"""

import asyncio
import os
from datetime import datetime

from tapo import ApiClient
from tapo.requests import EnergyDataInterval


async def main():
    tapo_username = "**********"
    tapo_password = "**********"
    ip_address = "************"

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)

    print("Turning device on...")
    await device.on()

    print("Waiting 2 seconds...")
    await asyncio.sleep(2)

    print("Turning device off...")
    await device.off()

    device_info = await device.get_device_info()
    print(f"Device info: {device_info.to_dict()}")

    device_usage = await device.get_device_usage()
    print(f"Device usage: {device_usage.to_dict()}")

    current_power = await device.get_current_power()
    print(f"Current power: {current_power.to_dict()}")

    energy_usage = await device.get_energy_usage()
    print(f"Energy usage: {energy_usage.to_dict()}")

    today = datetime.today()
    energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
    print(f"Energy data (hourly): {energy_data_hourly.to_dict()}")

    energy_data_daily = await device.get_energy_data(
        EnergyDataInterval.Daily,
        datetime(today.year, get_quarter_start_month(today), 1),
    )
    print(f"Energy data (daily): {energy_data_daily.to_dict()}")

    energy_data_monthly = await device.get_energy_data(
        EnergyDataInterval.Monthly,
        datetime(today.year, 1, 1),
    )
    print(f"Energy data (monthly): {energy_data_monthly.to_dict()}")


def get_quarter_start_month(today: datetime) -> int:
    return 3 * ((today.month - 1) // 3) + 1


if __name__ == "__main__":
    asyncio.run(main())
