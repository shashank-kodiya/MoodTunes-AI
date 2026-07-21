# Advanced Features & Developer Guide

## 🚀 Advanced Features

### 1. Custom Emotion Model Training (Future Enhancement)

You can train your own emotion detection model using your dataset:

```python
from emotion_detector import EmotionDetector
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout

# Create custom model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(...) - Train with your data
model.save('my_emotion_model.h5')

# Use with detector
detector = EmotionDetector(model_path='my_emotion_model.h5')
```

### 2. Spotify Integration (Future Implementation)

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyRecommender:
    def __init__(self, client_id, client_secret):
        credentials = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)
    
    def get_playlist(self, emotion):
        """Search Spotify for playlists matching emotion"""
        results = self.sp.search(q=emotion, type='playlist', limit=5)
        return results['playlists']['items']
    
    def play_song(self, track_uri):
        """Play a track (requires user authentication)"""
        # Implementation for user playback control
        pass
```

### 3. Emotion History Tracking

```python
import json
from datetime import datetime

class EmotionHistory:
    def __init__(self, history_file='emotion_history.json'):
        self.history_file = history_file
        self.history = self._load_history()
    
    def record_session(self, emotions, recommendations):
        """Record an emotion detection session"""
        session = {
            'timestamp': datetime.now().isoformat(),
            'emotions': emotions,
            'top_emotion': emotions[0][0] if emotions else None,
            'recommendations': recommendations
        }
        self.history.append(session)
        self._save_history()
    
    def _load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_emotion_trends(self):
        """Analyze emotion trends over time"""
        emotion_counts = {}
        for session in self.history:
            emotion = session['top_emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        return emotion_counts
```

### 4. Advanced Face Detection Options

```python
# Using Deep Neural Network (more accurate but slower)
import cv2

class AdvancedEmotionDetector:
    def __init__(self):
        # Load DNN model for face detection
        self.model_path = "opencv_face_detector_uint8.pb"
        self.config_path = "opencv_face_detector.pbtxt"
        self.net = cv2.dnn.readNetFromTensorflow(self.model_path, self.config_path)
    
    def detect_faces_dnn(self, frame, confidence_threshold=0.5):
        """Detect faces using Deep Neural Network"""
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        self.net.setInput(blob)
        detections = self.net.forward()
        
        faces = []
        h, w = frame.shape[:2]
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > confidence_threshold:
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                x1, y1, x2, y2 = box.astype('int')
                faces.append((x1, y1, x2-x1, y2-y1))
        
        return faces
```

### 5. Real-time Performance Monitoring

```python
import time
from collections import deque

class PerformanceMonitor:
    def __init__(self, window_size=30):
        self.frame_times = deque(maxlen=window_size)
        self.detection_times = deque(maxlen=window_size)
    
    def start_frame(self):
        self.frame_start = time.time()
    
    def end_frame(self):
        self.frame_times.append(time.time() - self.frame_start)
    
    def record_detection(self, duration):
        self.detection_times.append(duration)
    
    @property
    def avg_fps(self):
        if not self.frame_times:
            return 0
        return 1.0 / (sum(self.frame_times) / len(self.frame_times))
    
    @property
    def avg_detection_time(self):
        if not self.detection_times:
            return 0
        return sum(self.detection_times) / len(self.detection_times) * 1000  # ms
```

## 🧪 Testing Guide

### Unit Tests

```python
# test_emotion_detector.py
import unittest
from emotion_detector import EmotionDetector
import numpy as np
import cv2

class TestEmotionDetector(unittest.TestCase):
    def setUp(self):
        self.detector = EmotionDetector()
    
    def test_detector_initialization(self):
        """Test detector initializes correctly"""
        self.assertIsNotNone(self.detector.face_cascade)
        self.assertIsNotNone(self.detector.model)
        self.assertEqual(len(self.detector.emotion_labels), 7)
    
    def test_emotion_detection(self):
        """Test emotion detection on a frame"""
        # Create dummy frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        emotion, confidence, box = self.detector.detect_emotion(frame)
        # Should return None for empty frame
        self.assertIsNone(emotion)
    
    def test_emotion_labels(self):
        """Test emotion labels are correct"""
        expected_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.assertEqual(self.detector.emotion_labels, expected_labels)
```

### Integration Tests

```python
# test_emotion_processor.py
import unittest
from emotion_processor import EmotionProcessor

class TestEmotionProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = EmotionProcessor()
    
    def test_add_emotion(self):
        """Test adding emotions"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        self.processor.add_emotion('sad', 0.7)
        
        self.assertEqual(len(self.processor.detected_emotions), 3)
    
    def test_get_top_emotion(self):
        """Test getting top emotion"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        self.processor.add_emotion('sad', 0.7)
        
        top_emotion, count = self.processor.get_top_emotion()
        self.assertEqual(top_emotion, 'happy')
        self.assertEqual(count, 2)
    
    def test_reset(self):
        """Test processor reset"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.reset()
        
        self.assertEqual(len(self.processor.detected_emotions), 0)
```

## 📊 Performance Optimization Tips

### 1. Reduce Resolution
Lower resolution frames process faster:
```python
frame = cv2.resize(frame, (320, 240))  # Process smaller frames
```

### 2. Frame Skipping
Process every Nth frame:
```python
frame_count = 0
if frame_count % 3 == 0:  # Process every 3rd frame
    emotion, conf, box = detector.detect_emotion(frame)
frame_count += 1
```

### 3. Multithreading
```python
from threading import Thread
from queue import Queue

def process_frames(frame_queue):
    while True:
        frame = frame_queue.get()
        emotion, conf, box = detector.detect_emotion(frame)
        # Handle result
        frame_queue.task_done()

thread = Thread(target=process_frames, args=(frame_queue,), daemon=True)
thread.start()
```

## 🔧 Customization Options

### Change Emotion-Music Mapping

Edit `emotion_music_map.py`:

```python
emotion_music_mapping['custom_emotion'] = {
    "mood": "Custom mood description",
    "songs": [
        {"title": "Song Title", "artist": "Artist Name", "genre": "Genre"},
        # Add more songs...
    ]
}
```

### Add More Emotions

To support more emotions, retrain the model with a larger dataset or modify:

```python
# In emotion_detector.py
self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'confused', 'interested']
# And retrain the model with additional labels
```

## 📈 Scaling the Application

### For Production Deployment

1. **Use a faster inference model**: TensorFlow Lite, ONNX, or quantized models
2. **Implement caching**: Cache emotion predictions
3. **Add error handling**: Graceful fallbacks for failures
4. **Database integration**: Store results in PostgreSQL/MongoDB
5. **API wrapper**: Create REST API with Flask/FastAPI
6. **Docker containerization**: Package app for easy deployment

### Example FastAPI Wrapper

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
from emotion_detector import EmotionDetector

app = FastAPI()
detector = EmotionDetector()

@app.post("/detect_emotion")
async def detect_emotion(frame_data: bytes):
    # Convert bytes to frame
    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), -1)
    
    # Detect emotion
    emotion, confidence, box = detector.detect_emotion(frame)
    
    return {
        "emotion": emotion,
        "confidence": float(confidence)
    }
```

---

**For more advanced techniques, refer to the main README.md and inline code comments.**
