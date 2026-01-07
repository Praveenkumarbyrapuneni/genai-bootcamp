# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Set PYTHONPATH so imports work correctly
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Start command - use api.main since that's where the working code is
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
