import base64
from io import BytesIO
from PIL import Image

# Global variable to store captured image data
captured_image = None

# Function to update the captured image in memory
def save_captured_image(image):
    global captured_image
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    captured_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    print("Captured image updated.")

# Function to retrieve the captured image in base64 format
def get_captured_image():
    if captured_image is None:
        print("No image captured yet.")
        return None
    return f"data:image/png;base64,{captured_image}"

# Additional functions for managing application state can go here
# For example, functions to handle other image transformations, state updates, etc.
