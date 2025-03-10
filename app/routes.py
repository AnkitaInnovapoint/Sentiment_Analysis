from flask import Blueprint, render_template, request, jsonify
from app.models.feedback import Feedback
from app.utils.sentiment_analyzer import SentimentAnalyzer
from app.utils.avatar_generator import AvatarGenerator
from app.utils.video_generator import VideoGenerator
from app.utils.file_processor import process_csv
from app import db
import os
from datetime import datetime

main = Blueprint('main', __name__)
sentiment_analyzer = SentimentAnalyzer()
avatar_generator = AvatarGenerator()
video_generator = VideoGenerator()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get('text', '')
        department = data.get('department', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        # Analyze sentiment
        result = sentiment_analyzer.analyze_sentiment(text)
        
        if not result or 'error' in result:
            return jsonify({'error': 'Failed to analyze sentiment'}), 500
            
        # Generate avatar
        avatar_data = avatar_generator.generate_avatar(result['category'])
        
        # Generate video
        video_data = video_generator.generate_video(result['category'])
        
        # Save to database
        feedback = Feedback(
            text=text,
            department=department,
            sentiment=result['category'],
            score=result['score'],
            confidence=result['confidence']
        )
        db.session.add(feedback)
        db.session.commit()
        
        # Format response
        response = {
            'text': text,
            'category': result['category'],
            'emoji': result['emoji'],
            'description': result['description'],
            'score': round(result['score'], 3),
            'confidence': round(result['confidence'], 3),
            'department': department,
            'avatar': avatar_data,
            'video': video_data
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in analyze_sentiment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
            
        # Process CSV file
        feedback_data = process_csv(file)
        
        # Analyze sentiments
        results = sentiment_analyzer.analyze_bulk([item['feedback'] for item in feedback_data])
        
        # Save to database
        for item, result in zip(feedback_data, results):
            if not result or 'error' in result:
                continue
                
            feedback = Feedback(
                text=item['feedback'],
                department=item.get('department', ''),
                sentiment=result['category'],
                score=result['score'],
                confidence=result['confidence']
            )
            db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully processed {len(results)} feedback entries',
            'results': results
        })
        
    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/stats')
def get_stats():
    try:
        # Get all feedback
        feedbacks = Feedback.query.all()
        
        # Calculate statistics
        total = len(feedbacks)
        if total == 0:
            return jsonify({
                'total': 0,
                'average_score': 0,
                'sentiment_distribution': {}
            })
            
        # Calculate average score
        avg_score = sum(f.score for f in feedbacks) / total
        
        # Calculate sentiment distribution
        sentiment_dist = {}
        for feedback in feedbacks:
            sentiment_dist[feedback.sentiment] = sentiment_dist.get(feedback.sentiment, 0) + 1
            
        return jsonify({
            'total': total,
            'average_score': round(avg_score, 3),
            'sentiment_distribution': sentiment_dist
        })
        
    except Exception as e:
        print(f"Error in get_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500 