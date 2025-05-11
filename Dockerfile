# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_SECRET_KEY=supersecret \
    DB_HOST=your-db-host-ip \
    DB_NAME=project1_db \
    DB_USER=postgres \
    DB_PASS=1234

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port your Flask app runs on (updated to 80)
EXPOSE 80

# Run the Flask app
CMD ["python", "app.py"]
