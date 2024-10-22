Here’s the updated `README.md` reflecting the app's name, **Flask IP Blocklist Checker**:

```markdown
# Flask IP Blocklist Checker

## Overview

Flask IP Blocklist Checker is a lightweight web application designed to check if specified IP addresses are listed on common DNS-based blacklists (DNSBLs). It assists system administrators and network operators in monitoring and managing IP addresses that may be blacklisted, ensuring better email deliverability and overall network integrity.

## Features

- **IP Address Monitoring**: Check a list of specified IP addresses against popular DNSBLs.
- **Web Interface**: User-friendly web interface to display monitoring results.
- **Automatic Updates**: The app automatically refreshes its results every couple of hours.
- **Customizable IP List**: Easily modify the list of IP addresses to monitor by editing the `ip_address.txt` file.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework for Python.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX, used to run the application in production.
- **Docker**: Containerization platform for packaging the application and its dependencies.
- **Pydnsbl**: A Python library for checking DNS-based blacklists.

## Installation

To set up the Flask IP Blocklist Checker, follow these steps:

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

## Usage

- Navigate to `http://127.0.0.1:5000` in your web browser.
- The application will display the results of the IP address checks, showing whether each IP is blacklisted or not.
- You can force a recheck by clicking the "Recheck" button.

## Docker Setup

To run the application in a Docker container, follow these steps:

1. **Build the Docker image**:
   ```bash
   docker build -t flask-ip-blocklist-checker .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8000:8000 flask-ip-blocklist-checker
   ```

   The application will be accessible at `http://localhost:8000`.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
