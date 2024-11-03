import appState from './appState.js';

document.addEventListener('DOMContentLoaded', () => {
    const extractButton = document.getElementById('extractButton');
    const copyObjectButton = document.getElementById('copyObjectButton');
    const selectAllButton = document.getElementById('selectAllButton');
    const selectButton = document.getElementById('selectButton');

    // Check if elements are loaded
    if (!extractButton || !copyObjectButton || !selectAllButton || !selectButton) {
        console.error("One or more buttons not found.");
        return;
    }

    // Event listener for Extract Objects button
    extractButton.addEventListener('click', () => {
        console.log("Extract Objects button clicked!");

        // Hardcoded testing logic to set booleans to true and enable visibility
        appState.buttonsEnabled.copyObjectButton = true;
        appState.buttonsEnabled.selectAllButton = true;
        appState.buttonsEnabled.selectButton = true;

        // Show and animate other buttons
        [copyObjectButton, selectAllButton, selectButton].forEach(button => {
            button.classList.remove('hidden'); // Make them visible
            button.classList.add('fade-in'); // Apply fade-in animation
            button.disabled = false; // Enable the button
        });
    });
});
