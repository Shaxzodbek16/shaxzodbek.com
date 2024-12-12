  // Add click event for "See More" button
  document.querySelector('.see-more').addEventListener('click', () => {
    // Add your logic for see more functionality
    console.log('See more clicked');
  });

  // Add hover effect for blog image
  const blogImage = document.querySelector('.blog-image');
  blogImage.addEventListener('mouseover', () => {
    blogImage.style.transform = 'scale(1.02)';
    blogImage.style.transition = 'transform 0.3s ease';
  });
  blogImage.addEventListener('mouseout', () => {
    blogImage.style.transform = 'scale(1)';
  });