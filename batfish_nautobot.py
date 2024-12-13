#!/usr/bin/env python

"""Script used to test the network with batfish"""

import os  # Import the os module

from pybatfish.client.commands import *
from pybatfish.question import load_questions
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_incompatible_bgp_sessions,
    assert_no_incompatible_ospf_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_undefined_references,
)
from rich.console import Console

# Import the get_device_config function
from nautobot_config_fetcher import get_device_config

console = Console(color_system="truecolor")

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
    bf_session.host = "192.168.0.130"
    bf_set_network(NETWORK_NAME)

    # Manually provide the list of device names
    device_names = ["wee01-leaf-01", "wee01-leaf-02"]  # Add your device names here

    # Create the snapshot directory if it doesn't exist
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    # Initialize an empty dictionary to store snapshots
    snapshots = {}

    # Fetch configurations from Nautobot and initialize Batfish snapshots
    for device_name in device_names:
        config = get_device_config(device_name)

        if config:
            # Use the 'config' variable with init_snapshot
            snapshot_path = f"{SNAPSHOT_DIR}/{device_name}"
            bf_session.set_snapshot_dir(snapshot_path)  # Set the snapshot directory
            bf_init_snapshot(config, name=device_name, overwrite=True)  # Initialize the snapshot
            snapshots[device_name] = snapshot_path  # Store the snapshot path
        else:
            print(f"Could not retrieve config for {device_name}")
    
    # The rest of the main function remains the same
    load_questions()
    test_duplicate_rtr_ids(init_snap)
    test_bgp_compatibility(init_snap)
    test_ospf_compatibility(init_snap)
    test_bgp_unestablished(init_snap)
    test_undefined_references(init_snap)

if __name__ == "__main__":
    main()