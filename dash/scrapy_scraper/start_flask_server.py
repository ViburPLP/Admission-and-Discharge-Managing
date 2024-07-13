import subprocess
import time
import requests

def start_flask_server():
    try:
        # Try to get the response from the Flask server to check if it's already running
        response = requests.get('http://localhost:5000')
        if response.status_code == 200:
            print("Flask server is already running.")
            return
    except requests.ConnectionError:
        pass

    # Start the Flask server
    print("Starting Flask server...")
    subprocess.Popen(['python', 'C:/Users/Victor/Documents/Scraper/Localscraper/dash/scrapy_scraper/trigger_scrapy.py'])
    time.sleep(3) #time to start the server

if __name__ == '__main__':
    start_flask_server()
