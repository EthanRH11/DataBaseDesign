document.addEventListener("DOMContentLoaded", () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains("back-vid")) {
                    // Only apply blur effect when the video is out of view
                    entry.target.classList.remove("hidden-video");
                } else if (entry.target.classList.contains("hidden-text")) {
                    // Animate text when it comes into view
                    entry.target.classList.add("show-text");
                } else {
                    // Apply text animation
                    entry.target.classList.add("show");
                }
            } else {
                if (entry.target.classList.contains("back-vid")) {
                    // Apply blur effect to the video when it's out of view
                    entry.target.classList.add("hidden-video");
                } else if (entry.target.classList.contains("hidden-text")) {
                    // Reverse text animation when it's out of view
                    entry.target.classList.remove("show-text");
                } else {
                    // Reverse text animation
                    entry.target.classList.remove("show");
                }
            }
        });
    });

    // Observe video and text elements separately
    const videoElement = document.querySelector('.back-vid');
    const textElements = document.querySelectorAll('.hidden, .hidden-text');

    // Observe the video and text elements separately
    observer.observe(videoElement);
    textElements.forEach((el) => observer.observe(el));
});