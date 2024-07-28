// messages.js
export var successMessage = (message) => {
    return `
    <div id="responceMsg" class="notification is-success">
        <button class="delete"></button>
        ${message}
    </div>
    `;
};

export var errorMessage = (message) => {
    return `
    <div id="responceMsg" class="notification is-danger">
        <button class="delete"></button>
        ${message}
    </div>
    `;
};
