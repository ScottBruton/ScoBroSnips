function showEdgeThicknessSlider() {
    const rightPanel = document.getElementById('rightPanel');

    // Clear the panel content
    rightPanel.innerHTML = '';

    // Create and add the ScoBro Snips title
    const title = document.createElement('div');
    title.className = 'center-title';
    title.textContent = 'ScoBro Snips';
    rightPanel.appendChild(title);

    // Create and add the Edge Thickness label
    const label = document.createElement('div');
    label.className = 'slider-label';
    label.textContent = 'Edge Thickness';
    rightPanel.appendChild(label);

    // Create a container for the custom vertical slider
    const sliderContainer = document.createElement('div');
    sliderContainer.className = 'custom-vertical-slider';

    // Create the slider track
    const sliderTrack = document.createElement('div');
    sliderTrack.className = 'slider-track';
    sliderContainer.appendChild(sliderTrack);

    // Create the green progress element
    const sliderProgress = document.createElement('div');
    sliderProgress.className = 'slider-progress';
    sliderTrack.appendChild(sliderProgress);

    // Create the slider thumb
    const sliderThumb = document.createElement('div');
    sliderThumb.className = 'slider-thumb';
    sliderTrack.appendChild(sliderThumb);

    // Append the container to the panel
    rightPanel.appendChild(sliderContainer);

    // Create and add the value display
    const valueDisplay = document.createElement('div');
    valueDisplay.className = 'slider-value';
    valueDisplay.id = 'edgeThicknessValue';
    rightPanel.appendChild(valueDisplay);

    // Set initial value
    let initialValue = 1;
    let isDragging = false;

    // Update display with initial value
    updateSliderValue(initialValue);

    // Function to update the slider value display and position
    function updateSliderValue(value) {
        const sliderRect = sliderTrack.getBoundingClientRect();
        const maxTop = sliderRect.height - sliderThumb.offsetHeight;
        const newTop = ((value - 1) / 9) * maxTop;

        // Set the initial thumb and progress positions
        sliderThumb.style.top = `${newTop}px`;
        sliderProgress.style.height = `${newTop + sliderThumb.offsetHeight / 2}px`;
        sliderProgress.style.top = "0px";

        // Display value in pixels
        valueDisplay.textContent = `${value}px`;
    }

    // Event listener to start dragging
    sliderThumb.addEventListener('mousedown', (event) => {
        isDragging = true;
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });

    function onMouseMove(event) {
        if (isDragging) {
            // Calculate the new position of the slider thumb
            const sliderRect = sliderTrack.getBoundingClientRect();
            let newTop = event.clientY - sliderRect.top;

            // Constrain the thumb position within the track bounds
            newTop = Math.max(0, Math.min(newTop, sliderRect.height - sliderThumb.offsetHeight));

            // Calculate the slider value in the range 1 to 10 based on thumb position
            const sliderValue = Math.round((newTop / (sliderRect.height - sliderThumb.offsetHeight)) * 9) + 1;

            // Update thumb position, progress, and display
            sliderThumb.style.top = `${newTop}px`;
            sliderProgress.style.height = `${newTop + sliderThumb.offsetHeight / 2}px`;
            sliderProgress.style.top = "0px";
            valueDisplay.textContent = `${sliderValue}px`;  // Display in pixels
        }
    }

    function onMouseUp() {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }
}

// Initialize the custom slider and title when the page loads
document.addEventListener('DOMContentLoaded', () => {
    showEdgeThicknessSlider();
});
