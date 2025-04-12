document.addEventListener('DOMContentLoaded', () => {
    const uploadBox = document.getElementById('uploadBox');
    const imageInput = document.getElementById('imageInput');
    const previewSection = document.getElementById('previewSection');
    const originalImage = document.getElementById('originalImage');
    const colorizedImage = document.getElementById('colorizedImage');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const downloadBtn = document.getElementById('downloadBtn');

    // Handle click on upload box
    uploadBox.addEventListener('click', () => {
        imageInput.click();
    });

    // Handle drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImage(file);
        }
    });

    // Handle file input change
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImage(file);
        }
    });

    // Handle image processing
    async function handleImage(file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            // Show preview section
            previewSection.style.display = 'grid';
            
            // Display original image
            originalImage.src = e.target.result;
            
            // Show loading spinner
            loadingSpinner.style.display = 'flex';
            colorizedImage.style.opacity = '0';

            try {
                // Send image to backend for processing
                const response = await fetch('http://localhost:5000/colorize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        image: e.target.result
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to process image');
                }

                const data = await response.json();
                
                // Display colorized image
                colorizedImage.src = data.colorized;
                colorizedImage.style.opacity = '1';
                downloadBtn.style.display = 'block';
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to process image. Please try again.');
            } finally {
                loadingSpinner.style.display = 'none';
            }
        };
        reader.readAsDataURL(file);
    }

    // Handle download button click
    downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = 'colorized-image.png';
        link.href = colorizedImage.src;
        link.click();
    });
});