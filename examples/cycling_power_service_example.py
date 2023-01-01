import asyncio
from bleak import BleakClient
import sys

from pycycling.cycling_power_service import CyclingPowerService

# Borrowing heavily from aioconsole
async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)


async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data)

        await client.is_connected()
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        input = ''
        while not input:
            await ainput('Press any key to quit:')
        await trainer.disable_cycling_power_measurement_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "FA:05:BF:24:96:CC"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
