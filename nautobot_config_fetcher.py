import os
import requests

# --- Nautobot API settings ---
nautobot_url = "http://localhost:8081"  # Replace with your Nautobot URL
nautobot_token = "79c056180ba76e6e39b8cccf4b2ef9e635b15c15"  # Replace with your API token

SNAPSHOT_DIR = "/drone/src/snapshots/configs"  # Updated path to store configs

def get_device_config(device_name):
    """Retrieves the running configuration from Nautobot,
    replaces literal '\n' with actual newlines, prints it, and saves it to a file.
    """

    try:
        # Get the device ID
        device_id = get_device_id(device_name)
        if not device_id:
            print(f"Device '{device_name}' not found in Nautobot.")
            return None

        # Construct the API URL for config context
        url = f"{nautobot_url}/api/dcim/devices/{device_id}/"
        headers = {
            "Authorization": f"Token {nautobot_token}",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Access the config using "local_config_context_data"
        config = data["local_config_context_data"].get("running_config")

        if config:
            # Replace literal '\n' with actual newline characters
            config = config.replace("\\n", "\n")
            #print(config)  # Print the config with newlines

            # Save the configuration to a file
            if not os.path.exists(SNAPSHOT_DIR):
                os.makedirs(SNAPSHOT_DIR)  # Create the snapshots/configs directory if it doesn't exist
            filepath = os.path.join(SNAPSHOT_DIR, f"{device_name}.cfg")
            with open(filepath, "w") as f:
                f.write(config)  # Write the config to the file

        return config  # Return the config as is

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving config for {device_name}: {e}")
        return None

def get_device_id(device_name):
    """Retrieves the device ID from Nautobot for the given device name."""
    try:
        url = f"{nautobot_url}/api/dcim/devices/?name={device_name}"
        headers = {
            "Authorization": f"Token {nautobot_token}",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        if data["count"] == 1:
            return data["results"][0]["id"]
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving device ID for {device_name}: {e}")
        return None

def update_configs():
    """Updates the configuration files in the snapshots/configs folder."""
    device_names = ["wee01-leaf-02", "wee01-leaf-03"]  # Add your device names here
    for device_name in device_names:
        get_device_config(device_name)

def print_ls_snapshots():  # Updated function
    """Prints the output of the 'ls -l snapshots/configs' command."""
    try:
        # Execute the 'ls -l' command on the 'snapshots/configs' directory
        stream = os.popen("ls -l snapshots/configs")
        # Read the output from the command
        output = stream.read()
        # Print the output
        print(output)
    except Exception as e:
        print(f"Error executing ls command: {e}")

# Call the update_configs function when the script is run
if __name__ == "__main__":
    update_configs()