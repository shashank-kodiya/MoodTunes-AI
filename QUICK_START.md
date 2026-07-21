# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Webcam access

### Installation

#### Option 1: Using the Setup Script (Recommended for macOS/Linux)

```bash
# Navigate to project directory
cd "/Users/raristore/mini project"

# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh

# Activate virtual environment (if not already done)
source venv/bin/activate

# Start the app
streamlit run app.py
```

#### Option 2: Manual Installation

```bash
# Navigate to project directory
cd "/Users/raristore/mini project"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Start the app
streamlit run app.py
```

#### Option 3: Quick Install (Without Virtual Environment)

```bash
# Navigate to project directory
cd "/Users/raristore/mini project"

# Install dependencies globally
pip install -r requirements.txt

# Start the app
streamlit run app.py
```

### First Run

1. **App Opens**: The app will automatically open in your browser at `http://localhost:8501`
2. **Grant Permissions**: Allow browser access to your webcam when prompted
3. **Check Lighting**: Ensure you have good lighting and your face is visible
4. **Start Detection**: Click the "🎬 Start Camera" button
5. **View Results**: See your emotion and get music recommendations!

## 📱 Using the App

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🎵 Emotion-Based Music Recommendation App                   │
│ Detect Your Mood and Get Personalized Song Recommendations  │
├──────────────────┬──────────────────────────────────────────┤
│ 📹 Emotion       │ 🎶 Music Recommendations               │
│ Detection        │                                          │
│                  │ Detected Emotion: HAPPY                │
│ [🎬 Start]       │ Mood: Happy and Uplifting             │
│ [🔄 Reset]       │                                        │
│ [📊 Analyze]     │ 1. Walking on Sunshine                │
│                  │    Katrina & The Waves | Pop          │
│ Live Video Feed  │                                        │
│                  │ 2. Good as Hell                       │
│                  │    Lizzo | Pop                        │
├──────────────────┴──────────────────────────────────────────┤
│ 📊 Detection Statistics                                     │
│ Frames: 45 | Emotions: 3 | Top: Happy | Confidence: 87.5% │
└────────────────────────────────────────────────────────────┘
```

### Step-by-Step Usage

**Step 1: Prepare**
- Sit in front of your webcam
- Ensure good lighting
- Keep your face centered in the frame

**Step 2: Start**
- Click "🎬 Start Camera" button
- The app begins capturing video

**Step 3: React Naturally**
- Make natural expressions for 2-3 seconds
- Let the AI analyze multiple frames
- Blink normally - no special actions needed

**Step 4: View Results**
- See your detected emotion in large text
- Get 5 personalized song recommendations
- View statistics about the detection

**Step 5: Reset (Optional)**
- Click "🔄 Reset" to clear results
- Start a new detection session

## ⚙️ Configuration

### Sidebar Settings

**Capture Duration**: 1-10 seconds
- Longer duration = more frames = better accuracy
- Default: 3 seconds (good balance)

**Confidence Threshold**: 0-1.0
- Higher = stricter filtering
- Default: 0.5 (50% confidence)
- Lower threshold = more predictions accepted

**Show Statistics**: Toggle to show/hide stats
**Show Live Video**: Toggle to show/hide camera feed

## 🔧 Troubleshooting

### Camera Won't Work

```bash
# Check if streamlit can access camera
# Try restarting the app
streamlit run app.py

# On macOS, check System Preferences:
# Settings > Security & Privacy > Camera > Allow Streamlit
```

### Poor Emotion Detection

**Solutions**:
1. Improve lighting (bright but not glaring)
2. Move closer to camera (face should be prominent)
3. Lower confidence threshold in sidebar
4. Make more expressive expressions
5. Try multiple detection sessions

### Dependencies Won't Install

```bash
# Update pip first
python3 -m pip install --upgrade pip

# Try installing with specific versions
pip install -r requirements.txt --no-cache-dir

# If TensorFlow fails, install CPU version:
pip install tensorflow-cpu
```

### "No emotions detected" Message

- Lower the Confidence Threshold slider
- Improve lighting conditions
- Ensure face is clearly visible
- Try more expressive expressions

## 📚 File Structure

```
mini project/
├── app.py                           # Main Streamlit app
├── emotion_detector.py              # Face & emotion detection
├── emotion_processor.py             # Emotion analysis logic
├── emotion_music_map.py             # Emotion-to-songs mapping
├── requirements.txt                 # Python dependencies
├── config.ini                       # Configuration settings
├── README.md                        # Full documentation
├── ADVANCED_FEATURES.md             # Advanced usage
├── QUICK_START.md                   # This file
├── setup.sh                         # Setup script
├── test_emotion_detector.py         # Detector tests
├── test_emotion_processor.py        # Processor tests
└── test_emotion_music_map.py        # Mapping tests
```

## 🎯 Common Tasks

### Run Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m unittest discover -s . -p "test_*.py" -v

# Run specific test file
python -m unittest test_emotion_processor -v

# Run specific test
python -m unittest test_emotion_processor.TestEmotionProcessor.test_add_emotion -v
```

### View Logs

```bash
# Streamlit logs (if configured)
tail -f logs/app.log
```

### Change Music Recommendations

Edit `emotion_music_map.py`:
```python
emotion_music_mapping['happy']['songs'] = [
    {"title": "Your Song", "artist": "Your Artist", "genre": "Genre"},
    # Add more songs...
]
```

### Add New Emotions

1. Edit `emotion_detector.py` - update `emotion_labels`
2. Edit `emotion_music_map.py` - add new emotion mapping
3. Retrain the model if using custom dataset

## 🌐 Accessing from Other Devices

Share the app with others on your network:

```bash
# Find your IP address
ipconfig getifaddr en0  # On macOS

# Run streamlit with network access
streamlit run app.py --server.address=0.0.0.0

# Other users access via:
# http://<your-ip>:8501
```

## 📊 Understanding Results

### Emotion Distribution
- Shows percentage of each emotion detected
- More frames = more accurate representation
- Ties mean mixed emotions detected

### Average Confidence
- Higher = more certain predictions
- 100% = very confident
- < 50% = less confident (lower threshold)

### Top Emotion
- Most frequently detected emotion
- Used for music recommendations
- Breaks ties by first occurrence

## 🎓 Learning & Extending

### Modify UI
Edit `app.py` - Streamlit components are well-commented

### Add Features
1. Add new buttons/sliders in sidebar
2. Modify emotion detection parameters
3. Extend music recommendations
4. Add new visualization types

### Improve Accuracy
- Collect more training data
- Fine-tune the neural network
- Use better face detection model

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed without errors
- [ ] App runs: `streamlit run app.py`
- [ ] Browser opens automatically
- [ ] Camera permission granted
- [ ] "Start Camera" button works
- [ ] Emotion detected in < 5 seconds
- [ ] Song recommendations appear
- [ ] Statistics display correctly

## 🆘 Getting Help

1. **Check README.md** - Comprehensive documentation
2. **Check ADVANCED_FEATURES.md** - Advanced topics
3. **Review code comments** - Well-documented code
4. **Run tests** - See what's working
5. **Check error messages** - Clear error descriptions

## 🎉 You're Ready!

Now you can:
✨ Detect emotions from your face in real-time
🎵 Get personalized music recommendations
📊 View detailed statistics and insights
🔄 Reset and try again with different expressions

Enjoy exploring your emotions and discovering new music! 🎶

---

**Need more help?** Check [README.md](README.md) or [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)
