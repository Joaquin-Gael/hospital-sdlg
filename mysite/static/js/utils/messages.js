export var successMessage = (message) => {
    const toastHtml = `
    <div class="toast fade show toast-custom" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true">
        <div class="toast-header bg-success text-white">
            <i class="fa-solid fa-circle-check me-2"></i>
            <strong class="me-auto">Success</strong>
            <small>52s</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    </div>
    `;

    document.getElementById("response").innerHTML += toastHtml;

    const toastElement = document.querySelector('.toast-custom:last-child');

    setTimeout(() => {
        const toast = new bootstrap.Toast(toastElement);
        toast.hide();
    }, 5000);
};

export var errorMessage = (message) => {
    const toastHtml = `
    <div class="toast fade show toast-custom" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true">
        <div class="toast-header bg-danger text-white">
            <i class="fa-solid fa-circle-exclamation me-2"></i>
            <strong class="me-auto">Error</strong>
            <small>52s</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    </div>
    `;

    document.getElementById("response").innerHTML += toastHtml;

    const toastElement = document.querySelector('.toast-custom:last-child');

    setTimeout(() => {
        const toast = new bootstrap.Toast(toastElement);
        toast.hide();
    }, 5000);
};