document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.detail-group').forEach(group => {
      group.addEventListener('mouseenter', () => {
        group.querySelector('.detail-value').style.transform = 'translateY(-2px)';
      });

      group.addEventListener('mouseleave', () => {
        group.querySelector('.detail-value').style.transform = 'translateY(0)';
      });
    });

    const matches = document.querySelectorAll('.match-tag');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, { threshold: 0.5 });

    matches.forEach((match, index) => {
      match.style.opacity = '0';
      match.style.transform = 'translateY(20px)';
      match.style.transition = `all 0.3s ease ${index * 0.1}s`;
      observer.observe(match);
    });
  });