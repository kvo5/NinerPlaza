document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.product-track');
    const cards = track.querySelectorAll('.product-card');
    const prevBtn = document.querySelector('.carousel-nav.prev');
    const nextBtn = document.querySelector('.carousel-nav.next');
    let currentIndex = 1;  // Start with middle card active
    
    // Set initial active state
    updateActiveCard();

    // Auto scroll every 5 seconds (increased from 3 seconds for smoother feel)
    let autoScrollInterval = setInterval(nextSlide, 5000);

    function updateActiveCard() {
        cards.forEach(card => {
            card.classList.remove('active');
            card.style.transition = 'all 0.5s ease';  // Smoother transition
        });
        cards[currentIndex].classList.add('active');
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % cards.length;
        updateActiveCard();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + cards.length) % cards.length;
        updateActiveCard();
    }

    // Add click event listeners to navigation buttons
    prevBtn.addEventListener('click', () => {
        clearInterval(autoScrollInterval);  // Stop auto scroll
        prevSlide();
        // Resume auto scroll in the right direction after manual navigation
        autoScrollInterval = setInterval(nextSlide, 5000);
    });

    nextBtn.addEventListener('click', () => {
        clearInterval(autoScrollInterval);  // Stop auto scroll
        nextSlide();
        // Resume auto scroll in the right direction after manual navigation
        autoScrollInterval = setInterval(nextSlide, 5000);
    });

    // Pause auto-scroll when hovering over the carousel
    track.addEventListener('mouseenter', () => {
        clearInterval(autoScrollInterval);
    });

    // Resume auto-scroll when mouse leaves the carousel
    track.addEventListener('mouseleave', () => {
        autoScrollInterval = setInterval(nextSlide, 5000);
    });
}); 