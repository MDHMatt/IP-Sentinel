import os
import time
import ipaddress
import logging
from datetime import datetime
from threading import Thread
from pydnsbl import DNSBLIpChecker
from flask import Flask, render_template, jsonify
from logging.handlers import RotatingFileHandler

# Path to the configuration files
ip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'ip_addresses.txt')

# Define the log file path in the same directory as the config
log_file_path = os.path.join(os.path.dirname(ip_file_path), 'ip_checker.log')

# Set up log rotation
handler = RotatingFileHandler(log_file_path, maxBytes=2000, backupCount=3)  # 5 MB per file, 3 backups

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler]
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Log to a file in the same directory as config
        logging.StreamHandler()  # Also log to console
    ]
)

# Initialize Flask app
app = Flask(__name__)

# Create the DNSBLIpChecker instance using the built-in blocklists
checker = DNSBLIpChecker()

# Global variables to store the results, last run time, and errors
results = []
last_run_time = None
errors = []  # To hold any invalid IP errors

def load_ip_addresses(file_path):
    """Load IP addresses from the specified text file."""
    try:
        with open(file_path, 'r') as file:
            ip_addresses = [line.strip() for line in file if line.strip()]
            return ip_addresses
    except FileNotFoundError as e:
        logging.error(f"Error loading IP addresses file: {e}")
        return []

def is_valid_ip(ip):
    """Validate if the provided IP address is valid (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def check_ip_in_dnsbl(ip):
    """Checks if the IP is listed in any DNS-based blacklist."""
    result = checker.check(ip)  # Check IP using built-in blocklists
    return result

def update_results():
    """Updates the results of the IP check and stores them globally."""
    global results, last_run_time, errors
    
    # Reload the IP addresses from the file each time this function is called
    ip_addresses = load_ip_addresses(ip_file_path)

    results = []
    errors = []  # Reset errors for new check
    
    for ip in ip_addresses:
        if is_valid_ip(ip):
            result = check_ip_in_dnsbl(ip)  # Check IP
            if result.blacklisted:
                blacklist_info = {
                    'ip': ip,
                    'status': 'BLACKLISTED',
                    'details': [bl for bl in result.detected_by]
                }
                logging.info(f"{ip} is BLACKLISTED. Detected by: {', '.join(blacklist_info['details'])}")
            else:
                blacklist_info = {
                    'ip': ip,
                    'status': 'CLEAN',
                    'details': []
                }
                logging.info(f"{ip} is CLEAN.")
            results.append(blacklist_info)
        else:
            errors.append(f"{ip} is an invalid IP address.")
            logging.warning(f"Invalid IP address: {ip}")

    # Update the last run time
    last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info("IP check completed.")

def periodic_update(interval=3600):
    """Periodically updates the results every `interval` seconds."""
    while True:
        update_results()
        time.sleep(interval)

# Start the periodic update in a separate thread
thread = Thread(target=periodic_update)
thread.daemon = True
thread.start()

@app.route('/')
def home():
    """Serve the webpage with the current results, last run time, and errors."""
    return render_template('index.html', results=results, last_run_time=last_run_time, errors=errors)

@app.route('/recheck', methods=['POST'])
def recheck():
    """Force a recheck of all IPs, reload the IP list, and return JSON response."""
    update_results()
    return jsonify({
        'message': 'IPs rechecked',
        'status': 'success',
        'last_run_time': last_run_time,
        'errors': errors
    })

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000)
