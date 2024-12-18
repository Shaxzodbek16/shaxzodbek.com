document.addEventListener('DOMContentLoaded', function() {
    // File upload preview
    const fileInput = document.getElementById('profile_picture');
    const fileName = document.querySelector('.file-name');

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileName.textContent = this.files[0].name;

            // Preview image if possible
            const reader = new FileReader();
            reader.onload = function(e) {
                const avatar = document.querySelector('.profile-avatar img');
                if (avatar) {
                    avatar.src = e.target.result;
                } else {
                    const placeholder = document.querySelector('.avatar-placeholder');
                    if (placeholder) {
                        placeholder.style.display = 'none';
                        const newImg = document.createElement('img');
                        newImg.src = e.target.result;
                        document.querySelector('.profile-avatar').appendChild(newImg);
                    }
                }
            }
            reader.readAsDataURL(this.files[0]);
        } else {
            fileName.textContent = 'No file chosen';
        }
    });

    // Form submission animation
    const form = document.querySelector('.profile-form');
    const saveBtn = document.querySelector('.save-btn');

    form.addEventListener('submit', function(e) {
        saveBtn.style.width = saveBtn.offsetWidth + 'px';
        saveBtn.innerHTML = '<i class="bx bx-loader-alt bx-spin"></i>';
    });
});