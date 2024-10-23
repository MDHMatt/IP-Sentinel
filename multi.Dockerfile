# Set the Python version and major version as build arguments
ARG PYTHON_VERSION=3.12-slim
ARG PYTHON_MAJOR_VERSION=3.12

# Stage 1: Build the Flask app in a temporary container
FROM python:${PYTHON_VERSION} AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Create the final runtime image
FROM python:${PYTHON_VERSION}

# Set working directory
WORKDIR /app

# Install Gunicorn in the final image
RUN pip install --no-cache-dir gunicorn

# Copy the entire lib directory from the builder stage
COPY --from=builder /usr/local/lib/ /usr/local/lib/

#COPY --from=builder ${SITE_PACKAGES_PATH} ${SITE_PACKAGES_PATH}
COPY --from=builder /app/app /app

# # Copy only the essential parts from the builder stage
# COPY --from=builder /usr/local/lib/python${PYTHON_MAJOR_VERSION}*/site-packages /usr/local/lib/python${PYTHON_MAJOR_VERSION}*/site-packages
# COPY --from=builder /app/app /app

# Expose the application port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "check_ips:app"]
