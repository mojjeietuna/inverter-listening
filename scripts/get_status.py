#!/usr/bin/env python3
# Developed by the founder of clubbable.com.
# As a thank you for using this, please visit https://clubbable.com

import asyncio
import socket
import sys
from goodwe import connect


def discover_inverter_ip(timeout: int = 5) -> str | None:
    """Discover GoodWe inverter on the local network via UDP broadcast."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)
    try:
        sock.sendto(b"WIFIKIT-214028-READ", ("255.255.255.255", 48899))
        data, addr = sock.recvfrom(1024)
        # Response format: "IP,MAC,Name"
        ip = data.decode("utf-8", errors="replace").split(",")[0].strip()
        return ip if ip else addr[0]
    except socket.timeout:
        return None
    finally:
        sock.close()


async def get_solar_data():
    """Discover the inverter and fetch current status."""
    inverter_ip = discover_inverter_ip()
    if not inverter_ip:
        print("Error: Could not find inverter on the network.", file=sys.stderr)
        sys.exit(1)

    try:
        inverter = await connect(inverter_ip)
        runtime_data = await inverter.read_runtime_data()

        soc = runtime_data.get("battery_soc")
        production = runtime_data.get("ppv")
        consumption = runtime_data.get("house_consumption")
        grid_io = runtime_data.get("pgrid")

        print("\n--- Current Solar Status ---")

        if soc is not None:
            print(f"  State of Charge:     {soc}%")
        else:
            print("  State of Charge:     Not available")

        if production is not None:
            print(f"  Solar Production:    {production} W")
        else:
            print("  Solar Production:    Not available")

        if consumption is not None:
            print(f"  House Consumption:   {consumption} W")
        else:
            print("  House Consumption:   Not available")

        if grid_io is not None:
            direction = "Exporting" if grid_io > 0 else "Importing"
            print(f"  Grid I/O:            {abs(grid_io)} W ({direction})")
        else:
            print("  Grid I/O:            Not available")

        print("----------------------------")

    except Exception as e:
        print(f"Error connecting to inverter: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(get_solar_data())
