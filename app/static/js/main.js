document.addEventListener('DOMContentLoaded', function() {
    // Initialize sentiment distribution chart
    updateSentimentChart();

    // Handle real-time feedback form submission
    document.getElementById('feedbackForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const feedbackText = document.getElementById('feedbackText').value;
        const department = document.getElementById('department').value;
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: feedbackText,
                    department: department
                }),
            });

            const result = await response.json();
            
            if (response.ok) {
                displaySentimentResult(result);
                updateSentimentChart();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the feedback.');
        }
    });

    // Handle file upload form submission
    document.getElementById('fileUploadForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('feedbackFile');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            
            if (response.ok) {
                document.getElementById('uploadResult').innerHTML = `
                    <div class="alert alert-success">
                        ${result.message}
                    </div>
                `;
                updateSentimentChart();
            } else {
                document.getElementById('uploadResult').innerHTML = `
                    <div class="alert alert-danger">
                        Error: ${result.error}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('uploadResult').innerHTML = `
                <div class="alert alert-danger">
                    An error occurred while processing the file.
                </div>
            `;
        }
    });
});

// Display sentiment result with emoji
function displaySentimentResult(result) {
    const resultDiv = document.getElementById('sentimentResult');
    const emojiDiv = resultDiv.querySelector('.sentiment-emoji');
    const textDiv = resultDiv.querySelector('.sentiment-text');
    
    // Remove previous sentiment classes
    resultDiv.classList.remove('d-none');
    const sentimentDisplay = resultDiv.querySelector('.sentiment-display');
    sentimentDisplay.className = 'sentiment-display p-3 rounded';
    
    // Add appropriate sentiment class and emoji
    const sentimentEmoji = {
        'very positive': '😄',
        'positive': '🙂',
        'neutral': '😐',
        'negative': '🙁',
        'very negative': '😢'
    };
    
    sentimentDisplay.classList.add(result.sentiment.replace(' ', '-'));
    emojiDiv.textContent = sentimentEmoji[result.sentiment];
    textDiv.textContent = `Sentiment: ${result.sentiment} (Score: ${result.score.toFixed(2)})`;
}

// Update sentiment distribution chart
async function updateSentimentChart() {
    try {
        const response = await fetch('/stats');
        const stats = await response.json();
        
        const data = [{
            values: Object.values(stats.sentiment_distribution),
            labels: Object.keys(stats.sentiment_distribution).map(key => 
                key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
            ),
            type: 'pie',
            marker: {
                colors: ['#28a745', '#20c997', '#6c757d', '#dc3545', '#721c24']
            }
        }];
        
        const layout = {
            title: 'Sentiment Distribution',
            height: 400,
            showlegend: true,
            legend: {
                orientation: 'h',
                y: -0.1
            }
        };
        
        Plotly.newPlot('sentimentChart', data, layout);
    } catch (error) {
        console.error('Error updating chart:', error);
    }
} 