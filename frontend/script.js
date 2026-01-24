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
    const originalPreview = document.getElementById('original-preview');
    const processedPreview = document.getElementById('processed-preview');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');
    const processStatus = document.getElementById('process-status');

    // Context Toggle Elements
    const publicRadio = document.getElementById('public');
    const privateRadio = document.getElementById('private');
    const publicDesc = document.getElementById('public-desc');
    const privateDesc = document.getElementById('private-desc');

    // State
    let currentFile = null;
    let processedImageUrl = null;

    // ========================================
    // File Upload Handlers
    // ========================================

    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());

    // Keyboard accessibility
    dropZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    // Drag and drop
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

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    /**
     * Handle uploaded file
     * @param {File} file - The uploaded file
     */
    function handleFile(file) {
        // Validate file type
        const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            showNotification('Please upload a valid image file (PNG, JPG, JPEG)', 'error');
            return;
        }

        // Validate file size (max 10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            showNotification('File size must be less than 10MB', 'error');
            return;
        }

        currentFile = file;

        // Read and display preview
        const reader = new FileReader();
        reader.onload = (e) => {
            originalPreview.src = e.target.result;

            // Reset processed image
            processedPreview.src = '';
            processedImageUrl = null;
            downloadBtn.classList.add('hidden');

            // Show results section
            resultsSection.classList.remove('hidden');

            // Enable process button
            processBtn.disabled = false;

            // Update status
            updateProcessStatus('Ready', false);
        };
        reader.readAsDataURL(file);
    }

    // ========================================
    // Context Toggle Handlers
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

    publicRadio.addEventListener('change', updateContextDesc);
    privateRadio.addEventListener('change', updateContextDesc);

    // ========================================
    // Image Processing
    // ========================================

    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // Show loading state
        loader.classList.remove('hidden');
        processBtn.disabled = true;
        updateProcessStatus('Processing...', true);

        // Prepare form data
        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('context', publicRadio.checked ? 'public' : 'private');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.output_image) {
                // Extract filename and create URL
                const filename = data.output_image.split('/').pop();
                processedImageUrl = `/processed/${filename}?t=${Date.now()}`;

                // Load processed image
                processedPreview.src = processedImageUrl;

                // Show download button
                downloadBtn.classList.remove('hidden');

                // Auto download
                const link = document.createElement('a');
                link.href = processedImageUrl;
                link.download = `protected_${currentFile.name}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Update status
                updateProcessStatus('Complete', false);

            } else {
                throw new Error(data.error || 'Processing failed');
            }
        } catch (error) {
            console.error('Processing error:', error);
            showNotification(error.message || 'An error occurred during processing', 'error');
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
        if (!processedImageUrl) return;

        // Create download link
        const link = document.createElement('a');
        link.href = processedImageUrl;
        link.download = `protected_${currentFile.name}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // ========================================
    // Utility Functions
    // ========================================

    /**
     * Update the processing status indicator
     * @param {string} text - Status text
     * @param {boolean} processing - Whether currently processing
     */
    function updateProcessStatus(text, processing) {
        const statusDot = processStatus.querySelector('.status-dot');
        const statusText = processStatus.lastChild;

        statusText.textContent = text;

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

    /**
     * Show notification to user
     * @param {string} message - Notification message
     * @param {string} type - Notification type ('error', 'success', 'info')
     */
    function showNotification(message, type = 'info') {
        // Simple alert for now - could be enhanced with custom notification UI
        alert(message);
    }
});
