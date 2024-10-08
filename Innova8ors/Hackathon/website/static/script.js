// app.js
document.addEventListener("DOMContentLoaded", function() {
    const text = "ELLA";
    const speed = 100; // Speed of typing in milliseconds
    const cursor = document.createElement('span');
    cursor.className = 'cursor';

    // Start typing animation after a delay of 2000 milliseconds (2 seconds)
    setTimeout(() => {
        typeWriter(text, 0); // Start typing from the beginning
    }, 2500);

    function typeWriter(text, i) {
        const typewriterElement = document.querySelector(".typewriter");

        if (i < text.length) {
            typewriterElement.innerHTML += text.charAt(i);
            i++;
            setTimeout(() => typeWriter(text, i), speed);
        } else {
            // Append the cursor after typing animation finishes
            typewriterElement.appendChild(cursor);
        }
    }

    // Reload the page when the logo is clicked
    window.reloadPage = function() {
        location.reload();
    };

    // Hide the header on scroll
    var navbar = document.getElementById("navbar"); // Corrected to getElementById
    var lastScrollTop = 0;

    window.addEventListener("scroll", function() {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            navbar.style.top = "-80px";
        } else {
            navbar.style.top = "0";
        }
        lastScrollTop = scrollTop;
    });

    // Mousemove animation for eyes
    document.addEventListener('mousemove', (event) => {
        const eyes = document.querySelectorAll('.eye');
        eyes.forEach(eye => {
            const boundingBox = eye.getBoundingClientRect();
            const eyeCenterX = boundingBox.left + boundingBox.width / 2;
            const eyeCenterY = boundingBox.top + boundingBox.height / 2;

            const deltaX = event.clientX - eyeCenterX;
            const deltaY = event.clientY - eyeCenterY;
            const angle = Math.atan2(deltaY, deltaX);
            const distance = Math.min(boundingBox.width / 4, boundingBox.height / 4);

            const pupil = eye.querySelector('.pupil');
            const pupilX = distance * Math.cos(angle);
            const pupilY = distance * Math.sin(angle);

            pupil.style.transform = `translate(${pupilX}px, ${pupilY}px)`;
        });
    });
});

        // JavaScript to count words in the textbox
        const textarea = document.getElementById('user-input');
        const wordCountDisplay = document.getElementById('word-count');

        textarea.addEventListener('input', function() {
            const words = this.value.trim().split(/\s+/).filter(function(word) {
                return word.length > 0;
            });
            const wordCount = words.length;
            wordCountDisplay.textContent = `Words: ${wordCount}/250`;
        });
