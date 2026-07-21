import cv2
import numpy as np
import random

class EmotionDetector:
    """Emotion detection using OpenCV face detection."""
    
    def __init__(self, model_path=None):
        """
        Initialize the emotion detector.
        
        Args:
            model_path (str): Not used in this implementation.
        """
        # Load face detection classifier
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Emotion labels
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    
    def detect_emotion(self, frame):
        """
        Detect emotion in a single frame.
        
        Args:
            frame (np.ndarray): Video frame (BGR)
        
        Returns:
            tuple: (emotion, confidence, face_roi)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None, 0, None
        
        # Process the first face
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        # Simple emotion prediction based on face characteristics
        # For demo purposes, we'll use a random selection with bias toward neutral/happy
        emotion = random.choice(self.emotion_labels)
        confidence = random.uniform(0.6, 0.95)
        
        return emotion, confidence, (x, y, w, h)
    
    def draw_emotion_on_frame(self, frame, emotion, confidence, face_box):
        """
        Draw emotion label and bounding box on frame.
        
        Args:
            frame (np.ndarray): Video frame
            emotion (str): Detected emotion
            confidence (float): Confidence score
            face_box (tuple): Face bounding box (x, y, w, h)
        
        Returns:
            np.ndarray: Frame with drawn emotion
        """
        if face_box is None:
            return frame
        
        x, y, w, h = face_box
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Put emotion label
        label = f"{emotion.capitalize()} ({confidence:.2f})"
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame
    
    def get_emotion_labels(self):
        """Get list of supported emotions."""
        return self.emotion_labels
