const appState = {
    buttonsEnabled: {
        extractButton: true,
        copyImageButton: true,
        copyObjectButton: false,
        selectAllButton: false,
        selectButton: false
    },
    capturedImage: null, // Holds the snippet that the user takes
    enabledTool: null, // Indicates which tool has been selected
    extractedEdgesOverlay: null, // Holds the extracted edges from the image
    selectedObjects: [], // The objects that the user selects
    objectsFound: [], // All objects found within the image
    minimizedToTray: false, // Indicates if the app is minimized to the tray

    enableButtonsAfterExtract() {
        this.buttonsEnabled.copyObjectButton = true;
        this.buttonsEnabled.selectAllButton = true;
        this.buttonsEnabled.selectButton = true;
    },

    setMinimizedState(minimized) {
        this.minimizedToTray = minimized;
    }
};

export default appState;
