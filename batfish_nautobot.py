#!/usr/bin/env python

"""Script used to test the network with Batfish"""

from pybatfish.client.session import Session
from rich.console import Console

# Import the update_configs function
from nautobot_config_fetcher import update_configs  

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

def print_ls_snapshots():
    """Prints the output of the 'ls -l snapshots' command."""
    try:
        # Execute the 'ls -l' command on the 'snapshots' directory
        stream = os.popen("ls -l snapshots")
        # Read the output from the command
        output = stream.read()
        # Print the output
        print(output)
    except Exception as e:
        print(f"Error executing ls command: {e}")

def main():
    """init all the things"""
    NETWORK_NAME = "JBC_NET"
    SNAPSHOT_NAME = "snapshot00"
    SNAPSHOT_DIR = "./snapshots"

    # Update the configuration files in the snapshots folder
    update_configs()

    # Print the contents of the snapshots directory
    print_ls_snapshots()  

    bf_session.host = "192.168.0.130"  # Use the verified working address
    bf_session.set_network(NETWORK_NAME)

    # Initialize snapshot
    init_snap = bf_session.init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)

    # Run tests
    test_duplicate_rtr_ids(bf_session, init_snap)
    test_bgp_compatibility(bf_session, init_snap)
    test_ospf_compatibility(bf_session, init_snap)
    test_bgp_unestablished(bf_session, init_snap)
    test_undefined_references(bf_session, init_snap)

if __name__ == "__main__":
    main()