# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy the .env file into the container at /app
COPY .env .env

# Expose the Flask port
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
