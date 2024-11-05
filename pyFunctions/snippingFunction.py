import ctypes
import time
import cv2
import numpy as np
from PIL import ImageGrab
import eel
import threading
import tkinter as tk
from pyFunctions.appStateFunctions import update_captured_image
import base64
from io import BytesIO



# Set DPI awareness to handle high DPI scaling
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Global variables to store the original images
global original_image
global original_snippet_image

# Snipping function using Tkinter
def select_area():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.config(bg="black")
    root.after(10, lambda: root.focus_force())  # Bring the window to the foreground after a short delay
    start_x = start_y = end_x = end_y = 0
    rect = None

    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect
        start_x = event.x_root
        start_y = event.y_root
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_mouse_drag(event):
        nonlocal rect, end_x, end_y
        end_x = event.x_root
        end_y = event.y_root
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red", width=2)

    def on_mouse_up(event):
        root.quit()
        root.destroy()
        capture_selected_area(start_x, start_y, end_x, end_y)

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

# Capture the selected area and convert it to OpenCV format


def capture_selected_area(x1, y1, x2, y2):
    # Ensure the coordinates are in the correct order
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    # Add a small delay to ensure the screen is properly updated before capture
    time.sleep(0.2)

    # Grab the selected screen area
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2)).convert("RGBA")
    global original_snippet_image
    original_snippet_image = image

    # Convert the image to an OpenCV format
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
    global original_image
    original_image = open_cv_image.copy()

    # Convert image to base64 data URL
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_data = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

    print("Calling displaySnippedImage with image data...")
    time.sleep(1)
    eel.displaySnippedImage(image_data)

# Eel function to call the snipping tool
def start_snipping_tool():
    threading.Thread(target=select_area, daemon=True).start()

# External function to trigger the snipping tool
def trigger_snipping_tool():
    start_snipping_tool()
