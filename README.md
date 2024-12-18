# Swamp Discord Bot

A Discord bot for managing a friend server.

## Setup

1. Make sure you have Python 3.10+ installed
2. Install Poetry (package manager):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Create a `.env` file in the root directory with your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```

## Development

- Format code: `poetry run black .`
- Sort imports: `poetry run isort .`
- Lint code: `poetry run pylint src`

## Running the Bot

### Using Poetry
```bash
poetry run python src/bot.py
```

### Using Docker

You can pull the latest image from GitHub Container Registry:
```bash
docker pull ghcr.io/YOUR_GITHUB_USERNAME/swamp-discord-bot:main
```

Run the bot using Docker:
```bash
docker run -d \
  --name swamp-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN=your_token_here \
  ghcr.io/YOUR_GITHUB_USERNAME/swamp-discord-bot:main
```

### Using Nomad

1. Store your Discord token on the Nomad server:
   ```bash
   sudo mkdir -p /etc/discord
   echo "your_discord_token" | sudo tee /etc/discord/token
   sudo chmod 600 /etc/discord/token
   ```

2. Deploy the bot using Nomad:
   ```bash
   nomad job run swamp-bot.nomad
   ```

3. Check the status:
   ```bash
   nomad status swamp-discord-bot
   ```

The Nomad configuration:
- Mounts the token file from `/etc/discord/token` on the host
- Uses Nomad's template feature to securely pass the token to the container
- Includes automatic restarts and resource limits
- Pulls the latest image from GHCR

## CI/CD

This project uses GitHub Actions to automatically build and push Docker images to GitHub Container Registry (GHCR). The workflow:
- Builds on every push to main and pull requests
- Pushes images only on merges to main
- Tags images with:
  - Git SHA
  - Branch name
  - Semver tags (when version tags are pushed)

To use the GitHub Container Registry:
1. Ensure your repository has access to GitHub Packages
2. Use a Personal Access Token (PAT) with `packages:read` scope to pull images
3. Images are public by default, but you can change visibility in package settings 