  const searchInput = document.querySelector('.connections_search-container input');
  const connectionItems = document.querySelectorAll('.connections_item');

  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    connectionItems.forEach(item => {
      const name = item.querySelector('.connections_name').textContent.toLowerCase();
      const job = item.querySelector('.connections_job').textContent.toLowerCase();
      if (name.includes(searchTerm) || job.includes(searchTerm)) {
        item.style.display = 'flex';
      } else {
        item.style.display = 'none';
      }
    });
  });

  const paginationButtons = document.querySelectorAll('.connections_pagination button');
  paginationButtons.forEach(button => {
    button.addEventListener('click', () => {
      if (!button.classList.contains('active') && !button.querySelector('i')) {
        paginationButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
      }
    });
  });

  function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  }