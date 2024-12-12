  // Add hover animation to cards
  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-5px)';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
    });
  });

  // Add search functionality
  const searchInput = document.querySelector('.search-input');
  const cards = document.querySelectorAll('.card');

  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();

    cards.forEach(card => {
      const title = card.querySelector('.card-title').textContent.toLowerCase();
      const role = card.querySelector('.card-role').textContent.toLowerCase();
      const description = card.querySelector('.card-description').textContent.toLowerCase();

      if (title.includes(searchTerm) || role.includes(searchTerm) || description.includes(searchTerm)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });

  const paginationButtons = document.querySelectorAll('.pagination button');

  paginationButtons.forEach(button => {
    button.addEventListener('click', () => {
      paginationButtons.forEach(btn => btn.classList.remove('active'));
      if (!isNaN(button.textContent)) {
        button.classList.add('active');
      }
    });
  });