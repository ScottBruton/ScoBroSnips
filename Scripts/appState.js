// appState.js
const appState = {
    buttonsEnabled: {
        extractButton: true,
        copyImageButton: true,
        copyObjectButton: false,
        selectAllButton: false,
        selectButton: false
    },
    enableButtonsAfterExtract() {
        this.buttonsEnabled.copyObjectButton = true;
        this.buttonsEnabled.selectAllButton = true;
        this.buttonsEnabled.selectButton = true;
    }
};

export default appState;
