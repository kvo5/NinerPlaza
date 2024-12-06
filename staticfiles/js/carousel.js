document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const items = carousel.querySelectorAll('.carousel-item');
    const prevBtn = document.querySelector('.carousel-nav.prev');
    const nextBtn = document.querySelector('.carousel-nav.next');
    let currentIndex = 0;
    const totalItems = items.length;

    // Auto scroll every 5 seconds
    const autoScrollInterval = setInterval(nextSlide, 5000);

    function updateSlide(index) {
        items.forEach(item => item.classList.remove('active'));
        items[index].classList.add('active');
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalItems;
        updateSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateSlide(currentIndex);
    }

    prevBtn.addEventListener('click', () => {
        clearInterval(autoScrollInterval);
        prevSlide();
    });

    nextBtn.addEventListener('click', () => {
        clearInterval(autoScrollInterval);
        nextSlide();
    });
}); 