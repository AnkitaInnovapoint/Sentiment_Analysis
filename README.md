# Employee Feedback Sentiment Analysis Dashboard

A web-based application that analyzes employee feedback using natural language processing to provide insights into employee sentiment across different departments.

## Features

- **Real-time Sentiment Analysis**: Instantly analyze employee feedback text
- **Bulk Analysis**: Upload CSV files containing multiple feedback entries
- **Department-wise Analysis**: Track sentiment across different departments
- **Interactive Visualization**: View sentiment distribution through interactive charts
- **User-friendly Interface**: Clean, modern UI with emoji indicators
- **Responsive Design**: Works on both desktop and mobile devices

## Demo Video
[Link to Demo Video]

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd sentiment_analysis
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Real-time Feedback Analysis
1. Enter employee feedback in the text area
2. (Optional) Select the department
3. Click "Analyze Sentiment"
4. View the sentiment analysis result with emoji indicator

### Bulk Analysis
1. Prepare a CSV file with the following columns:
   - `feedback`: The employee feedback text
   - `department`: The department name (optional)
2. Click "Choose File" and select your CSV file
3. Click "Upload and Analyze"
4. View the sentiment distribution chart

### Sample CSV Format
```csv
feedback,department
"I love working here!",HR
"The team is great!",IT
```

## Technical Details

### Backend
- **Framework**: Flask
- **Database**: SQLite
- **Sentiment Analysis**: Transformers (DistilBERT)
- **API Endpoints**:
  - `/analyze`: Real-time sentiment analysis
  - `/upload`: Bulk file processing
  - `/stats`: Sentiment statistics

### Frontend
- **Framework**: Bootstrap 5
- **Charts**: Plotly.js
- **Icons**: Font Awesome
- **Responsive Design**: Mobile-first approach

### Sentiment Categories
- Very Positive (😄)
- Positive (🙂)
- Neutral (😐)
- Negative (🙁)
- Very Negative (😢)

## Project Structure
```
sentiment_analysis/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   └── index.html
│   ├── models/
│   │   └── feedback.py
│   ├── utils/
│   │   ├── sentiment_analyzer.py
│   │   └── file_processor.py
│   ├── __init__.py
│   └── routes.py
├── requirements.txt
├── run.py
└── README.md
```

## Demo Data
A sample CSV file (`sample_feedback.csv`) is included in the repository for testing purposes. It contains:
- 15 different feedback entries
- Various departments
- Different sentiment levels
- Real-world scenarios

## Future Enhancements
1. Multi-language support
2. Advanced analytics dashboard
3. Department-wise trend analysis
4. Export functionality for reports
5. User authentication
6. API key integration for external services

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
[Your Contact Information]

## Acknowledgments
- Transformers for sentiment analysis
- Flask for the web framework
- Bootstrap for the UI components
- Plotly.js for visualizations 