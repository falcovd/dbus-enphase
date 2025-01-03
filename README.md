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

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/falcovd/dbus-enphase.git
    cd dbus-enphase
    ```

2. **Install Dependencies**:
    Ensure Python 3.x is installed on your system, then install required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare the `config.ini` File**:
    Create a `config.ini` file in the root directory with the following structure:
    ```ini
    [auth]
    token = your_actual_token_here

    [network]
    ip_address = ip_address_of_enphase
    ```
    - Replace `your_actual_token_here` with your Enphase API token.
    - Update `ip_address` with the IP address of your Enphase system.

4. **Run the Script**:
    ```bash
    chmod +x install.sh && ./install.sh
    ```

## Configuration

The `config.ini` file contains:

- **Auth Section**:
  - `token`: Enphase API access token.
- **Network Section**:
  - `ip_address`: IP address of the Enphase system.

## Development

### Prerequisites

- Python 3.x
- Victron's `velib_python` library

### Testing

Run the script to simulate the D-Bus service and test its functionality:
```bash
python3 dbus_enphase_service.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or fixes.
