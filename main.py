import webview
import threading
import http.server
import socketserver
import os

# Automatically find the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = BASE_DIR # Path to SCOBROSNIPS folder

# Set the port for the local server
PORT = 8000

# Step 1: Create a function to start a local server
def start_server():
    # Check if DIRECTORY exists
    if not os.path.exists(DIRECTORY):
        print(f"Directory '{DIRECTORY}' does not exist. Please check the path.")
        exit(1)  # Exit if the directory doesn't exist

    os.chdir(DIRECTORY)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

# Step 2: Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Ensures it exits when the main program exits
server_thread.start()

# Step 3: Open the HTML interface in PyWebView
webview.create_window('ScoBro Snips', f'http://localhost:{PORT}/home.html', width=800, height=600)
webview.start()
