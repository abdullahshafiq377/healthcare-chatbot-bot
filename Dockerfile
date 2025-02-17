# Use an official Python image as the base
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy required files
COPY requirements.txt .
COPY app.py .
COPY .env .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000

# Start the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
