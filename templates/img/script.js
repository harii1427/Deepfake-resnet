document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file');
    const imgArea = document.querySelector('.img-area');
    const webcamAccess = document.getElementById('webcam-access');
    const webcamModal = document.getElementById('webcamModal');
    const video = document.getElementById('video');
    const captureBtn = document.getElementById('captureBtn');

    // Function to handle file selection
    function handleFileSelect(file) {
        const reader = new FileReader();

        reader.onload = function (event) {
            const imgSrc = event.target.result;
            displayImage(imgSrc);
        };

        reader.readAsDataURL(file);
    }

    // Function to display the selected image
    function displayImage(imgSrc) {
        imgArea.innerHTML = `
            <img src="${imgSrc}" alt="Uploaded Image">
        `;
    }

    // Event listener for file input change
    fileInput.addEventListener('change', function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            handleFileSelect(selectedFile);
        }
    });

    // Drag and drop functionality
    const dragDropArea = document.getElementById('dragDropArea');

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

    // Webcam access functionality
    webcamAccess.addEventListener('click', function () {
        openWebcamModal();
    });

    // Function to open the webcam modal
    function openWebcamModal() {
        webcamModal.style.display = 'block';
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    video.srcObject = stream;
                    video.play();
                })
                .catch(function (error) {
                    console.error('Error accessing the camera:', error);
                });
        }
    }

    // Close webcam modal
    webcamModal.addEventListener('click', function (event) {
        if (event.target === webcamModal || event.target.classList.contains('close')) {
            closeWebcamModal();
        }
    });

    // Function to close the webcam modal
    function closeWebcamModal() {
        webcamModal.style.display = 'none';
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }
    }

    // Capture image from webcam
    captureBtn.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        const imgSrc = canvas.toDataURL('image/png');
        displayImage(imgSrc);
        closeWebcamModal();
    });
});
