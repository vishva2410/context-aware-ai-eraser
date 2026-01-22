document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const processBtn = document.getElementById('process-btn');
    const originalPreview = document.getElementById('original-preview');
    const processedPreview = document.getElementById('processed-preview');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');

    // Toggle Logic
    const publicRadio = document.getElementById('public');
    const privateRadio = document.getElementById('private');
    const publicDesc = document.getElementById('public-desc');
    const privateDesc = document.getElementById('private-desc');

    let currentFile = null;

    // --- Drag & Drop ---
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.match('image.*')) {
            alert("Please upload an image file.");
            return;
        }
        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            originalPreview.src = e.target.result;
            // Hide previous results
            resultsSection.classList.remove('hidden');
            processedPreview.src = "";
            processBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // --- Context Toggle ---
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

    // --- Processing ---
    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        loader.classList.remove('hidden');
        processBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', currentFile);

        const context = publicRadio.checked ? 'public' : 'private';
        formData.append('context', context);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                // The API returns the file path, but we need to fetch it or ensure it's accessible.
                // Since this is a local setup and we're not serving the samples/output directory explicitly via static yet...
                // Wait, Flask static folder is ../frontend. 
                // We need to serve the output images. 
                // Let's rely on the backend returning a relative URL that we can use?
                // Currently backend returns absolute path or relative path like 'samples/output/...'
                // Flask default static folder serves from 'static'. 
                // We changed static_folder to 'frontend'.
                // We need a route to serve the processed images.

                // For now, let's assume we need to add a route for image serving or base64.
                // But wait, I didn't add that route in api/app.py.
                // I should probably fix that.

                // Let's try to load it. If it fails, I'll fix the backend.
                // Ideally, the backend should return a URL.
                // But for now, let's assume the path is directly accessible if we add a route.

                // Actually, let's fix the frontend to expect a data:image/png;base64 if we change backend,
                // OR we add a route to serve 'samples/output'.

                // Let's assume there is a route /images/<filename>. 
                // I'll add that route in the next step.

                // Let's construct a path.
                const filename = data.output_image.split('/').pop();
                processedPreview.src = `/processed/${filename}?t=${new Date().getTime()}`; // bust cache

            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (err) {
            console.error(err);
            alert("An error occurred during processing.");
        } finally {
            loader.classList.add('hidden');
            processBtn.disabled = false;
        }
    });
});
