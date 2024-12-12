    const aboutMeData = {
      title: "John Doe",
      description: "Passionate developer with over 5 years of experience in web development. Specialized in creating responsive and user-friendly applications using modern technologies.",
      image: "/api/placeholder/600/600",
      extra_data: "Available for freelance projects and collaborations",
      location: "San Francisco, CA",
      created_at: "2024-12-12T10:00:00Z"
    };
 function formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    }
    document.getElementById('aboutMeTitle').textContent = aboutMeData.title;
    document.getElementById('aboutMeDescription').textContent = aboutMeData.description;
    document.getElementById('aboutMeLocation').textContent = aboutMeData.location;
    document.getElementById('aboutMeExtra').textContent = aboutMeData.extra_data;
    document.getElementById('aboutMeDate').textContent = `Last updated: ${formatDate(aboutMeData.created_at)}`;

    if (aboutMeData.image) {
      document.getElementById('aboutMeImage').src = aboutMeData.image;
    }