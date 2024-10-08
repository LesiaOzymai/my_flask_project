# Use a lightweight Python image
FROM python:3.11.3-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies inside the container
RUN python -m pip install -r requirements.txt

# Copy all project files into the container
COPY . /app

# Define the command to run the Flask application
CMD flask --app myapp run -h 0.0.0.0 -p $PORT