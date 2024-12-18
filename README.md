# 🧅 Swamp Discord Bot

Welcome to the Swampiest Discord bot in all the land! Like Shrek's onion, this bot has layers... of functionality!

## 🏰 Setting Up Your Own Swamp

1. Make sure you've got Python 3.10+ installed (even Donkey could do this!)
2. Install Poetry (it's like finding the perfect swamp, but for code):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install the magical dependencies (they're like onion layers):
   ```bash
   poetry install
   ```
4. Create a `.env` file (your secret scroll) with your Discord token:
   ```
   DISCORD_TOKEN=your_magical_token_here
   ```

## 🧪 Development (or "Brewing Swamp Potions")

- Format code (make it pretty like Fiona): `poetry run black .`
- Sort imports (arrange them like Shrek arranges his swamp): `poetry run isort .`
- Lint code (check for ogre-sized mistakes): `poetry run pylint src`

## 🏃‍♂️ Running Your Swamp Bot

### 🧙‍♂️ Using Poetry (The Magical Way)
```bash
poetry run python src/bot.py
```

### 🐋 Using Docker (The Far Far Away Way)

Pull the image from the magical registry (like stealing a potion from the Fairy Godmother's factory):
```bash
docker pull ghcr.io/swamp-netizens/discord-bot:main
```

Run it like you're running from an angry mob:
```bash
docker run -d \
  --name swamp-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN=your_magical_token_here \
  ghcr.io/swamp-netizens/discord-bot:main
```

### 🗺️ Using Nomad (The Far Far Far Away Way)

1. Store your magical token on the Nomad server (like hiding Fiona in the tower):
   ```bash
   sudo mkdir -p /etc/discord
   echo "your_magical_token" | sudo tee /etc/discord/token
   sudo chmod 600 /etc/discord/token
   ```

2. Deploy your bot (like sending Donkey on a mission):
   ```bash
   nomad job run swamp-bot.nomad
   ```

3. Check if everything's working (like checking if your swamp is still yours):
   ```bash
   nomad status swamp-discord-bot
   ```

The Nomad configuration is like Shrek's perfect swamp setup:
- Keeps your token safe (like Dragon guards the castle)
- Automatically restarts (like Shrek's determination to get his swamp back)
- Uses minimal resources (leaves plenty of room for the fairytale creatures)
- Always gets the latest version (fresher than morning waffles)

## 🏗️ CI/CD (Continuous Integration / Continuous Donkey)

Our magical GitHub Actions workflow (more reliable than Fairy Godmother's potions):
- Builds faster than Gingy can run
- Pushes images automatically (like ejecting fairytale creatures from the swamp)
- Tags everything properly (better organized than Lord Farquaad's kingdom)

To use the GitHub Container Registry (the Royal Package Storage):
1. Make sure your kingdom (repository) has the right permissions
2. Get your special key (PAT) with `packages:read` access
3. Images are public by default (like an All Star song)

Remember: This bot has LAYERS! 🧅