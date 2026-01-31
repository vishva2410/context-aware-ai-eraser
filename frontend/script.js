/**
 * Context-Aware AI Eraser
 * Frontend JavaScript Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    // ========================================
    // DOM Elements
    // ========================================
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const processBtn = document.getElementById('process-btn');
    const downloadBtn = document.getElementById('download-btn');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');
    const processStatus = document.getElementById('process-status');

    // Result Containers
    const imageComparison = document.getElementById('image-comparison');
    // Video elements removed

    // Image Elements
    const compOriginal = document.getElementById('comp-original');
    const compProcessed = document.getElementById('comp-processed');
    const sliderHandle = document.querySelector('.handle');
    const afterWrapper = document.querySelector('.image-wrapper.after');


    // Context Toggle Elements
    const publicRadio = document.getElementById('public');
    const privateRadio = document.getElementById('private');
    const publicDesc = document.getElementById('public-desc');
    const privateDesc = document.getElementById('private-desc');

    // State
    let currentFile = null;
    let processedUrl = null;
    let isDragging = false;

    // ========================================
    // File Upload Handlers
    // ========================================

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        // Validate file type
        const validImageTypes = ['image/png', 'image/jpeg', 'image/jpg'];

        if (!validImageTypes.includes(file.type)) {
            showNotification('Please upload a valid image (PNG/JPG)', 'error');
            return;
        }

        // Validate file size (max 10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            showNotification('File too large. Max size: 10MB', 'error');
            return;
        }

        currentFile = file;

        // Reset UI
        resultsSection.classList.remove('hidden');
        processBtn.disabled = false;
        downloadBtn.classList.add('hidden');
        processedUrl = null;
        updateProcessStatus('Ready to Process', false);

        const objectUrl = URL.createObjectURL(file);

        // Setup Image Comparison View
        if (imageComparison) imageComparison.classList.remove('hidden');
        const videoResult = document.getElementById('video-result');
        if (videoResult) videoResult.classList.add('hidden'); // Hide if exists

        if (compOriginal) compOriginal.src = objectUrl;
        if (compProcessed) compProcessed.src = objectUrl; // Initially match original

        // Reset slider position
        if (sliderHandle) sliderHandle.style.left = '50%';
        if (afterWrapper) afterWrapper.style.width = '50%';
    }

    // ========================================
    // Comparison Slider Logic
    // ========================================

    function updateSlider(x) {
        if (!imageComparison || !sliderHandle) return;
        const sliderRect = imageComparison.getBoundingClientRect();
        let percentage = ((x - sliderRect.left) / sliderRect.width) * 100;

        // Clamp
        percentage = Math.max(0, Math.min(100, percentage));

        sliderHandle.style.left = `${percentage}%`;

        // The 'after' image is the PROCESSED one (bottom layer logic usually, but here:
        // wrapper.after has z-index 1. wrapper.before (original) has z-index 2.
        // If we want to reveal the 'processed' image, we clip the 'before' image.
        // Let's adjust: "before" wrapper is Original (Top). "after" wrapper is Processed (Bottom).

        // Actually earlier CSS: .before { z-index: 2; width: 50% }
        // So 'before' (Original) is being clipped. 
        // 100% width = Full Original. 0% width = Full Processed.

        // Let's invert the slider logic to make it intuitive:
        // Slide Right -> Reveal Processed? Or Reveal Original?

        // Let's use clip-path or width on the TOP element (Original).
        const originalWrapper = document.querySelector('.image-wrapper.before');
        if (originalWrapper) originalWrapper.style.width = `${percentage}%`;
    }

    if (imageComparison) {
        imageComparison.addEventListener('mousedown', () => isDragging = true);
        imageComparison.addEventListener('touchstart', () => isDragging = true);
    }

    document.addEventListener('mouseup', () => isDragging = false);
    document.addEventListener('touchend', () => isDragging = false);

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        updateSlider(e.clientX);
    });

    document.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        updateSlider(e.touches[0].clientX);
    });


    // ========================================
    // Context Toggle
    // ========================================

    function updateContextDesc() {
        if (publicRadio.checked) {
            publicDesc.classList.add('active');
            privateDesc.classList.remove('active');
        } else {
            publicDesc.classList.remove('active');
            privateDesc.classList.add('active');
        }
    }

    if (publicRadio && privateRadio) {
        publicRadio.addEventListener('change', updateContextDesc);
        privateRadio.addEventListener('change', updateContextDesc);
    }

    // ========================================
    // Processing Logic
    // ========================================

    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        loader.classList.remove('hidden');
        processBtn.disabled = true;
        updateProcessStatus('Processing Image...', true);

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('context', publicRadio.checked ? 'public' : 'private');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            // Robust JSON handling
            let data;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                data = await response.json();
            } else {
                // If text/html, it's likely a server exception that wasn't caught as JSON
                const text = await response.text();
                console.error("Non-JSON response:", text);
                throw new Error("Server returned an invalid response (not JSON). See console.");
            }

            if (response.ok && data.output_image) {
                const filename = data.output_image.split('/').pop();
                processedUrl = `/processed/${filename}?t=${Date.now()}`;

                if (compProcessed) compProcessed.src = processedUrl;

                // Reset slider to middle to show difference
                if (imageComparison) {
                    updateSlider(imageComparison.getBoundingClientRect().left + (imageComparison.offsetWidth / 2));
                }

                downloadBtn.classList.remove('hidden');

                updateProcessStatus('Complete', false);

            } else {
                throw new Error(data.error || 'Processing failed');
            }
        } catch (error) {
            console.error('Processing error:', error);
            showNotification(error.message || 'An error occurred', 'error');
            updateProcessStatus('Error', false);
        } finally {
            loader.classList.add('hidden');
            processBtn.disabled = false;
        }
    });

    // ========================================
    // Download Handler
    // ========================================

    downloadBtn.addEventListener('click', () => {
        if (!processedUrl) return;

        const link = document.createElement('a');
        link.href = processedUrl;
        link.download = `protected_${currentFile.name}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    function updateProcessStatus(text, processing) {
        const statusDot = processStatus.querySelector('.status-dot');
        const statusText = processStatus.lastChild;

        if (statusText) statusText.textContent = text;

        if (statusDot) {
            if (processing) {
                statusDot.style.background = 'var(--warning)';
            } else if (text === 'Complete') {
                statusDot.style.background = 'var(--success)';
            } else if (text === 'Error') {
                statusDot.style.background = 'var(--danger)';
            } else {
                statusDot.style.background = 'var(--text-muted)';
            }
        }
    }

    function showNotification(message, type = 'info') {
        alert(message);
    }
});
