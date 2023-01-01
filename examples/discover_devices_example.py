"""
An example script which lists all available bluetooth devices. Use this to obtain the device_address used in other
scripts
"""

import asyncio
from bleak import BleakScanner


async def run():
    devices = await BleakScanner.discover(timeout=35,return_adv=True)
    for k, v in devices.items():
        print(k, v)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
