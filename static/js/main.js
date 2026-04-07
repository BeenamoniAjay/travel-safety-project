document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form[action="/search"]');
    if (!form) {
        return;
    }

    form.addEventListener('submit', () => {
        const input = form.querySelector('input[name="city"]');
        if (input && input.value.trim() === '') {
            input.classList.add('is-invalid');
        }
    });
});
