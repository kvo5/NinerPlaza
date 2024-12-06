// Giftcard Carousel Implementation
document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.carousel');
    const items = carousel.querySelectorAll('.carousel-item');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    let currentIndex = 0;

    function showItem(index) {
        items.forEach((item, i) => {
            item.classList.remove('active');
            if (i === index) {
                item.classList.add('active');
            }
        });
    }

    function nextItem() {
        currentIndex = (currentIndex + 1) % items.length;
        showItem(currentIndex);
    }

    function prevItem() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        showItem(currentIndex);
    }

    nextBtn.addEventListener('click', nextItem);
    prevBtn.addEventListener('click', prevItem);

    // Optional: Auto-play
    setInterval(nextItem, 5000);
});

// Image Hover-effect Implementation
document.addEventListener('DOMContentLoaded', function () {
    const productImages = document.querySelectorAll('.product-item img');

    productImages.forEach(image => {
        const hoverImageSrc = image.getAttribute('data-hover');
        const originalSrc = image.getAttribute('src');

        image.addEventListener('mouseover', () => {
            image.setAttribute('src', hoverImageSrc);
        });

        image.addEventListener('mouseout', () => {
            image.setAttribute('src', originalSrc);
        });
    });
});

// Zoom functionality for product images
document.addEventListener('DOMContentLoaded', function() {
    const productImage = document.querySelector('.product-image img');
    if (productImage) {
        productImage.addEventListener('click', () => {
            productImage.classList.toggle('zoomed');
        });
    }
});

// Size Modal
document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById("sizeChartModal");
    var btn = document.querySelector(".size-chart");
    var span = document.getElementsByClassName("close")[0];
    var inchesBtn = document.getElementById("inchesBtn");
    var cmBtn = document.getElementById("cmBtn");
    var sizeChartImage = document.getElementById("sizeChartImage");

    btn.onclick = function() {
        modal.style.display = "block";
        document.body.classList.add('modal-open');
    }

    span.onclick = function() {
        modal.style.display = "none";
        document.body.classList.remove('modal-open');
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            document.body.classList.remove('modal-open');
        }
    }

    inchesBtn.onclick = function() {
        sizeChartImage.src = "images/T-ShirtINCHES.png";
        inchesBtn.classList.add("active");
        cmBtn.classList.remove("active");
    }

    cmBtn.onclick = function() {
        sizeChartImage.src = "images/T-ShirtCENTI.png";
        cmBtn.classList.add("active");
        inchesBtn.classList.remove("active");
    }
});