---
name: inverter-listening
description: "Fetches and displays live data from a Goodwe solar inverter on the local network. Use to get current solar production, battery state of charge, house consumption, and grid import/export status."
---

# Goodwe Inverter Listening

This skill provides on-demand access to a Goodwe solar inverter's live data over the local WiFi network.

## Core Functionality

The skill uses the `goodwe` Python library to connect to the inverter and retrieve a snapshot of its current operational data.

## Setup & Requirements

Before this skill can be used, the `goodwe` Python library must be installed. This is a one-time setup.

```bash
# It is recommended to use a dedicated virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install goodwe
```

## Core Script

The primary tool is `scripts/get_status.py`. It connects to a hardcoded IP address for the inverter and prints the formatted status.

**Inverter IP Address:** `192.168.1.180`

### Usage

The script is intended to be called from an alias for easy access.

```bash
/path/to/venv/bin/python scripts/get_status.py
```

## Workflow for an Agent

1.  Receive a request for solar data (e.g., "solar status").
2.  Execute the `get_status.py` script using the correct Python virtual environment.
3.  Format the script's output and present it to the user.
