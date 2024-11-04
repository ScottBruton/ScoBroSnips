import webview
import threading
import http.server
import socketserver
import os
import win32api
import win32con
import win32gui
import ctypes
from PIL import Image

# Automatically find the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = BASE_DIR  # Path to SCOBROSNIPS folder

# Set the port for the local server
PORT = 8000

# Define the path to the tray icon
ICON_PATH = os.path.join(BASE_DIR, "Media", "icons", "trayIcon.ico")

# Python function to be exposed to JavaScript
class API:
    def __init__(self):
        self.minimizedToTray = True  # Start minimized by default

    def my_python_function(self, value):
        print(f"Python function called with value: {value}")
        return f"Hello from Python! Received value: {value}"

    def set_minimized_state(self, minimized):
        """Updates the minimizedToTray state."""
        self.minimizedToTray = minimized

    def get_minimized_state(self):
        """Returns the current minimized state."""
        return self.minimizedToTray

api = API()

# Function to start a local server
def start_server():
    if not os.path.exists(DIRECTORY):
        print(f"Directory '{DIRECTORY}' does not exist. Please check the path.")
        exit(1)

    os.chdir(DIRECTORY)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

# Initialize the PyWebView window
window = None

def create_window():
    global window
    window = webview.create_window(
        'ScoBro Snips', f'http://localhost:{PORT}/home.html',
        js_api=api, width=800, height=600, hidden=True  # Start hidden
    )

# Function to handle show/hide based on tray icon click
def toggle_window():
    minimized = api.get_minimized_state()
    if minimized:
        print("Showing window")  # Debug print
        window.show()
        api.set_minimized_state(False)
    else:
        print("Hiding window")  # Debug print
        window.hide()
        api.set_minimized_state(True)

# Function to exit the app cleanly
def exit_app():
    if window:
        window.destroy()
    os._exit(0)  # Stop the application completely

# Windows Tray Icon setup using win32api and win32gui
def setup_tray_icon_win32():
    def on_notify(hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:
            toggle_window()  # Trigger show/hide on double-click
            return 0  # Return 0 explicitly after handling double-click
        elif lparam == win32con.WM_RBUTTONUP:
            # Show context menu on right-click
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "Show/Hide")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "Exit")

            pos = win32gui.GetCursorPos()
            print(f"Right-click detected. Cursor position: {pos}")  # Debug print
            win32gui.SetForegroundWindow(hwnd)  # Bring tray icon to the foreground

            # TrackPopupMenu with additional focus handling
            result = win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN | win32con.TPM_RETURNCMD | win32con.TPM_RIGHTBUTTON, pos[0], pos[1], 0, hwnd, None)
            print(f"TrackPopupMenu result: {result}")  # Debug print
            if result == 1023:
                toggle_window()
            elif result == 1024:
                exit_app()
            win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)
            win32gui.DestroyMenu(menu)  # Clean up menu after use
            return 0  # Return 0 after handling right-click menu

        return 0  # Ensure 0 is returned by default

    # Load icon
    wc = win32gui.WNDCLASS()
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "TrayIconClass"
    wc.lpfnWndProc = on_notify  # Assign the notification handler
    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(class_atom, "TrayIconWindow", 0, 0, 0, 0, 0, 0, 0, 0, None)

    # Add the icon to the system tray
    icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
    hicon = win32gui.LoadImage(0, ICON_PATH, win32con.IMAGE_ICON, 0, 0, icon_flags)
    nid = (hwnd, 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP, win32con.WM_USER + 20, hicon, "ScoBro Snips")
    win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    win32gui.PumpMessages()  # Start the message loop for tray icon

# Run the application
if __name__ == "__main__":
    # Start the local server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Set up and start the win32 tray icon in a separate thread
    tray_thread_win32 = threading.Thread(target=setup_tray_icon_win32)
    tray_thread_win32.daemon = True
    tray_thread_win32.start()

    # Create the PyWebView window, initially hidden
    create_window()
    webview.start()
