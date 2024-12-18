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

```bash
poetry run python src/bot.py
``` 