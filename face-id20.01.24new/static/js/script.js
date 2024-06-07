document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('captureButton');

    // Helper function to delay a certain amount of time
    function delay(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(error => {
            console.error("Error accessing the camera", error);
        });

    async function capturePhoto(count) {
        if (count >= 20) return; // Stop after 20 photos

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/png');

        // Send the image data to the server
        try {
            const response = await fetch('/save_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ imageData: imageData })
            });
            const data = await response.json();
            console.log(data.message);
            await delay(500); // Wait for 0.5 seconds
            capturePhoto(count + 1); // Take the next photo
        } catch (error) {
            console.error('Error:', error);
        }
    }

    captureButton.addEventListener('click', () => capturePhoto(0));
});
