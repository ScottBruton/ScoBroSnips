# appStateFunctions.py

capturedImage = None 
enabledTool = None
extractedEdgesOverlay = None 
selectedObjects = []
objectsFound = []
minimizedToTray = False  # Corrected to uppercase 'False'

def update_captured_image(image):
    global capturedImage
    capturedImage = image  # Update captured image in appState
