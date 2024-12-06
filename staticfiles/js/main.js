document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll functionality
    document.querySelectorAll('.scroll-to').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            const headerOffset = 120; // Match the scroll-padding-top value
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        });
    });

    // Scroll indicator visibility
    const scrollIndicator = document.querySelector('.scroll-indicator');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const opacity = 1 - (scrollTop / (window.innerHeight * 0.5));
        
        if (scrollIndicator) {
            scrollIndicator.style.opacity = Math.max(0, Math.min(1, opacity));
        }
        
        lastScrollTop = scrollTop;
    });

    // Optional: Add parallax effect to hero background
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
        });
    }
}); 