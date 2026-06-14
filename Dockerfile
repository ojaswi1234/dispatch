FROM python:3.11-slim

# Create a non-root user
RUN useradd -m -s /bin/bash dispatch_user

WORKDIR /app

# Install system dependencies if required for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them first to leverage layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Set ownership
RUN chown -R dispatch_user:dispatch_user /app

USER dispatch_user

EXPOSE 8000

CMD ["gunicorn", "dispatch.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
