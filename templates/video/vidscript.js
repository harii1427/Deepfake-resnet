document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('input1');
    const videoArea = document.getElementById('video');
    let videoStream = null;
    let mediaRecorder = null;
    let recordedChunks = [];

    // Function to handle file selection
    function handleFileSelect(file) {
        const reader = new FileReader();

        reader.onload = function (event) {
            const videoSrc = event.target.result;
            displayVideo(videoSrc);
        };

        reader.readAsDataURL(file);
    }

    // Function to display the selected video
    function displayVideo(videoSrc) {
        videoArea.innerHTML = `
            <video controls>
                <source src="${videoSrc}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        `;
    }

    // Event listener for file input change
    fileInput.addEventListener('change', function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            handleFileSelect(selectedFile);
        }
    });

    // Function to access camera
    function accessCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                videoStream = stream;
                const videoElement = document.createElement('video');
                videoElement.srcObject = stream;
                videoElement.autoplay = true;
                videoArea.innerHTML = '';
                videoArea.appendChild(videoElement);
            })
            .catch(error => {
                console.error('Error accessing camera:', error);
                alert('Error accessing camera. Please check your browser settings and try again.');
            });
    }

    // Event listener for camera access button
    document.querySelector('.camera_button').addEventListener('click', accessCamera);

    // Function to start recording
    function startRecording() {
        if (videoStream) {
            const options = { mimeType: 'video/webm' };
            mediaRecorder = new MediaRecorder(videoStream, options);
            mediaRecorder.ondataavailable = handleDataAvailable;
            mediaRecorder.start();
            console.log('Recording started...');
        } else {
            console.error('No video stream available.');
            alert('No video stream available. Please access the camera first.');
        }
    }

    // Event listener for record button
    document.querySelector('.record_button').addEventListener('click', startRecording);

    // Function to handle data available during recording
    function handleDataAvailable(event) {
        recordedChunks.push(event.data);
        console.log('Recorded chunks:', recordedChunks);
        // Save recorded video when recording is stopped
        mediaRecorder.onstop = function() {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'recorded-video.webm';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            recordedChunks = [];
        };
    }

    // Drag and drop functionality (for video upload)
    const dragDropArea = document.querySelector('.app');

    // Prevent default behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dragDropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area on drag over
    ['dragenter', 'dragover'].forEach(eventName => {
        dragDropArea.addEventListener(eventName, highlight, false);
    });

    // Remove highlight on drag leave
    ['dragleave', 'drop'].forEach(eventName => {
        dragDropArea.addEventListener(eventName, unhighlight, false);
    });

    // Handle drop event
    dragDropArea.addEventListener('drop', handleDrop, false);

    // Function to prevent default behaviors
    function preventDefaults(event) {
        event.preventDefault();
        event.stopPropagation();
    }

    // Function to highlight drop area
    function highlight() {
        dragDropArea.classList.add('highlight');
    }

    // Function to remove highlight from drop area
    function unhighlight() {
        dragDropArea.classList.remove('highlight');
    }

    // Function to handle dropped files
    function handleDrop(event) {
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const droppedFile = files[0];
            handleFileSelect(droppedFile);
        }
    }
});
