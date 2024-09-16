// Get the HTML elements
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('pdfFile');
const qaSection = document.getElementById('qa-section');
const qaList = document.getElementById('qa-list');
const loadingIndicator = document.getElementById('loading');
const uploadMoreSection = document.getElementById('uploadMore');
const uploadAnotherBtn = document.getElementById('uploadAnother');

// Function to handle PDF upload
uploadBtn.addEventListener('click', async function () {
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a PDF file to upload.');
        return;
    }

    if (!file.name.endsWith('.pdf')) {
        alert('Only PDF files are allowed.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    // Show loading indicator
    loadingIndicator.classList.remove('hidden');
    qaSection.classList.add('hidden');
    uploadMoreSection.classList.add('hidden');

    try {
        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            // Display the questions and answers
            displayQuestionsAndAnswers(result.questions_and_answers);
        }
    } catch (error) {
        alert('An error occurred: ' + error.message);
    } finally {
        loadingIndicator.classList.add('hidden');
    }
});

// Function to display questions and answers
function displayQuestionsAndAnswers(qAndA) {
    qaList.innerHTML = '';

    for (const [question, answer] of Object.entries(qAndA)) {
        const questionElem = document.createElement('div');
        questionElem.innerHTML = `<strong>Q: ${question}</strong><br>A: ${answer}`;
        qaList.appendChild(questionElem);
    }

    qaSection.classList.remove('hidden');
    uploadMoreSection.classList.remove('hidden');
}

// Handle "Upload Another PDF" button
uploadAnotherBtn.addEventListener('click', function () {
    window.open('upload.html', '_blank'); // Open the upload page in a new tab
});
