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


document.getElementById('voiceCommandButton').addEventListener('click', function () {
    startVoiceCommand();
});

function startVoiceCommand() {
    // Use Web Speech API or other methods to capture user's voice input
    // For example, you can use the Web Speech API for basic functionality:
    if ('webkitSpeechRecognition' in window) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onresult = function (event) {
            var result = event.results[0][0].transcript;
            sendVoiceCommandToServer(result);
        };

        recognition.start();
    } else {
        alert("Web Speech API is not supported in this browser. Please use a supported browser.");
    }
}
