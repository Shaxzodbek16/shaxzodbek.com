document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    const formGroups = document.querySelectorAll('.form-group');
    const successMessage = document.querySelector('.success-message');

    formGroups.forEach((group, index) => {
        setTimeout(() => {
            group.classList.add('animate');
        }, index * 150);
    });

    // Form validation and submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let isValid = true;

        // Validate each input
        form.querySelectorAll('input, textarea').forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('error');

                // Remove error class after animation
                setTimeout(() => {
                    input.classList.remove('error');
                }, 500);
            }
        });

        if (isValid) {
            // Hide form and show success message
            form.style.display = 'none';
            successMessage.classList.add('show');
        }
    });

    // Remove error state on input
    form.querySelectorAll('input, textarea').forEach(input => {
        input.addEventListener('input', () => {
            input.classList.remove('error');
        });
    });
});
const hamburger = document.querySelector('.hamburger');
const links = document.querySelector('.links');
const login = document.querySelector('.login');
const navLinks = document.querySelectorAll('.links a');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    links.classList.toggle('active');
    login.classList.toggle('active');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        links.classList.remove('active');
        login.classList.remove('active');
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!links.contains(e.target) && !hamburger.contains(e.target) && !login.contains(e.target)) {
        hamburger.classList.remove('active');
        links.classList.remove('active');
        login.classList.remove('active');
    }
});

document.querySelectorAll('.videos__card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});
document.addEventListener('DOMContentLoaded', () => {
    // Animate cards on scroll
    const cards = document.querySelectorAll('.book__card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});