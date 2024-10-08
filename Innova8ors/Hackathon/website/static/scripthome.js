document.addEventListener("DOMContentLoaded", function() {
    const text = "ELLA";
    const speed = 100; // Speed of typing in milliseconds
    const cursor = document.createElement('span');
    cursor.className = 'cursor';
    const header = document.querySelector('header');

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

    // Add event listener for scroll event
    window.addEventListener('scroll', changeHeaderColor);
});
