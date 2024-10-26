# Flask IP Blocklist Checker

## Overview

Flask IP Blocklist Checker is a lightweight web application designed to check if specified IP addresses are listed on common DNS-based blacklists (DNSBLs). It assists system administrators and network operators in monitoring and managing IP addresses that may be blacklisted, ensuring better email deliverability and overall network integrity.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework for Python.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX, used to run the application in production.
- **Docker**: Containerization platform for packaging the application and its dependencies.
- **Pydnsbl**: A Python library for checking DNS-based blacklists.

## Features

- **DNSBL IP Checking**: Automatically checks IP addresses against popular DNS-based blacklists.
- **Dynamic IP List Updates**: By mounting the `config` directory, you can update the IP list file dynamically without rebuilding the container.
- **Automatic Updates**: The app automatically refreshes its results every couple of hours.
- **Customizable IP List**: Easily modify the list of IP addresses to monitor by editing the `ip_address.txt` file.
- **Log Rotation**: Maintains logs with rotation, ensuring efficient storage management.
- **Web Interface and REST API**: Displays results in a simple web interface and allows for manual rechecking via API.

## Getting Started

### Prerequisites

- **Docker** (recommended for easy deployment)
- **Python 3.12+** (if running locally)

### Dependencies Overview

| Dependency | Description |
|------------|-------------|
| `aiodns` | Provides asynchronous DNS resolution for non-blocking DNS queries. |
| `blinker` | Manages signals for event handling, such as request start/finish in Flask. |
| `cffi` & `pycparser` | Support C Foreign Function Interface (FFI) for calling C libraries from Python. |
| `click` | Manages Flask's CLI commands. |
| `Flask` | The main framework for building the web application. |
| `gunicorn` | WSGI HTTP server used to run the Flask app in production. |
| `idna` | Supports encoding and decoding for internationalized domain names. |
| `itsdangerous` | Ensures secure data signing for session management. |
| `Jinja2` | Flask’s templating engine for rendering dynamic HTML. |
| `MarkupSafe` | Automatically escapes HTML/XML content for security. |
| `packaging` | Parses and compares versions, used by other libraries. |
| `pycares` | Advanced DNS functionality with asynchronous support. |
| `pydnsbl` | Core library for checking IPs against DNSBLs. |
| `Werkzeug` | Manages HTTP requests, routing, and debugging in Flask. |

### Usage with Python 3.12+

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/flask-ip-blocklist-checker.git
   cd flask-ip-blocklist-checker
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the IP addresses**:
   - Edit the `config/ip_address.txt` file to include the IP addresses you want to monitor. Each IP should be on a new line.

5. **Run the application**:
   ```bash
   flask run
   ```

   This will start the application on `http://127.0.0.1:5000`.

### Usage with Docker

Build the Docker image:
```bash
docker build -t mdhmatt/flask-ip-blocklist-checker .
```

Run the Docker container with a mounted configuration directory:
```bash
docker run -d -p 8000:8000 -v $(pwd)/config:/app/config mdhmatt/flask-ip-blocklist-checker
```

> **Note**: The `config` directory includes an `ip_addresses.txt` file where you can add, remove, or modify the IP addresses to be checked. Changes will be picked up dynamically by the app without requiring a rebuild.

### Configuration

- **IP Address List**: Add IPs to `config/ip_addresses.txt`. Each IP should be on a new line.
- **Log Location**: The application logs are saved in `config/ip_checker.log` with rotation enabled (up to three backups).

### Accessing the Application

- Web UI: Open [http://localhost:8000](http://localhost:8000) in your browser to view the current IP check results.
- API Endpoint: Recheck IPs by sending a `POST` request to `http://localhost:8000/recheck` or using the webgui button.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
