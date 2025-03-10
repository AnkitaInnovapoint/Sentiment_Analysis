from transformers import pipeline
import torch

class SentimentAnalyzer:
    def __init__(self):
        # Initialize the sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Define sentiment categories and their thresholds
        self.sentiment_categories = {
            'VERY_POSITIVE': {'min': 0.8, 'emoji': '😄', 'description': 'Very Positive'},
            'POSITIVE': {'min': 0.4, 'emoji': '🙂', 'description': 'Positive'},
            'NEUTRAL': {'min': -0.4, 'emoji': '😐', 'description': 'Neutral'},
            'NEGATIVE': {'min': -0.8, 'emoji': '🙁', 'description': 'Negative'},
            'VERY_NEGATIVE': {'min': float('-inf'), 'emoji': '😢', 'description': 'Very Negative'}
        }

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text using Hugging Face's transformers.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Dictionary containing sentiment analysis results
        """
        try:
            # Get sentiment analysis result
            result = self.sentiment_analyzer(text)[0]
            
            # Convert the score to our scale (-1 to 1)
            # Hugging Face returns a score between 0 and 1, where 1 is positive
            # We'll convert it to our -1 to 1 scale
            score = (result['score'] * 2) - 1 if result['label'] == 'POSITIVE' else -result['score'] * 2 + 1
            
            # Determine sentiment category
            category = self._get_sentiment_category(score)
            
            return {
                'text': text,
                'score': round(score, 3),
                'category': category,
                'emoji': self.sentiment_categories[category]['emoji'],
                'description': self.sentiment_categories[category]['description'],
                'confidence': round(result['score'], 3)
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return {
                'text': text,
                'score': 0,
                'category': 'NEUTRAL',
                'emoji': '😐',
                'description': 'Neutral',
                'confidence': 0
            }

    def _get_sentiment_category(self, score):
        """
        Determine the sentiment category based on the score.
        
        Args:
            score (float): The sentiment score between -1 and 1
            
        Returns:
            str: The sentiment category
        """
        for category, threshold in self.sentiment_categories.items():
            if score >= threshold['min']:
                return category
        return 'VERY_NEGATIVE'

    def analyze_bulk(self, texts):
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts (list): List of text strings to analyze
            
        Returns:
            list: List of sentiment analysis results
        """
        return [self.analyze_sentiment(text) for text in texts] 