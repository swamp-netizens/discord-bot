FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy source code
COPY src/ ./src/

# Run the bot
CMD ["poetry", "run", "python", "src/bot.py"] 