const images = document.querySelectorAll('.cv__img');
const prevButton = document.querySelector('.cv__img-nav--prev');
const nextButton = document.querySelector('.cv__img-nav--next');
let currentImageIndex = 0;
let intervalId;

function showImage(index) {
    images[currentImageIndex].classList.remove('active');
    currentImageIndex = (index + images.length) % images.length;
    images[currentImageIndex].classList.add('active');
}

function showNextImage() {
    showImage(currentImageIndex + 1);
}

function showPrevImage() {
    showImage(currentImageIndex - 1);
}

function startAutoSlide() {
    intervalId = setInterval(showNextImage, 5000);
}

function stopAutoSlide() {
    clearInterval(intervalId);
}

prevButton.addEventListener('click', () => {
    showPrevImage();
    stopAutoSlide();
    startAutoSlide();
});

nextButton.addEventListener('click', () => {
    showNextImage();
    stopAutoSlide();
    startAutoSlide();
});

startAutoSlide();