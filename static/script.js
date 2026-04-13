document.addEventListener('DOMContentLoaded', function() {
    // Initialize particles background
    particlesJS.load('particles-js', '/static/particles-config.json');

    const promptInput = document.getElementById('promptInput');
    const generateBtn = document.getElementById('generateBtn');
    const output = document.getElementById('output');
    let isGenerating = false;

    generateBtn.addEventListener('click', async function() {
        if (isGenerating) return;
        isGenerating = true;
        output.style.display = 'none';

        try {
            // Your existing image generation code here
            // When generation completes:
            output.style.display = 'block';
        } catch (error) {
            console.error('Generation failed:', error);
        } finally {
            isGenerating = false;
        }
    });
})();