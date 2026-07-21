<<<<<<< HEAD
# 🎵 Emotion-Based Music Recommendation App

A web application that detects your facial emotion in real-time using a webcam and recommends personalized songs based on your detected mood.

## 🎯 Features

- **Real-Time Emotion Detection**: Uses OpenCV and TensorFlow/Keras to detect emotions from webcam input
- **Multiple Frame Analysis**: Captures 30-40 frames (2-3 seconds) for accurate emotion detection
- **Smart Emotion Processing**: 
  - Collects multiple emotion predictions
  - Ranks emotions by frequency
  - Calculates confidence scores
  - Removes noise from detection
- **Personalized Music Recommendations**: Maps detected emotions to curated playlists
- **Beautiful Streamlit UI**: Simple, interactive, and user-friendly interface
- **Detailed Statistics**: View emotion distribution and detection metrics

## 🏗️ Project Structure

```
mini project/
├── app.py                      # Main Streamlit application
├── emotion_detector.py         # EmotionDetector class (OpenCV + ML model)
├── emotion_processor.py        # EmotionProcessor class (emotion analysis)
├── emotion_music_map.py        # Emotion-to-music mapping database
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam access
- Git (optional)

### Step 1: Clone the Repository
```bash
cd /Users/raristore/mini\ project
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.y
```

The app will open in your default browser at `http://localhost:8501`

## 📖 How to Use

1. **Prepare Your Setup**
   - Ensure good lighting
   - Position your face in front of the webcam
   - Keep a clear view of your face

2. **Start Detection**
   - Click the "🎬 Start Camera" button
   - The app will capture frames for 3 seconds (adjustable)

3. **View Results**
   - See your detected emotion
   - Get personalized song recommendations
   - View detection statistics and emotion distribution

4. **Explore Recommendations**
   - Each emotion maps to 5 curated songs
   - Songs include title, artist, and genre information
   - Use songs as music inspiration

5. **Reset for Next Session**
   - Click "🔄 Reset" to clear data
   - Start a new detection session

## 🧠 Emotion Classification

The app supports the following emotions:
- **Happy** → Pop, Dance, Uplifting music
- **Sad** → Slow, Acoustic, Reflective music
- **Angry** → Rock, Metal, Intense music
- **Neutral** → Chill, Lo-Fi, Ambient music
- **Surprise** → Energetic, Upbeat, Dynamic music
- **Fear** → Dark, Mysterious, Intense music
- **Disgust** → (Additional emotion support)

## ⚙️ Technical Details

### Emotion Detection Pipeline
```
Video Frame → Face Detection (Haar Cascade)
           → Face Cropping & Resizing (48x48)
           → Normalization
           → CNN Model Prediction
           → Emotion Classification
```

### Emotion Processing
```
Multiple Predictions → Frequency Analysis
                    → Confidence Scoring
                    → Duplicate Removal
                    → Ranking by Occurrence
```

### Key Classes

#### EmotionDetector
- Handles face detection using OpenCV Haar Cascades
- Loads/creates TensorFlow/Keras emotion classification model
- Predicts emotions from video frames
- Draws bounding boxes and labels on frames

#### EmotionProcessor
- Stores detected emotions and confidence scores
- Calculates emotion frequency distribution
- Generates statistics and summaries
- Converts data to pandas DataFrame for visualization

#### Music Recommendation Engine
- Maps emotions to curated song lists
- Provides detailed song metadata (title, artist, genre)
- Supports dynamic emotion-to-playlist mapping

## 🎚️ Configuration Options

In the sidebar, you can adjust:
- **Capture Duration** (1-10 seconds): How long to capture frames
- **Confidence Threshold** (0-1): Minimum confidence to accept predictions
- **Show Statistics**: Toggle statistics display
- **Show Live Video**: Toggle live video feed

## 📊 Metrics & Success Criteria

The app provides several metrics:
- **Total Frames Analyzed**: Number of frames processed
- **Unique Emotions**: Count of different emotions detected
- **Top Emotion**: Most frequently detected emotion
- **Average Confidence**: Mean confidence across all predictions
- **Emotion Distribution**: Breakdown by emotion type

## 🔮 Future Enhancements

As mentioned in the PRD, planned features include:
- ✨ Spotify API integration for direct music playback
- 🎬 YouTube auto-play for music videos
- 👤 User login and authentication system
- 💾 Save detected emotions and playlists
- 📱 Mobile app version
- 🤖 Advanced Deep Learning model for better accuracy
- 🌐 Multi-language support
- 🎨 Enhanced UI with more visualizations
- 📈 Emotion history tracking
- 🎯 Personalized recommendations based on listening history

## 🐛 Troubleshooting

### Issue: "Unable to access webcam"
- Check browser/application camera permissions
- Ensure no other app is using the camera
- Restart the application

### Issue: "Low emotion detection accuracy"
- Improve lighting conditions
- Move closer to the camera
- Ensure your face is centered
- Lower the confidence threshold
- Try multiple detection sessions

### Issue: "Model loading errors"
- Ensure TensorFlow is properly installed
- Try: `pip install --upgrade tensorflow`
- Check Python version (3.8+ required)

### Issue: "Streamlit not found"
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated

## 💻 System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: ~1GB for dependencies
- **Webcam**: Required for emotion detection

## 📝 Configuration Files

### requirements.txt
Contains all Python package dependencies:
- streamlit: Web UI framework
- opencv-python: Computer vision library
- numpy: Numerical computing
- pandas: Data manipulation
- tensorflow & keras: Deep learning frameworks
- pillow: Image processing

## 🔐 Privacy & Security

- **Local Processing**: All processing happens on your local machine
- **No Data Storage**: No videos or emotions are stored or uploaded
- **No Cloud Dependency**: Works completely offline after installation
- **Privacy First**: Your webcam feed is processed locally only

## 📄 License & Attribution

This is an educational project built for demonstration purposes.

## 👨‍💻 Developer Notes

### Key Implementation Details

1. **Emotion Detection Model**
   - Uses Haar Cascade Classifier for face detection
   - Implements a 7-layer CNN for emotion classification
   - Resizes faces to 48x48 pixels for processing
   - Normalizes pixel values to [0, 1] range

2. **Performance Optimization**
   - Processes at ~30 FPS
   - Uses NumPy for efficient matrix operations
   - Pandas for optimized data aggregation
   - Streamlit caching for faster reruns

3. **Error Handling**
   - Graceful camera access failures
   - Confidence threshold filtering
   - Face detection error management
   - Model prediction error handling

## 🤝 Contributing

To improve this project:
1. Fork the repository
2. Create a feature branch
3. Make improvements
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments
- Check Streamlit documentation: https://docs.streamlit.io
- OpenCV docs: https://docs.opencv.org

---

**Built with ❤️ using Streamlit, OpenCV, and TensorFlow**
=======
# MoodTunes-AI
The soundtrack to your state of mind
>>>>>>> 1cdde325bfaad3dce6b99232287beabf1d2c7632
