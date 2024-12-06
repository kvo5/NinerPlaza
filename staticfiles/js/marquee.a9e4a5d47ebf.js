document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.sponsors-track');
    const firstGroup = track.querySelector('.sponsor-group');
    
    // Create exact clone of the first group
    const clone = firstGroup.cloneNode(true);
    track.appendChild(clone);
}); 