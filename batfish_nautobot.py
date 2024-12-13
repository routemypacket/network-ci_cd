#!/usr/bin/env python

"""Script used to test the network with Batfish"""

from pybatfish.client.session import Session  # Correct import for Session
from rich.console import Console

# Import the get_device_config function
from nautobot_config_fetcher import get_device_config

console = Console(color_system="truecolor")

# Initialize Batfish session
bf_session = Session()  # Initialize the Batfish session

def test_duplicate_rtr_ids(session, snap):
    """Testing for duplicate router IDs"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:"
    )
    session.asserts.assert_no_duplicate_router_ids(
        snapshot=snap,
        protocols={"ospf", "bgp"},
    )
    console.print(
        ":green_heart: [bold green]No duplicate router IDs found[/bold green] :green_heart:"
    )

def test_duplicate_rtr_ids(snap):
    """Testing for duplicate router IDs"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_duplicate_router_ids(
        snapshot=snap,
        protocols={"ospf", "bgp"},
    )
    console.print(
        ":green_heart: [bold green]No duplicate router IDs found[/bold green] :green_heart:"
    )

def test_bgp_compatibility(snap):
    """Testing for incompatible BGP sessions"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_bgp_sessions(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:"
    )

def test_ospf_compatibility(snap):
    """Testing for incompatible OSPF sessions"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_ospf_sessions(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:"
    )

def test_bgp_unestablished(snap):
    """Testing for BGP sessions that are not established"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_unestablished_bgp_sessions(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:"
    )

def test_undefined_references(snap):
    """Testing for any undefined references"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for undefined references[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_undefined_references(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]No undefined refences found![/bold green] :green_heart:"
    )

def main():
    """init all the things"""
    NETWORK_NAME = "JBC_NET"
    SNAPSHOT_NAME = "snapshot00"
    SNAPSHOT_DIR = "./snapshots"

    bf_session.host = "192.168.0.130"  # Use the verified working address
    bf_session.set_network(NETWORK_NAME)

    # Manually provide the list of device names
    device_names = ["wee01-leaf-01", "wee01-leaf-02"]  # Add your device names here

    # Initialize an empty dictionary to store snapshots
    snapshots = {}

    # Create Batfish snapshots for each device
    for device_name in device_names:
        config = get_device_config(device_name)

        if config:
            # Use the 'config' variable in your Batfish snapshot
            snapshot_path = f"{SNAPSHOT_DIR}/{device_name}"
            bf_session.set_snapshot_dir(snapshot_path)
            bf_init_snapshot(config, name=device_name, overwrite=True)
            snapshots[device_name] = snapshot_path  # Store the snapshot path
        else:
            print(f"Could not retrieve config for {device_name}")

    # Initialize snapshot
    init_snap = bf_session.init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)

    # Run tests 
    test_duplicate_rtr_ids(bf_session, init_snap)  # Pass bf_session to the test function
    test_bgp_compatibility(bf_session, init_snap)  # Pass bf_session to the test function
    test_ospf_compatibility(bf_session, init_snap)  # Pass bf_session to the test function
    test_bgp_unestablished(bf_session, init_snap)  # Pass bf_session to the test function
    test_undefined_references(bf_session, init_snap)  # Pass bf_session to the test function

if __name__ == "__main__":
    main()