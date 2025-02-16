# Dbus Enphase Service

A virtual device for the Victron Energy ecosystem that retrieves real-time data from the Enphase web service and makes it available on the Victron D-Bus. This service enables seamless integration of Enphase energy production data into Victron systems for monitoring and analysis.

## Features

- Retrieves power and energy production data from Enphase microinverters.
- Publishes data to Victron’s D-Bus for compatibility with Victron monitoring tools.
- Configurable via an external `config.ini` file for authentication and network setup.

## Use Cases

- **Hybrid Systems**: Monitor Enphase production data alongside Victron installations.
- **Energy Insights**: Integrate Enphase inverter data into Victron GX devices.

## Installation

 ```bash
wget https://github.com/falcovd/dbus-enphase/archive/refs/tags/v1.0.0.zip # replace v1.0.0 with the latest release
unzip v1.0.0.zip
cd v1.0.0
chmod +x install.sh && ./install.sh
 ```
    
## Configuration

The `config.ini` file contains:

- **Auth Section**:
  - `token`: Enphase API access token.
- **Network Section**:
  - `ip_address`: IP address of the Enphase system.

## Limitations
In this version there are some limitations, because I have developed the system primarily for my own use. The limitations are:
- Only metering and parsing 1 phase
- Hardcoded 230V on L1 Voltage
- Calculating Amps from L1 - (PV production / 230)
- Hardcoded maximum power 4350W (my PV capacity)

## Development

### Prerequisites

- Python 3.x
- Victron's `velib_python` library (included in submodule)

### Testing

Run the script to simulate the D-Bus service and test its functionality:
```bash
python3 dbus_enphase_service.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or fixes.
