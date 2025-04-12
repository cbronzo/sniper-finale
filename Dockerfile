# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your source code into the container
COPY . /app

# Expose the port your Flask app runs on
EXPOSE 8000

# Run your app
CMD ["python", "app.py"]
