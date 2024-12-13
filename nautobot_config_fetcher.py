import requests

# --- Nautobot API settings ---
nautobot_url = "http://localhost:8081"  # Replace with your Nautobot URL
nautobot_token = "79c056180ba76e6e39b8cccf4b2ef9e635b15c15"  # Replace with your API token

def get_device_config(device_name):
    """Retrieves the running configuration from Nautobot for the given device name."""

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