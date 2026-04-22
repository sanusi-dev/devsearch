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

// Run on initial page load
updateActiveNav();

// Run after every HTMX swap
document.addEventListener('htmx:afterSwap', updateActiveNav);

// Run on browser back/forward
window.addEventListener('popstate', updateActiveNav);





// Auto-dismiss toast messages after 4 seconds
document.addEventListener('htmx:afterSettle', function() {
    document.querySelectorAll('.toast').forEach(function(toast) {
        setTimeout(function() {
            toast.style.transition = 'opacity 0.5s, transform 0.5s';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(2rem)';
            setTimeout(function() { toast.remove(); }, 500);
        }, 4000);
    });
});
// Also run on initial page load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toast').forEach(function(toast) {
        setTimeout(function() {
            toast.style.transition = 'opacity 0.5s, transform 0.5s';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(2rem)';
            setTimeout(function() { toast.remove(); }, 500);
        }, 4000);
    });
});
