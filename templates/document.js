document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const username = form.querySelector('input[name="username"]');
    const password = form.querySelector('input[name="password"]');
    const loginButton = form.querySelector('.login-button');

    function checkInputs() {
        loginButton.disabled =!(username.value.trim() && password.value.trim());
        loginButton.style.opacity = username.value.trim() && password.value.trim() ? '1' : '0.4';}
    username.addEventListener('input', checkInputs);
    password.addEventListener('input', checkInputs);
});
