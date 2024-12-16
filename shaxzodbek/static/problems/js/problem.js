const hints = document.querySelectorAll('.hint');
hints.forEach(hint => {
    const header = hint.querySelector('.hint-header');
    header.addEventListener('click', () => {
        hint.classList.toggle('active');
        const icon = hint.querySelector('.fas');
        icon.style.transform = hint.classList.contains('active') ? 'rotate(180deg)' : 'rotate(0)';
    });
});

const tabs = document.querySelectorAll('.tab');
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
    });
});

const examples = document.querySelectorAll('.example');
examples.forEach((example, index) => {
    example.style.opacity = '0';
    example.style.animation = `fadeIn 0.5s ease ${index * 0.2}s forwards`;
});