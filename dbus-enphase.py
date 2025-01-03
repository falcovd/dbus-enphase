#!/usr/bin/env python3

"""
A class to put a simple service on the dbus, according to Victron standards, with constantly updating
paths. See example usage below. It is used to generate dummy data for other processes that rely on the
dbus. See files in dbus_vebus_to_pvinverter/test and dbus_vrm/test for other usage examples.

To change a value while testing, without stopping your dummy script and changing its initial value, write
to the dummy data via the dbus. See example.

https://github.com/victronenergy/dbus_vebus_to_pvinverter/tree/master/test
"""

import os
import sys
import time
import json
import logging
import platform
import argparse
import requests
import urllib3
from configparser import ConfigParser
from gi.repository import GLib

# import the velib
sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext/velib_python'))
from vedbus import VeDbusService

class DbusEnphaseService:
    def __init__(self, servicename, deviceinstance, paths, productname='Enphase', connection='Enphase service', productid=0):
        self._dbusservice = VeDbusService(servicename)
        self._paths = paths

        logging.debug(f"{servicename} /DeviceInstance = {deviceinstance}")

        # Create the management objects, as specified in the ccgx dbus-api document
        self._dbusservice.add_path('/Mgmt/ProcessName', __file__)
        self._dbusservice.add_path('/Mgmt/ProcessVersion', f"Unknown version, and running on Python {platform.python_version()}")
        self._dbusservice.add_path('/Mgmt/Connection', connection)

        # Create the mandatory objects
        self._dbusservice.add_path('/DeviceInstance', deviceinstance)
        self._dbusservice.add_path('/ProductId', productid)
        self._dbusservice.add_path('/ProductName', productname)
        self._dbusservice.add_path('/FirmwareVersion', 0)
        self._dbusservice.add_path('/HardwareVersion', 0)
        self._dbusservice.add_path('/Connected', 1)

        for path, settings in self._paths.items():
            self._dbusservice.add_path(
                path, settings['initial'], writeable=True, onchangecallback=self._handle_changed_value
            )

        self._dbusservice.register()
        GLib.timeout_add(5000, self._update)

        # Load configuration
        self._config = self._load_config()

    def _load_config(self):
        config = ConfigParser()
        config.read('config.ini')
        return {
            'token': config.get('auth', 'token'),
            'ip_address': config.get('network', 'ip_address')
        }

    def _update(self):
        try:
            req_headers = self._get_headers()
            ip_address = self._config['ip_address']
            response = requests.get(
                f"https://{ip_address}/production.json?details=1",
                headers=req_headers,
                timeout=15,
                verify=False
            )
            data = response.json()

            now = max(data["production"][0]["wNow"], 0)
            kWh_lifetime = round(data["production"][0]["whLifetime"] / 1000, 3)

            self._dbusservice['/Ac/Energy/Forward'] = kWh_lifetime
            self._dbusservice['/Ac/Power'] = now
            self._dbusservice['/Ac/L1/Power'] = now
            self._dbusservice['/Ac/L1/Voltage'] = 230
            self._dbusservice['/Ac/L1/Current'] = round(now / 230, 3)
        except Exception as e:
            logging.error(f"Error occurred during update: {e}")
        return True

    def _get_headers(self):
        urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
        token = self._config['token']
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def _handle_changed_value(path, value):
        logging.debug(f"Path {path} updated to {value}")
        return True  # Accept the change

# === Main script for debugging purposes ===

def _check_config_file():
    if not os.path.exists('config.ini'):
        logging.error("Configuration file 'config.ini' not found. Please create it and provide the required settings.")
        sys.exit(1)

    config = ConfigParser()
    config.read('config.ini')

    if not config.has_section('auth') or not config.has_option('auth', 'token'):
        logging.error("Missing 'auth' section or 'token' in 'config.ini'.")
        sys.exit(1)

    if not config.has_section('network') or not config.has_option('network', 'ip_address'):
        logging.error("Missing 'network' section or 'ip_address' in 'config.ini'.")
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.DEBUG)
    _check_config_file()

    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)

    pvac_output = DbusEnphaseService(
        servicename='com.victronenergy.pvinverter.enphase',
        deviceinstance=0,
        paths={
            '/Ac/Energy/Forward': {'initial': None},
            '/Ac/Power': {'initial': None},
            '/Ac/MaxPower': {'initial': 4350},
            '/ErrorCode': {'initial': 0},
            '/Ac/L1/Power': {'initial': None},
            '/Ac/L1/Current': {'initial': 0},
            '/Ac/L1/Voltage': {'initial': 0},
            '/Position': {'initial': 1},
        }
    )

    logging.info('Connected to dbus, switching to GLib.MainLoop()')
    mainloop = GLib.MainLoop()
    mainloop.run()

if __name__ == "__main__":
    main()

