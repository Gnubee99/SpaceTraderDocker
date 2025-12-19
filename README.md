# SpaceTraderDocker

A Docker-deployable application to interact and play the [SpaceTraders.io](https://spacetraders.io) API game. Navigate the stars, trade goods, and build your space empire!

## Features

- 🚀 Docker-based deployment for easy setup
- 🎮 Interactive SpaceTraders.io API client
- 📊 View agent information, ships, and contracts
- 🌟 Register new agents
- 🔄 Continuous operation mode
- 🐍 Python-based implementation

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (optional, but recommended)
- SpaceTraders.io API token (or create a new agent)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. Clone this repository:
   ```bash
   git clone https://github.com/Gnubee99/SpaceTraderDocker.git
   cd SpaceTraderDocker
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your SpaceTraders API token:
   ```env
   SPACETRADERS_TOKEN=your_token_here
   ```

4. Run the application:
   ```bash
   docker-compose up
   ```

### Option 2: Using Docker CLI

Build and run with Docker CLI:

```bash
# Build the image
docker build -t spacetraders-app .

# Run with your token
docker run -e SPACETRADERS_TOKEN=your_token_here spacetraders-app
```

## Usage

### View Your Agent Information

Run the container with your API token to view agent info, ships, and contracts:

```bash
docker run -e SPACETRADERS_TOKEN=your_token_here spacetraders-app
```

### Register a New Agent

To register a new agent and get an API token:

```bash
docker run \
  -e REGISTER_NEW_AGENT=true \
  -e AGENT_CALLSIGN=YourCallsign \
  -e AGENT_FACTION=COSMIC \
  spacetraders-app
```

**Important:** Save the token that is displayed! You'll need it for future runs.

### Keep Container Running

For continuous operations, use keep-alive mode:

```bash
docker run \
  -e SPACETRADERS_TOKEN=your_token_here \
  -e KEEP_ALIVE=true \
  spacetraders-app
```

Or with docker-compose:

```bash
# Edit .env and set KEEP_ALIVE=true
docker-compose up -d
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SPACETRADERS_TOKEN` | Your SpaceTraders API token | - | Yes (unless registering) |
| `KEEP_ALIVE` | Keep container running indefinitely | `false` | No |
| `REGISTER_NEW_AGENT` | Register a new agent | `false` | No |
| `AGENT_CALLSIGN` | Callsign for new agent | - | Yes (if registering) |
| `AGENT_FACTION` | Starting faction for new agent | `COSMIC` | No |

## Available Factions

When registering a new agent, you can choose from these factions:
- `COSMIC` - The Cosmic Engineers
- `VOID` - The Voidfarers
- `GALACTIC` - The Galactic Alliance
- `QUANTUM` - The Quantum Federation
- `DOMINION` - The Stellar Dominion

## Docker Commands Reference

```bash
# Build the image
docker build -t spacetraders-app .

# Run container
docker run spacetraders-app

# Run in background (detached mode)
docker run -d spacetraders-app

# View logs
docker logs -f spacetraders-client

# Stop container
docker stop spacetraders-client

# Remove container
docker rm spacetraders-client
```

## Development

### Project Structure

```
SpaceTraderDocker/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker build exclusions
├── .env.example        # Environment variables template
├── .gitignore         # Git exclusions
└── README.md          # This file
```

### Local Development

To run locally without Docker:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable and run
export SPACETRADERS_TOKEN=your_token_here
python main.py
```

## Troubleshooting

### "No SPACETRADERS_TOKEN environment variable found"

Make sure you've set the `SPACETRADERS_TOKEN` environment variable either in your `.env` file or when running the docker command.

### "Failed to get agent info: 401"

Your API token is invalid or expired. Try registering a new agent or check that you've copied the token correctly.

### Container exits immediately

This is normal behavior unless `KEEP_ALIVE=true` is set. The application retrieves your game state and exits. Use `docker logs` to view the output.

## Resources

- [SpaceTraders.io Official Site](https://spacetraders.io)
- [SpaceTraders API Documentation](https://docs.spacetraders.io)
- [Docker Documentation](https://docs.docker.com)

## License

This project is open source and available for use under standard open source terms.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
