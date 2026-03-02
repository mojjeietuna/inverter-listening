import asyncio
import sys
from goodwe import connect

INVERTER_IP = '192.168.1.180'

async def get_solar_data():
    """Connect to the inverter and fetch the customized data."""
    try:
        inverter = await connect(INVERTER_IP)
        runtime_data = await inverter.read_runtime_data()
        all_sensors = {s.id_: s for s in inverter.sensors()}

        # --- Data Extraction ---
        soc = runtime_data.get('battery_soc')
        production = runtime_data.get('ppv')
        consumption = runtime_data.get('house_consumption')
        grid_io = runtime_data.get('pgrid')

        # --- Formatting ---
        print("\n--- Current Solar Status ---")
        
        # State of Charge
        if soc is not None:
            print(f"  State of Charge:     {soc}%")
        else:
            print("  State of Charge:     Not available")
            
        # Solar Production
        if production is not None:
            print(f"  Solar Production:    {production} W")
        else:
            print("  Solar Production:    Not available")

        # House Consumption
        if consumption is not None:
            print(f"  House Consumption:   {consumption} W")
        else:
            print("  House Consumption:   Not available")

        # Grid I/O
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
