// Update active navigation link
function updateActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('nav a[href]').forEach(link => {
        const href = link.getAttribute('href');
        const isActive =
            href === path ||
            (href !== '/' && path.startsWith(href));

        link.classList.toggle('text-main', isActive);
        link.classList.toggle('font-bold', isActive);
        link.classList.toggle('text-white/70', !isActive);
        link.classList.toggle('font-normal', !isActive);
        link.classList.toggle('hover:text-white', !isActive);
    });
}





// SweetAlert2 Toast Mixin
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    width: 'auto',
    customClass: {
        popup: 'max-w-[400px]', // Ensure very long text still wraps
    },
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

// Function to show SweetAlert2 toasts
function showToast(message, tags) {
    let icon = 'info';
    if (tags.includes('success')) icon = 'success';
    if (tags.includes('error')) icon = 'error';
    if (tags.includes('warning')) icon = 'warning';
    if (tags.includes('info')) icon = 'info';

    Toast.fire({
        icon: icon,
        title: message
    });
}

// Function to process Django messages from the script tag
function processDjangoMessages() {
    const messagesEl = document.getElementById('django-messages');
    if (messagesEl) {
        try {
            const messages = JSON.parse(messagesEl.textContent);
            messages.forEach(msg => {
                showToast(msg.message, msg.tags);
            });
            // Clear messages after processing to prevent re-showing on back/forward
            messagesEl.remove();
        } catch (e) {
            console.error("Error parsing Django messages:", e);
        }
    }
}

// Listen for messages passed via HX-Trigger header from the server
document.body.addEventListener('messages', function(evt) {
    // HTMX passes the event payload in evt.detail.value or evt.detail
    const messages = evt.detail.value || evt.detail;
    if (Array.isArray(messages)) {
        messages.forEach(msg => {
            showToast(msg.message, msg.tags);
        });
    }
});

// Run on initial page load
processDjangoMessages();
updateActiveNav();

// Run after every HTMX swap
document.addEventListener('htmx:afterSwap', function(evt) {
    updateActiveNav();
    processDjangoMessages(); // Check for messages in swapped content
});

// Run on browser back/forward
window.addEventListener('popstate', function() {
    updateActiveNav();
    processDjangoMessages();
});

// Confirmation Utility for HTMX
window.confirmAction = function(element, options = {}) {
    const title = options.title || 'Are you sure?';
    const text = options.text || "You won't be able to revert this!";
    const icon = options.icon || 'warning';
    const confirmButtonText = options.confirmButtonText || 'Yes, delete it!';

    Swal.fire({
        title: title,
        text: text,
        icon: icon,
        showCancelButton: true,
        confirmButtonText: confirmButtonText,
        cancelButtonText: 'Cancel',
        buttonsStyling: false,
        customClass: {
            confirmButton: 'btn btn--main mx-[0.3rem]',
            cancelButton: 'btn btn--sub mx-[0.3rem]',
            actions: 'mt-[2rem]',
            popup: 'rounded-3xl p-[2rem]',
        },
        background: '#fff',
        color: '#545454',
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, trigger the HTMX request
            element.dispatchEvent(new Event('confirmed'));
        }
    });
};
