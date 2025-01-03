#!/bin/bash

# Variables
SERVICE_DIR="/service/dbus-enphase"
CONFIG_FILE="config.ini"
RC_LOCAL="/etc/rc.local"

# Check if service directory exists
if [ -d "$SERVICE_DIR" ]; then
  echo "Service already exists in $SERVICE_DIR. Installation aborted."
  exit 1
fi

echo "Creating the config file now..."
# Prompt for token and IP
read -p "Enter the API token of your Enphase system: " TOKEN
read -p "Enter the IP address of your Enphase system: " IP_ADDRESS

# Generate the config.ini file
echo "Creating $CONFIG_FILE..."
cat <<EOF > $CONFIG_FILE
[auth]
token = $TOKEN

[network]
ip_address = $IP_ADDRESS
EOF

echo "$CONFIG_FILE created."

# Create service directory
echo "Creating service directory at $SERVICE_DIR..."
mkdir -p "$SERVICE_DIR"

# Copy necessary files
echo "Copying files to $SERVICE_DIR..."
cp -r ext "$SERVICE_DIR"
cp dbus-enphase.py "$SERVICE_DIR"
cp config.ini "$SERVICE_DIR"

# Make script executable
chmod +x "$SERVICE_DIR/dbus-enphase.py"
echo "Script dbus-enphase.py is now executable."

# Create rc.local if it doesn't exist
if [ ! -f "$RC_LOCAL" ]; then
  echo "Creating $RC_LOCAL..."
  cat <<EOF > $RC_LOCAL
#!/bin/bash

EOF
  chmod +x "$RC_LOCAL"
fi

# Add script to rc.local
if ! grep -q "$SERVICE_DIR/dbus-enphase.py" "$RC_LOCAL"; then
  echo "Adding script to $RC_LOCAL..."
  sed -i "\$i$SERVICE_DIR/dbus-enphase.py &\n" "$RC_LOCAL"
else
  echo "Script already added to $RC_LOCAL."
fi

# Run the script
echo "Starting the service..."
"$SERVICE_DIR/dbus-enphase.py" &

echo "Installation completed successfully."

