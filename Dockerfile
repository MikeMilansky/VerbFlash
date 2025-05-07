FROM python:3.12-slim

# Install dependencies
RUN pip install python-dotenv python-telegram-bot


# Copy files
COPY . /app/

# Set working directory
WORKDIR /app/

# Run the bot
CMD ["python", "main.py"]
