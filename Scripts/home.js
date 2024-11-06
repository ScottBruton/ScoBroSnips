// Function to display snipped image in the main content area
window.onload = function () {
  // Ensure displaySnippedImage is exposed to Python
  function displaySnippedImage(imageData) {
    console.log("displaySnippedImage called");
    const contentArea = document.getElementById("mainContent");
    if (!contentArea) {
      console.error("mainContent element not found!");
      return;
    }

    const img = new Image();
    img.src = imageData;
    contentArea.innerHTML = "";
    contentArea.appendChild(img);
  }

  // Expose displaySnippedImage to Python using Eel
  if (typeof eel !== "undefined") {
    eel.expose(displaySnippedImage);
  } else {
    console.error("Eel is not defined. Make sure eel.js is loaded correctly.");
  }
};

// Example function for handling button click
function copyImage() {
  if (typeof eel !== "undefined") {
    eel.copy_image(); // Calls Python function named `copy_image`
  } else {
    console.error("Eel is not defined. Make sure eel.js is loaded correctly.");
  }
}

// Add event listeners to buttons
document.querySelectorAll(".icon-button").forEach((button, index) => {
  button.addEventListener("click", () => {
    console.log(`Button ${index + 1} clicked`);
    // Add individual actions based on index or button text here
  });
});
