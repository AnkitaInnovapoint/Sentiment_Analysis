import os
from openai import OpenAI
from PIL import Image
import io
import base64

class AvatarGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Define avatar prompts for different sentiments
        self.sentiment_prompts = {
            'VERY_POSITIVE': "Create a cheerful, bright, and energetic avatar with a big smile and warm colors. The avatar should look extremely happy and positive.",
            'POSITIVE': "Create a friendly and optimistic avatar with a gentle smile and pleasant colors. The avatar should look happy and content.",
            'NEUTRAL': "Create a balanced and composed avatar with a calm expression and neutral colors. The avatar should look professional and collected.",
            'NEGATIVE': "Create a concerned and thoughtful avatar with a slightly worried expression and cooler colors. The avatar should look concerned but not extremely negative.",
            'VERY_NEGATIVE': "Create a serious and downcast avatar with a sad expression and dark colors. The avatar should look very concerned and negative."
        }

    def generate_avatar(self, sentiment_category):
        """
        Generate an avatar based on the sentiment category using DALL-E 3.
        
        Args:
            sentiment_category (str): The sentiment category (VERY_POSITIVE, POSITIVE, etc.)
            
        Returns:
            str: Base64 encoded image data
        """
        try:
            # Get the appropriate prompt for the sentiment
            prompt = self.sentiment_prompts.get(sentiment_category, self.sentiment_prompts['NEUTRAL'])
            
            # Generate image using DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                response_format="b64_json"
            )
            
            # Get the base64 image data
            image_data = response.data[0].b64_json
            
            return image_data
            
        except Exception as e:
            print(f"Error generating avatar: {str(e)}")
            return None

    def save_avatar(self, base64_data, filename):
        """
        Save the avatar image to a file.
        
        Args:
            base64_data (str): Base64 encoded image data
            filename (str): Name of the file to save
        """
        try:
            # Decode base64 data
            image_data = base64.b64decode(base64_data)
            
            # Create image from data
            image = Image.open(io.BytesIO(image_data))
            
            # Save image
            image.save(filename)
            
        except Exception as e:
            print(f"Error saving avatar: {str(e)}") 