    // Image gallery modal
    const modal = document.querySelector('.modal');
    const modalImg = document.querySelector('.modal-image');
    const closeModal = document.querySelector('.close-modal');
    const galleryImages = document.querySelectorAll('.gallery-image');

    galleryImages.forEach(img => {
        img.addEventListener('click', () => {
            modal.style.display = 'block';
            modalImg.src = img.src;
            setTimeout(() => modal.classList.add('active'), 10);
        });
    });

    closeModal.addEventListener('click', () => {
        modal.classList.remove('active');
        setTimeout(() => modal.style.display = 'none', 300);
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            setTimeout(() => modal.style.display = 'none', 300);
        }
    });

    // Status badge
    const statusBadge = document.querySelector('.status-badge');
    const isWorking = true; // This would come from your backend
    statusBadge.className = `status-badge ${isWorking ? 'status-active' : 'status-inactive'}`;
    statusBadge.textContent = isWorking ? 'Currently Working' : 'Not Working';

    // Back button
    document.querySelector('.back-button').addEventListener('click', () => {
        window.history.back();
    });

    // Technology tags hover effect
    document.querySelectorAll('.tech-tag').forEach(tag => {
        tag.addEventListener('mouseenter', () => {
            tag.style.transform = 'translateY(-2px)';
        });

        tag.addEventListener('mouseleave', () => {
            tag.style.transform = 'translateY(0)';
        });
    });