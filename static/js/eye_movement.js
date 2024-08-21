document.addEventListener('mousemove', (event) => {
    const eyes = document.querySelectorAll('.eye');
    eyes.forEach(eye => {
        const rect = eye.getBoundingClientRect();
        const eyeX = rect.left + rect.width / 2;
        const eyeY = rect.top + rect.height / 2;

        const angle = Math.atan2(event.clientY - eyeY, event.clientX - eyeX);
        const distance = Math.min(eye.offsetWidth / 4, eye.offsetHeight / 4);

        const pupil = eye.querySelector('.pupil');
        pupil.style.transform = `translate(${Math.cos(angle) * distance}px, ${Math.sin(angle) * distance}px)`;
    });
});