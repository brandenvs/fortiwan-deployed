// Implements Toast Updates
function alertMsg(title, text, alertType, delay) {
    const toast = document.getElementById('liveToast');
    const toastTitle = document.getElementById('toast-title');
    const toastText = document.getElementById('toast-text');

    toastTitle.innerText = title;
    toastText.innerText = text;
    if (alertType == 'info') {
        toast.classList.add('text-info')
        toast.classList.add('bg-info-subtle')

        toast.classList.remove('text-success')
        toast.classList.remove('bg-success-subtle')
        toast.classList.remove('text-danger')
        toast.classList.remove('bg-danger-subtle')
    } else if (alertType == 'success') {
        toast.classList.add('text-success')
        toast.classList.add('bg-success-subtle')

        toast.classList.remove('text-info')
        toast.classList.remove('bg-info-subtle')
        toast.classList.remove('text-danger')
        toast.classList.remove('bg-danger-subtle')
    } else if (alertType == 'error') {
        toast.classList.add('text-danger')
        toast.classList.add('bg-danger-subtle')

        toast.classList.remove('text-info')
        toast.classList.remove('bg-info-subtle')
        toast.classList.remove('text-success')
        toast.classList.remove('bg-success-subtle')
    }

    // Create and show the toast
    const toastBootstrap = new bootstrap.Toast(toast, { delay: delay });
    return toastBootstrap
}