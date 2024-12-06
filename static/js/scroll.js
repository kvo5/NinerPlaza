document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with class 'scroll-to'
    const scrollButtons = document.querySelectorAll('.scroll-to');
    
    scrollButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the target section id from the href
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            // Calculate offset to account for fixed header
            const headerOffset = 110;
            const elementPosition = targetSection.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        });
    });
}); 