const slideWidth = 320;  // Update to match new card width + margin
const cardsPerSlide = Math.floor(carouselContainer.offsetWidth / slideWidth);

// Update the slide function
function slideCards(direction) {
    const currentPosition = parseInt(carouselSlide.style.transform.replace('translateX(', '')) || 0;
    const moveAmount = direction === 'next' ? -slideWidth : slideWidth;
    const newPosition = currentPosition + moveAmount;
    
    // Add bounds checking
    if (newPosition > 0 || Math.abs(newPosition) > (totalCards - cardsPerSlide) * slideWidth) {
        return;
    }
    
    carouselSlide.style.transform = `translateX(${newPosition}px)`;
} 