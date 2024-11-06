import eel 
import webview
import threading
import http.server
import socketserver
import shutil 
import os
import wx
import wx.adv
import traceback
from PIL import Image
import keyboard
from pyFunctions.snippingFunction import snipping_tool_function
from pyFunctions.appStateFunctions import save_captured_image, get_captured_image
from pathlib import Path  

# Initialize Eel with the directory containing HTML files
eel.init(".")  # Assuming the HTML files are in the root directory

# Ensure eel.js is available in the project directory
def ensure_eel_js_exists():
    eel_js_source = Path(eel.__file__).parent / 'eel.js'
    eel_js_target = Path('.') / 'eel.js'
    if not eel_js_target.exists():
        try:
            shutil.copy(eel_js_source, eel_js_target)
            print("Copied eel.js to project directory.")
        except Exception as e:
            print("Error copying eel.js:", e)
            traceback.print_exc()

ensure_eel_js_exists()

# Function to handle snipping tool hotkey event
def on_snipping_hotkey():
    snipped_image = snipping_tool_function()
    if snipped_image is None:
        print("Error: No image captured.")
        return
    save_captured_image(snipped_image)
    eel.show_snipped_image()()  # Calls JavaScript function in home.js

@eel.expose
def get_snipped_image_data():
    return get_captured_image()

@eel.expose
def test_function():
    print("test_function called from JavaScript")

# Function to listen for the hotkey
def hotkey_listener():
    keyboard.add_hotkey('ctrl+alt+s', on_snipping_hotkey)

# Automatically find the directory where this script is located
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DIRECTORY = BASE_DIR  # Path to SCOBROSNIPS folder
except Exception as e:
    print("Error determining base directory:", e)
    traceback.print_exc()
    exit(1)

# Set the port for the local server
PORT = 8000

# Define the path to the tray icon
ICON_PATH = os.path.join(BASE_DIR, "Media", "icons", "trayIcon.ico")

# Define an API for PyWebView to use
class API:
    def __init__(self):
        self.minimizedToTray = True

    def my_python_function(self, value):
        print(f"Python function called with value: {value}")
        return f"Hello from Python! Received value: {value}"

    def set_minimized_state(self, minimized):
        self.minimizedToTray = minimized

    def get_minimized_state(self):
        return self.minimizedToTray

api = API()

# Function to start a local server
def start_server():
    try:
        if not os.path.exists(DIRECTORY):
            print(f"Directory '{DIRECTORY}' does not exist. Please check the path.")
            exit(1)

        os.chdir(DIRECTORY)
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), handler)
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
    except Exception as e:
        print("Error starting local server:", e)
        traceback.print_exc()
        exit(1)

# Initialize the PyWebView window
window = None

def create_window():
    global window
    try:
        window = webview.create_window(
            'ScoBro Snips', f'http://localhost:{PORT}/home.html',
            js_api=api, width=800, height=600, hidden=True  # Start hidden
        )
    except Exception as e:
        print("Error creating PyWebView window:", e)
        traceback.print_exc()

# Function to handle show/hide based on tray icon click
def toggle_window():
    try:
        minimized = api.get_minimized_state()
        if minimized:
            print("Showing window")
            window.show()
            api.set_minimized_state(False)
        else:
            print("Hiding window")
            window.hide()
            api.set_minimized_state(True)
    except Exception as e:
        print("Error toggling window visibility:", e)
        traceback.print_exc()

# Function to exit the app cleanly
def exit_app():
    if window:
        window.destroy()
    wx.CallAfter(wx.GetApp().ExitMainLoop)

# wxPython App and TaskBarIcon for System Tray
def setup_tray_icon_wx(app):
    class TaskBarIcon(wx.adv.TaskBarIcon):
        TBMENU_SHOW_HIDE = wx.NewIdRef()
        TBMENU_EXIT = wx.NewIdRef()

        def __init__(self, frame):
            super(TaskBarIcon, self).__init__()
            self.frame = frame
            try:
                # Set the icon
                icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
                self.SetIcon(icon, "ScoBro Snips")
            except Exception as e:
                print("Error setting tray icon:", e)
                traceback.print_exc()

            # Bind events
            self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_double_click)
            self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_right_click)

        def CreatePopupMenu(self):
            menu = wx.Menu()
            menu.Append(self.TBMENU_SHOW_HIDE, "Show/Hide")
            menu.AppendSeparator()
            menu.Append(self.TBMENU_EXIT, "Exit")
            self.Bind(wx.EVT_MENU, self.on_toggle_window, id=self.TBMENU_SHOW_HIDE)
            self.Bind(wx.EVT_MENU, self.on_exit, id=self.TBMENU_EXIT)
            return menu

        def on_left_double_click(self, event):
            self.on_toggle_window(event)

        def on_right_click(self, event):
            self.PopupMenu(self.CreatePopupMenu())

        def on_toggle_window(self, event):
            toggle_window()

        def on_exit(self, event):
            exit_app()

    frame = wx.Frame(None)
    TaskBarIcon(frame)

# Main application setup
if __name__ == "__main__":
    try:
        # Start local server thread
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()

        # Start hotkey listener thread
        hotkey_thread = threading.Thread(target=hotkey_listener)
        hotkey_thread.daemon = True
        hotkey_thread.start()

        # Initialize wx App and set up the tray icon
        app = wx.App(False)
        setup_tray_icon_wx(app)

        # Create the PyWebView window with debugging enabled
        create_window()

        # Start the PyWebView loop on the main thread with debugging
        webview.start(debug=True, gui='wx')

        # Start the wx main loop after webview is up
        app.MainLoop()

    except Exception as e:
        print("Error running the main application:", e)
        traceback.print_exc()
