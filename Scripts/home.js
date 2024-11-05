// Function to display snipped image in the main content area
window.onload = function() {
    function displaySnippedImage(imageData) {
        console.log("displaySnippedImage called");  // Log when the function is called
        console.log("Received image data:", imageData);  // Log the image data to verify format

        const contentArea = document.getElementById('mainContent');
        if (!contentArea) {
            console.error("mainContent element not found!");  // Log an error if the element isn't found
            return;
        }

        const img = new Image();
        img.src = imageData;  // Expecting imageData to be a data URL (e.g., base64 encoded PNG)
        img.onload = () => console.log("Image loaded successfully");  // Confirm when image loads successfully
        img.onerror = (error) => console.error("Error loading image:", error);  // Log any loading errors

        contentArea.innerHTML = '';  // Clear previous content
        contentArea.appendChild(img);  // Insert the new image
    }

    // Expose displaySnippedImage to Eel so it can be called from Python
    if (typeof eel !== 'undefined') {
        eel.expose(displaySnippedImage);
    } else {
        console.error("Eel is not defined. Make sure eel.js is loaded correctly.");
    }
};

// Example function for handling button click
function copyImage() {
    if (typeof eel !== 'undefined') {
        eel.copy_image()();  // Calls Python function named `copy_image`
    } else {
        console.error("Eel is not defined. Make sure eel.js is loaded correctly.");
    }
}

// Add event listeners to buttons
document.querySelectorAll('.icon-button').forEach((button, index) => {
    button.addEventListener('click', () => {
        console.log(`Button ${index + 1} clicked`);
        // You can add individual actions based on index or button text
    });
});
