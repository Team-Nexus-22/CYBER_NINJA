
document.getElementById('checkForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const websiteUrl = document.getElementById('websiteInput').value.trim();

    if (!websiteUrl) {
        alert('Please enter a valid website URL');
        return;
    }

    const apiKey = '8717eff9e6baf7e37ed5df9dad469841f46f722872657996628f9365dd5562fc';
    const apiUrl = 'https://www.virustotal.com/api/v3/urls';

    const options = {
  method: 'POST',
  headers: {
    accept: 'application/json',
    'x-apikey': '8717eff9e6baf7e37ed5df9dad469841f46f722872657996628f9365dd5562fc',
    'content-type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({url: websiteUrl})
};
    fetch(apiUrl, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Initial Response from VirusTotal:', data);
            if (data.data && data.data.id) {
                // If successful, fetch analysis details using the provided link
                return fetch(data.data.links.self, {
                    headers: {
                        'x-apikey': apiKey,
                        'Content-Type': 'application/json'
                    }
                });
            } else {
                throw new Error('Unable to get analysis ID from VirusTotal');
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch analysis details');
            }
            return response.json();
        })
        .then(analysisData => {
            console.log('Analysis Details:', analysisData);
            displayResult(analysisData);
        })
        .catch(error => {
            console.error('Error:', error);
            displayError('This website is flagged as malicious');
        });
});

function displayResult(analysisData) {
    const resultContainer = document.getElementById('resultContainer');
    const resultMessage = document.getElementById('resultMessage');

    if (analysisData.data && analysisData.data.attributes && analysisData.data.attributes.stats) {
        const stats = analysisData.data.attributes.stats;
        if (stats.harmless > 0 || stats.suspicious > 0) {
            resultMessage.textContent = 'This website is safe.';
            resultMessage.style.color = 'green';
        } else {
            resultMessage.textContent = 'This website is flagged as malicious or suspicious.';
            resultMessage.style.color = 'red';
        }
    } else {
        displayError('Error: Unable to determine website status.');
    }

    resultContainer.classList.remove('hidden');
}

function displayError(message) {
    const resultContainer = document.getElementById('resultContainer');
    const resultMessage = document.getElementById('resultMessage');
    
    resultMessage.textContent = message;
    resultMessage.style.color = 'red';
    
    resultContainer.classList.remove('hidden');
}
