# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in Docker
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY . /app


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


# Install Node.js 14.x and npm
EXPOSE 80

#Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
