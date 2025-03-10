import pandas as pd
from app.utils.sentiment_analyzer import SentimentAnalyzer
from app import db
from app.models.feedback import Feedback
from datetime import datetime

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()

def process_excel(file):
    """
    Process Excel/CSV file containing feedback data.
    Expected columns: 'feedback', 'department' (optional)
    """
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Validate required columns
        if 'feedback' not in df.columns:
            raise ValueError("File must contain a 'feedback' column")

        # Process feedback texts
        texts = df['feedback'].tolist()
        departments = df['department'].tolist() if 'department' in df.columns else [None] * len(texts)

        # Analyze sentiments using Hugging Face
        results = sentiment_analyzer.analyze_bulk(texts)

        # Save to database
        for result, department in zip(results, departments):
            feedback = Feedback(
                text=result['text'],
                sentiment=result['category'],
                score=result['score'],
                confidence=result['confidence'],
                department=department,
                timestamp=datetime.utcnow()
            )
            db.session.add(feedback)
        
        db.session.commit()

        return {
            'message': f'Successfully processed {len(results)} feedback entries',
            'results': results
        }

    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

def process_google_form(form_data):
    """
    Process feedback data from Google Forms.
    Expected format: {'feedback': text, 'department': department}
    """
    try:
        result = sentiment_analyzer.analyze_sentiment(form_data['feedback'])
        
        feedback = Feedback(
            text=result['text'],
            sentiment=result['category'],
            score=result['score'],
            confidence=result['confidence'],
            department=form_data.get('department'),
            timestamp=datetime.utcnow()
        )
        db.session.add(feedback)
        db.session.commit()

        return {
            'message': 'Successfully processed feedback',
            'result': result
        }

    except Exception as e:
        raise Exception(f"Error processing Google Form data: {str(e)}")

def process_csv(file):
    """
    Process a CSV file containing employee feedback.
    
    Args:
        file: FileStorage object containing the CSV file
        
    Returns:
        list: List of dictionaries containing feedback data
    """
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate required columns
        if 'feedback' not in df.columns:
            raise ValueError("CSV file must contain a 'feedback' column")
            
        # Convert to list of dictionaries
        feedback_data = []
        for _, row in df.iterrows():
            feedback_data.append({
                'feedback': str(row['feedback']),
                'department': str(row.get('department', ''))
            })
            
        return feedback_data
        
    except Exception as e:
        raise Exception(f"Error processing CSV file: {str(e)}") 