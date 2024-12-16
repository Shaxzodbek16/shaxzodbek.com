const searchInput = document.querySelector('.search-container input');
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const rows = tbody.querySelectorAll('tr');

    rows.forEach(row => {
        const title = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        if (title.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

const difficultySelect = document.querySelectorAll('.filter-select')[1];
difficultySelect.addEventListener('change', (e) => {
    const difficulty = e.target.value.toLowerCase();
    const rows = tbody.querySelectorAll('tr');

    rows.forEach(row => {
        const rowDifficulty = row.querySelector('.difficulty').textContent.toLowerCase();
        if (!difficulty || rowDifficulty === difficulty) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

const paginationButtons = document.querySelectorAll('.pagination button');
paginationButtons.forEach(button => {
    button.addEventListener('click', () => {
        if (!button.classList.contains('active') && !button.querySelector('i')) {
            paginationButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        }
    });
});