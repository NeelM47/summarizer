// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const summarizeBtn = document.getElementById('summarize-btn');
    const addDocBtn = document.getElementById('add-doc-btn');
    const documentsContainer = document.getElementById('documents-container');
    const resultDiv = document.getElementById('result');
    const loaderDiv = document.getElementById('loader');
    
    let docCount = 2; // Initial document count

    // --- LOGIC TO ADD NEW DOCUMENT TEXTBOX ---
    addDocBtn.addEventListener('click', () => {
        docCount++;
        const newDocContainer = document.createElement('div');
        newDocContainer.className = 'doc-container';
        
        const newTextArea = document.createElement('textarea');
        newTextArea.className = 'document-input';
        newTextArea.placeholder = `Paste Document ${docCount} here...`;
        
        newDocContainer.appendChild(newTextArea);
        documentsContainer.appendChild(newDocContainer);
    });

    // --- LOGIC TO SUMMARIZE ---
    summarizeBtn.addEventListener('click', async () => {
		const numClusters = document.getElementById("num-clusters").value;
        // Find ALL textareas with the class 'document-input'
        const textareas = document.querySelectorAll('.document-input');
        
        // Collect text from all non-empty textareas
        const documents = Array.from(textareas)
                               .map(textarea => textarea.value)
                               .filter(doc => doc.trim() !== '');

        if (documents.length === 0) {
            resultDiv.innerHTML = '<p style="color: red;">Please provide at least one document.</p>';
            return;
        }

        // Show loader and disable buttons
        loaderDiv.style.display = 'block';
        summarizeBtn.disabled = true;
        addDocBtn.disabled = true;
        resultDiv.innerHTML = '<p>Processing...</p>';

        try {
            const response = await fetch('/summarize/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ documents: documents,
									   num_clusters: parseInt(numClusters, 10)
				}),
            });

            if (!response.ok) {
                // Try to get a more detailed error from the server
                const errorData = await response.json().catch(() => ({ detail: 'Unknown server error' }));
                throw new Error(`HTTP error ${response.status}: ${errorData.detail}`);
            }

            const data = await response.json();
            resultDiv.innerHTML = `<p>${data.summary}</p>`;

        } catch (error) {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
        } finally {
            // Hide loader and re-enable buttons
            loaderDiv.style.display = 'none';
            summarizeBtn.disabled = false;
            addDocBtn.disabled = false;
        }
    });
});
