import os
from PIL import Image
import io
import base64
import numpy as np
import moviepy.editor as mpy

class VideoGenerator:
    def __init__(self):
        # Define paths for different sentiment images
        self.sentiment_images = {
            'VERY_POSITIVE': 'static/images/very_positive.jpg',
            'POSITIVE': 'static/images/positive.jpg',
            'NEUTRAL': 'static/images/neutral.jpg',
            'NEGATIVE': 'static/images/negative.jpg',
            'VERY_NEGATIVE': 'static/images/very_negative.jpg'
        }
        
        # Create static/images directory if it doesn't exist
        os.makedirs('static/images', exist_ok=True)

    def generate_video(self, sentiment_category, duration=4):
        """
        Generate a video based on the sentiment category using local images.
        
        Args:
            sentiment_category (str): The sentiment category
            duration (int): Duration of the video in seconds
            
        Returns:
            str: Base64 encoded video data
        """
        try:
            # Get the appropriate image path for the sentiment
            image_path = self.sentiment_images.get(sentiment_category, self.sentiment_images['NEUTRAL'])
            
            # Create a list of frames using the same image
            frames = []
            for _ in range(4):  # We'll use the same image 4 times
                with open(image_path, 'rb') as img_file:
                    img_data = img_file.read()
                    frames.append(base64.b64encode(img_data).decode('utf-8'))
            
            # Create video from frames
            video_data = self._create_video_from_frames(frames, duration)
            
            return video_data
            
        except Exception as e:
            print(f"Error generating video: {str(e)}")
            return None

    def _create_video_from_frames(self, frames, duration):
        """
        Create a video from a list of base64 encoded frames.
        
        Args:
            frames (list): List of base64 encoded image data
            duration (int): Duration of the video in seconds
            
        Returns:
            str: Base64 encoded video data
        """
        try:
            # Convert base64 frames to PIL Images
            pil_frames = []
            for frame in frames:
                image_data = base64.b64decode(frame)
                image = Image.open(io.BytesIO(image_data))
                pil_frames.append(image)
            
            # Create video clips from frames
            clips = []
            frame_duration = duration / len(frames)
            
            for frame in pil_frames:
                # Convert PIL Image to numpy array
                frame_array = np.array(frame)
                # Create video clip
                clip = mpy.ImageClip(frame_array).set_duration(frame_duration)
                clips.append(clip)
            
            # Concatenate clips
            final_clip = mpy.concatenate_videoclips(clips)
            
            # Write to temporary file
            temp_path = "temp_video.mp4"
            final_clip.write_videofile(temp_path, fps=24)
            
            # Read the video file and convert to base64
            with open(temp_path, "rb") as video_file:
                video_data = base64.b64encode(video_file.read()).decode('utf-8')
            
            # Clean up
            os.remove(temp_path)
            final_clip.close()
            
            return video_data
            
        except Exception as e:
            print(f"Error creating video: {str(e)}")
            return None

    def save_video(self, base64_data, filename):
        """
        Save the video to a file.
        
        Args:
            base64_data (str): Base64 encoded video data
            filename (str): Name of the file to save
        """
        try:
            # Decode base64 data
            video_data = base64.b64decode(base64_data)
            
            # Save video
            with open(filename, 'wb') as f:
                f.write(video_data)
            
        except Exception as e:
            print(f"Error saving video: {str(e)}") 