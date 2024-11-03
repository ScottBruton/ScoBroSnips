import appState from './appState.js';

document.addEventListener('DOMContentLoaded', () => {
    const extractButton = document.getElementById('extractButton');
    const copyImageButton = document.getElementById('copyImageButton');
    const copyObjectButton = document.getElementById('copyObjectButton');
    const selectAllButton = document.getElementById('selectAllButton');
    const selectButton = document.getElementById('selectButton');

    // Initialize buttons based on state
    function initializeButtons() {
        extractButton.disabled = !appState.buttonsEnabled.extractButton;
        copyImageButton.disabled = !appState.buttonsEnabled.copyImageButton;

        // Set initial visibility and fade-in classes
        if (!appState.buttonsEnabled.copyObjectButton) copyObjectButton.classList.add('hidden');
        if (!appState.buttonsEnabled.selectAllButton) selectAllButton.classList.add('hidden');
        if (!appState.buttonsEnabled.selectButton) selectButton.classList.add('hidden');
    }

    // Function to show buttons with fade-in effect
    function showButtonsWithFadeIn() {
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
    }

    // Add event listener to Extract Objects button
    extractButton.addEventListener('click', () => {
        console.log("Extract Objects button clicked!");
        showButtonsWithFadeIn();
    });

    initializeButtons();
});
