#!/usr/bin/env python

"""Script used to test the network with Batfish"""

from pybatfish.client.session import Session
from rich.console import Console

# Import the get_device_config function
from nautobot_config_fetcher import get_device_config

console = Console(color_system="truecolor")

# Initialize Batfish session
bf_session = Session()

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

def test_bgp_compatibility(session, snap):
    """Testing for incompatible BGP sessions"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    session.asserts.assert_no_incompatible_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:"
    )

def test_ospf_compatibility(session, snap):
    """Testing for incompatible OSPF sessions"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:"
    )
    session.asserts.assert_no_incompatible_ospf_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:"
    )

def test_bgp_unestablished(session, snap):
    """Testing for BGP sessions that are not established"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    session.asserts.assert_no_unestablished_bgp_sessions(snapshot=snap)
    console.print(
        ":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:"
    )

def test_undefined_references(session, snap):
    """Testing for any undefined references"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for undefined references[/bold yellow] :white_exclamation_mark:"
    )
    session.asserts.assert_no_undefined_references(snapshot=snap)
    console.print(
        ":green_heart: [bold green]No undefined references found![/bold green] :green_heart:"
    )

def main():
    """Initialize all the things"""
    NETWORK_NAME = "JBC_NET"
    SNAPSHOT_NAME = "snapshot00"
    SNAPSHOT_DIR = "./snapshots"

    # Initialize Batfish session
    bf_session = Session()
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
            # For example, to create a snapshot:
            snapshots[device_name] = bf_session.add_snapshot(config, name=device_name)
        else:
            print(f"Could not retrieve config for {device_name}")

    # Run Batfish tests for each snapshot
    for device_name, snapshot in snapshots.items():
        console.print(f"[bold blue]Testing device: {device_name}[/bold blue]")
        
        # Set the snapshot for the current device
        bf_session.set_snapshot(snapshot.snapshot)

        # Run your tests (assuming these functions are defined elsewhere)
        test_duplicate_rtr_ids(bf_session, init_snap)
        test_bgp_compatibility(bf_session, init_snap)
        test_ospf_compatibility(bf_session, init_snap)
        test_bgp_unestablished(bf_session, init_snap)
        test_undefined_references(bf_session, init_snap)
        console.print("\n")  # Add an empty line between devices

if __name__ == "__main__":
    main()