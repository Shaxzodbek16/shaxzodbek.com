document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function () {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bx-show');
                icon.classList.add('bx-hide');
            } else {
                input.type = 'password';
                icon.classList.remove('bx-hide');
                icon.classList.add('bx-show');
            }
        });
    });
    const password1Input = document.getElementById('password1');
    if (password1Input) {
        password1Input.addEventListener('input', validatePassword);
    }

    function validatePassword() {
        const password = password1Input.value;
        const requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /[0-9]/.test(password)
        };

        Object.entries(requirements).forEach(([requirement, isValid]) => {
            const li = document.querySelector(`[data-requirement="${requirement}"]`);
            if (li) {
                li.classList.toggle('valid', isValid);
            }
        });
    }

    const form = document.querySelector('.reset-form');
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
        const password1 = document.getElementById('password1')?.value;
        const password2 = document.getElementById('password2')?.value;

        if (password1 && password2 && password1 !== password2) {
            e.preventDefault();
            alert('Passwords do not match!');
            return;
        }

        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="bx bx-loader-alt bx-spin"></i> Processing...';
    });
});