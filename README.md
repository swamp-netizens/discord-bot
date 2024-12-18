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