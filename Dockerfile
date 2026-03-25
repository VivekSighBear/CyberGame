FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry (no virtualenv inside container)
RUN poetry config virtualenvs.create false

# Copy only dependency files first (for caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy rest of code
COPY . .

# Expose port (if Streamlit)
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]