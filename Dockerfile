FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ffmpeg curl unzip gcc python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://deno.land/install.sh | sh && \
    ln -s /root/.deno/bin/deno /usr/local/bin/deno

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose port for web server
EXPOSE 8080

# Run the bot
CMD ["python3", "-m", "AnnieXMedia"]
