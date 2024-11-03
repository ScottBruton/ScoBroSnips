// Example function for handling button click
function copyImage() {
    eel.copy_image()();  // Calls Python function named `copy_image`
}

// Add event listeners to buttons
document.querySelectorAll('.sidebar-btn').forEach((button, index) => {
    button.addEventListener('click', () => {
        console.log(`Button ${index + 1} clicked`);
        // You can add individual actions based on index or button text
    });
});
