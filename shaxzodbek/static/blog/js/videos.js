const videoGrid = document.getElementById('videoGrid');
  const videoCount = 6;

  for (let i = 0; i < videoCount; i++) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.style.animationDelay = `${i * 0.1}s`;

    card.innerHTML = `
                <img src="/api/placeholder/400/200" alt="Video thumbnail">
                <div class="content">
                    <h3>LOREM IPSUM IS SIMPLY DUMMY TEXT</h3>
                    <a href="#" class="read-more">READ MORE</a>
                </div>
            `;

    videoGrid.appendChild(card);
  }

  // Search functionality
  const searchInput = document.getElementById('searchInput');
  searchInput.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.video-card');

    cards.forEach(card => {
      const title = card.querySelector('h3').textContent.toLowerCase();
      if (title.includes(searchTerm)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });