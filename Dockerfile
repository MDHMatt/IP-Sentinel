# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Set PYTHONPATH to include the installed dependencies
ENV PYTHONPATH=/app/dependencies

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app/check_ips.py

# Run the application
#CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app.check_ips:app"]
