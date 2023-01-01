import asyncio
from bleak import BleakClient

from pycycling.cycling_power_service import CyclingPowerService

async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data)

        await client.is_connected()
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(30.0)
        await trainer.disable_cycling_power_measurement_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "FOA5E101-9203-0A1-69F2-A8A21A0057E4"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
