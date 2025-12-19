#!/usr/bin/env python3
"""
SpaceTraders.io API Game Client
A Docker-deployable application to interact with SpaceTraders.io API
"""

import os
import requests
import time
from datetime import datetime

# API Configuration
API_BASE_URL = "https://api.spacetraders.io/v2"
API_TOKEN = os.environ.get("SPACETRADERS_TOKEN", "")

class SpaceTradersClient:
    """Client for interacting with SpaceTraders.io API"""
    
    def __init__(self, token=None):
        self.token = token or API_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def register_agent(self, callsign, faction="COSMIC"):
        """Register a new agent"""
        url = f"{API_BASE_URL}/register"
        data = {
            "symbol": callsign,
            "faction": faction
        }
        response = requests.post(url, json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Agent registered successfully!")
            print(f"  Callsign: {result['data']['agent']['symbol']}")
            print(f"  Token: {result['data']['token']}")
            print(f"  Faction: {result['data']['agent']['startingFaction']}")
            return result['data']['token']
        else:
            print(f"✗ Registration failed: {response.status_code}")
            print(f"  {response.text}")
            return None
    
    def get_agent_info(self):
        """Get current agent information"""
        if not self.token:
            print("✗ No API token provided")
            return None
        
        url = f"{API_BASE_URL}/my/agent"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            data = result.get('data')
            if not data:
                print(f"✗ Unexpected API response format")
                return None
            print(f"\n=== Agent Information ===")
            print(f"Callsign: {data['symbol']}")
            print(f"Headquarters: {data['headquarters']}")
            print(f"Credits: {data['credits']:,}")
            print(f"Starting Faction: {data['startingFaction']}")
            return data
        else:
            print(f"✗ Failed to get agent info: {response.status_code}")
            print(f"  {response.text}")
            return None
    
    def list_ships(self):
        """List all ships owned by the agent"""
        if not self.token:
            print("✗ No API token provided")
            return None
        
        url = f"{API_BASE_URL}/my/ships"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            ships = result.get('data', [])
            print(f"\n=== Ships ({len(ships)}) ===")
            for ship in ships:
                print(f"  • {ship['symbol']} - {ship['registration']['role']}")
                print(f"    Location: {ship['nav']['waypointSymbol']}")
                print(f"    Status: {ship['nav']['status']}")
                print(f"    Fuel: {ship['fuel']['current']}/{ship['fuel']['capacity']}")
            return ships
        else:
            print(f"✗ Failed to list ships: {response.status_code}")
            print(f"  {response.text}")
            return None
    
    def list_contracts(self):
        """List all contracts"""
        if not self.token:
            print("✗ No API token provided")
            return None
        
        url = f"{API_BASE_URL}/my/contracts"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            contracts = result.get('data', [])
            print(f"\n=== Contracts ({len(contracts)}) ===")
            for contract in contracts:
                print(f"  • {contract['id']}")
                print(f"    Type: {contract['type']}")
                print(f"    Accepted: {contract['accepted']}")
                print(f"    Fulfilled: {contract['fulfilled']}")
                if not contract['fulfilled']:
                    print(f"    Deadline: {contract['terms']['deadline']}")
            return contracts
        else:
            print(f"✗ Failed to list contracts: {response.status_code}")
            print(f"  {response.text}")
            return None
    
    def get_system_info(self, system_symbol):
        """Get information about a system"""
        url = f"{API_BASE_URL}/systems/{system_symbol}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            data = result.get('data')
            if not data:
                print(f"✗ Unexpected API response format")
                return None
            print(f"\n=== System: {system_symbol} ===")
            print(f"Type: {data['type']}")
            print(f"Coordinates: ({data['x']}, {data['y']})")
            print(f"Waypoints: {len(data.get('waypoints', []))}")
            return data
        else:
            print(f"✗ Failed to get system info: {response.status_code}")
            return None

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("   SpaceTraders.io Docker Client")
    print("   Navigate the stars, trade goods, build your empire!")
    print("=" * 60)
    print()

def main():
    """Main application entry point"""
    print_banner()
    
    # Check if token is provided
    if not API_TOKEN:
        print("⚠ No SPACETRADERS_TOKEN environment variable found")
        print("\nTo use this application, you need to:")
        print("1. Register at https://spacetraders.io")
        print("2. Get your API token")
        print("3. Set the SPACETRADERS_TOKEN environment variable")
        print("\nExample:")
        print("  docker run -e SPACETRADERS_TOKEN=your_token_here spacetraders-app")
        print("\nTo register a new agent, set REGISTER_NEW_AGENT=true")
        print("  docker run -e REGISTER_NEW_AGENT=true -e AGENT_CALLSIGN=MyAgent spacetraders-app")
        return
    
    client = SpaceTradersClient(API_TOKEN)
    
    # Check if we should register a new agent
    if os.environ.get("REGISTER_NEW_AGENT", "").lower() == "true":
        callsign = os.environ.get("AGENT_CALLSIGN", "")
        faction = os.environ.get("AGENT_FACTION", "COSMIC")
        
        if not callsign:
            print("✗ AGENT_CALLSIGN environment variable required for registration")
            return
        
        token = client.register_agent(callsign, faction)
        if token:
            print("\n⚠ Save this token! Set SPACETRADERS_TOKEN to this value for future runs.")
        return
    
    # Display agent information
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    agent = client.get_agent_info()
    if agent:
        client.list_ships()
        client.list_contracts()
        
        # Get system info if headquarters is available
        if 'headquarters' in agent:
            headquarters = agent['headquarters']
            if '-' in headquarters:
                system_symbol = headquarters.split('-')[0]
                client.get_system_info(system_symbol)
    
    print("\n" + "=" * 60)
    print("Application completed successfully!")
    print("To keep the container running, set KEEP_ALIVE=true")
    
    # Keep alive mode for continuous operation
    if os.environ.get("KEEP_ALIVE", "").lower() == "true":
        print("Keep-alive mode enabled. Container will run indefinitely.")
        print("Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")

if __name__ == "__main__":
    main()
