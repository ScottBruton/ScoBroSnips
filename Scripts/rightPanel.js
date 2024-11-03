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

 const firstMarkerOffset = 10; // Starting position of the first marker, 10px from the top
const totalMarkers = 10;
const thumbHeight = 10; // Adjust based on half the thumb's total height

for (let i = 0; i < totalMarkers; i++) {
    const marker = document.createElement('div');
    marker.className = 'slider-marker';

    // Calculate marker position with the first marker at 10px from the top and evenly spaced down
    const markerPosition = `calc(${firstMarkerOffset}px + ${(i / (totalMarkers - 1)) * (100 - firstMarkerOffset + 5.5)}%)`;
    marker.style.top = markerPosition;

    sliderTrack.appendChild(marker);
}
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

    // Initial value
    let initialValue = 1;
    updateSliderValue(initialValue);

    // Handle dragging of the slider thumb
    let isDragging = false;

    sliderThumb.addEventListener('mousedown', () => {
        isDragging = true;
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });

    function onMouseMove(event) {
        if (isDragging) {
            const sliderRect = sliderTrack.getBoundingClientRect();
            let newTop = event.clientY - sliderRect.top;

            // Constrain to bounds and calculate nearest snap point
            newTop = Math.max(0, Math.min(newTop, sliderRect.height - sliderThumb.offsetHeight));
            const snapValue = Math.round((newTop / (sliderRect.height - sliderThumb.offsetHeight)) * 9) + 1;
            const snapTop = ((snapValue - 1) / 9) * (sliderRect.height - sliderThumb.offsetHeight);

            // Update thumb, progress, and value display
            sliderThumb.style.top = `${snapTop}px`;
            sliderProgress.style.height = `${snapTop + sliderThumb.offsetHeight / 2}px`;
            sliderProgress.style.top = "0px";
            valueDisplay.textContent = `${snapValue}px`;
        }
    }

    function onMouseUp() {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }

    function updateSliderValue(value) {
        const sliderRect = sliderTrack.getBoundingClientRect();
        const maxTop = sliderRect.height - sliderThumb.offsetHeight;
        const newTop = ((value - 1) / 9) * maxTop;

        sliderThumb.style.top = `${newTop}px`;
        sliderProgress.style.height = `${newTop + sliderThumb.offsetHeight / 2}px`;
        sliderProgress.style.top = "0px";
        valueDisplay.textContent = `${value}px`;
    }
}

// Initialize the custom slider and title when the page loads
document.addEventListener('DOMContentLoaded', () => {
    showEdgeThicknessSlider();
});
