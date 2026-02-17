# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and model
COPY backend/ ./backend/

# Expose port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Set environment variable for Flask
ENV FLASK_APP=backend/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=7860

# Run with gunicorn for production (install if needed)
RUN pip install gunicorn

# Start the app
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "backend.app:app"]