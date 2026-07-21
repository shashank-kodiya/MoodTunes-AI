# Development Guidelines & Best Practices

## 📋 Development Standards

This document outlines best practices and guidelines for developing and extending the Emotion-Based Music Recommendation App.

## 🎯 Code Quality Standards

### Python Style
- **Standard**: PEP 8
- **Line Length**: 88 characters (Black formatter)
- **Imports**: Group imports (stdlib, third-party, local)
- **Naming**: snake_case for functions/variables, PascalCase for classes

### Example
```python
import os
import sys
from datetime import datetime

import cv2
import numpy as np
import streamlit as st

from emotion_detector import EmotionDetector
from emotion_processor import EmotionProcessor
```

### Docstring Format
Use Google-style docstrings:

```python
def detect_emotion(self, frame):
    """
    Detect emotion in a single frame.
    
    Analyzes facial features in the provided frame to predict the
    most likely emotion. Uses Haar Cascade for face detection and
    a pre-trained CNN for emotion classification.
    
    Args:
        frame (np.ndarray): Video frame in BGR format with shape (H, W, 3)
    
    Returns:
        tuple: A tuple containing:
            - emotion (str): Detected emotion name or None if no face
            - confidence (float): Confidence score between 0 and 1
            - face_roi (tuple): Face bounding box (x, y, w, h) or None
    
    Raises:
        ValueError: If frame is not BGR format
        RuntimeError: If model fails to predict
    
    Example:
        >>> frame = cv2.imread('face.jpg')
        >>> emotion, conf, box = detector.detect_emotion(frame)
        >>> print(f"{emotion}: {conf:.2%}")
        happy: 95.32%
    
    Note:
        Frame should have good lighting and visible face for accuracy.
        Model accuracy depends on training data and face visibility.
    """
    # Implementation...
```

### Type Hints
Use type hints for better code documentation:

```python
from typing import Tuple, Optional, List, Dict

def add_emotion(self, emotion: Optional[str], confidence: float) -> None:
    """Add an emotion prediction to the list."""
    if emotion is not None:
        self.detected_emotions.append(emotion)
        self.confidence_scores.append(confidence)

def get_top_emotion(self) -> Tuple[Optional[str], int]:
    """Get the most frequently detected emotion."""
    freq = self.get_emotion_frequency()
    if freq:
        return freq[0]
    return None, 0
```

## 🧪 Testing Guidelines

### Test Structure
```python
import unittest
from module_to_test import ClassToTest

class TestClassName(unittest.TestCase):
    """Test cases for ClassName."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.obj = ClassToTest()
    
    def tearDown(self):
        """Clean up after each test."""
        # Cleanup code if needed
        pass
    
    def test_normal_case(self):
        """Test normal operation."""
        result = self.obj.method()
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Test boundary conditions."""
        result = self.obj.method(edge_value)
        self.assertTrue(condition)
    
    def test_error_case(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            self.obj.method(invalid_input)
```

### Test Coverage
- **Target**: >80% code coverage
- **Tools**: `coverage.py`

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover
coverage report
coverage html  # Generate HTML report
```

### Test Naming Convention
- Test files: `test_module_name.py`
- Test classes: `Test{ClassName}`
- Test methods: `test_{feature}_{scenario}`

Examples:
```
✅ test_emotion_detector.py
✅ class TestEmotionDetector(unittest.TestCase)
✅ def test_detect_emotion_with_face(self)
✅ def test_detect_emotion_without_face(self)
✅ def test_draw_emotion_on_frame_valid_box(self)
```

## 📁 File Organization

### Directory Structure
```
mini project/
├── /src                    # Main source code
│   ├── app.py
│   ├── emotion_detector.py
│   └── emotion_processor.py
├── /tests                  # Test files
│   ├── test_detector.py
│   └── test_processor.py
├── /docs                   # Documentation
│   └── *.md
├── /models                 # Pre-trained models
│   └── emotion_model.h5
├── /data                   # Data files
│   └── songs.json
└── requirements.txt
```

### Module Organization
Keep modules focused and single-purpose:
- `emotion_detector.py`: Only face & emotion detection
- `emotion_processor.py`: Only emotion analysis
- `emotion_music_map.py`: Only music mapping
- `app.py`: Only UI and orchestration

## 🔄 Git Workflow

### Branch Naming
```
feature/add-spotify-integration
bugfix/fix-camera-access
docs/update-readme
test/add-detector-tests
refactor/optimize-inference
```

### Commit Messages
```
# Format: <type>: <subject>
# Types: feat, fix, docs, style, refactor, test, chore

feat: add emotion history tracking
fix: handle missing face detection gracefully
docs: add deployment guide
test: increase test coverage to 85%
refactor: simplify emotion processing logic
chore: update dependencies
```

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings
```

## 🚀 Performance Guidelines

### Code Optimization

#### ✅ Good Practices
```python
# Use list comprehension instead of loops
emotions_upper = [e.upper() for e in emotions]

# Use built-in functions
total = sum(scores)
avg = sum(scores) / len(scores)

# Cache expensive operations
@st.cache_resource
def load_detector():
    return EmotionDetector()

# Avoid unnecessary copies
emotion_list = np.array(data, copy=False)
```

#### ❌ Avoid
```python
# Inefficient loop
emotions_upper = []
for emotion in emotions:
    emotions_upper.append(emotion.upper())

# Recalculating in loop
for i in range(n):
    total = sum(scores)  # Calculate each iteration

# Inefficient string operations
result = ""
for char in string:
    result += char  # Creates new string each time
```

### Profiling

```python
# Profile function execution
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
detector.detect_emotion(frame)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

## 🛡️ Security Best Practices

### Input Validation
```python
def add_emotion(self, emotion: Optional[str], confidence: float) -> None:
    """Validate inputs before processing."""
    # Check types
    if emotion is not None and not isinstance(emotion, str):
        raise TypeError(f"emotion must be str, got {type(emotion)}")
    
    if not isinstance(confidence, (int, float)):
        raise TypeError(f"confidence must be float, got {type(confidence)}")
    
    # Check ranges
    if confidence < 0 or confidence > 1:
        raise ValueError(f"confidence must be in [0, 1], got {confidence}")
    
    # Sanitize input
    emotion = emotion.lower().strip() if emotion else None
    
    # Proceed with valid input
    if emotion is not None:
        self.detected_emotions.append(emotion)
        self.confidence_scores.append(confidence)
```

### Error Handling
```python
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera")
    
    frame = cap.read()
    if frame is None:
        raise ValueError("Failed to read frame")
    
except RuntimeError as e:
    logger.error(f"Camera error: {e}")
    st.error(f"❌ Camera error: {e}")
except ValueError as e:
    logger.warning(f"Frame error: {e}")
    continue
finally:
    if 'cap' in locals():
        cap.release()
```

## 📊 Logging Standards

### Setup Logging
```python
import logging
import logging.handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Log Levels
```python
logger.debug("Detailed information for debugging")
logger.info("General information about app state")
logger.warning("Warning about potential issues")
logger.error("Error occurred but app continues")
logger.critical("Critical error, app may fail")
```

### Good Logging Practices
```python
# ✅ Good: Informative and structured
logger.info(f"Detected {len(emotions)} emotions, top: {top_emotion}")
logger.error(f"Face detection failed: {error_msg}", exc_info=True)

# ❌ Bad: Vague or excessive
logger.info("Something happened")
logger.debug(f"Frame: {frame}")  # Don't log large objects
```

## 🔧 Configuration Management

### Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.5'))
MODEL_PATH = os.getenv('MODEL_PATH', 'default_model.h5')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

### Configuration File
```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access configuration
threshold = config.getfloat('emotion_detection', 'confidence_threshold')
capture_duration = config.getint('video_capture', 'default_capture_duration')
```

## 📚 Documentation Standards

### Docstring Examples
Every function should have:
1. One-line summary
2. Detailed description (if needed)
3. Args section
4. Returns section
5. Raises section (if applicable)
6. Example usage (if helpful)

### Inline Comments
```python
# Use comments for WHY, not WHAT
# ✅ Why are we filtering by confidence?
# The model can be uncertain, so we only accept predictions with high confidence
if confidence > THRESHOLD:
    predictions.append(emotion)

# ❌ Don't repeat what code obviously does
# confidence > THRESHOLD means confidence is greater than threshold
if confidence > THRESHOLD:  # This is obvious!
```

## 🎓 Code Review Checklist

Before submitting code, verify:

- [ ] **Style**: Follows PEP 8
- [ ] **Documentation**: Docstrings and comments added
- [ ] **Testing**: New tests for new code
- [ ] **Performance**: No obvious inefficiencies
- [ ] **Security**: Input validation, error handling
- [ ] **Compatibility**: Works with Python 3.8+
- [ ] **Dependencies**: All imports available
- [ ] **Logging**: Appropriate log levels used
- [ ] **Error Handling**: Graceful failure
- [ ] **Type Hints**: Used where helpful

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] All tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No debug code remaining
- [ ] Logging configured properly
- [ ] Environment variables set
- [ ] Performance tested
- [ ] Security audit done
- [ ] Backups in place
- [ ] Rollback plan ready

## 📈 Common Refactoring Patterns

### Extracting Methods
```python
# Before: Large method doing multiple things
def process_emotion(emotion, confidence):
    if emotion and confidence > 0.5:
        emotion_upper = emotion.upper()
        recommendation = get_music(emotion_upper)
        return recommendation

# After: Extracted validation
def is_valid_prediction(emotion, confidence):
    return emotion is not None and confidence > 0.5

def process_emotion(emotion, confidence):
    if is_valid_prediction(emotion, confidence):
        recommendation = get_music(emotion.upper())
        return recommendation
```

### Reducing Complexity
```python
# Before: Multiple nested conditions
if emotion:
    if confidence > 0.5:
        if emotion in mapping:
            result = mapping[emotion]
        else:
            result = default

# After: Guard clauses
if not emotion or confidence <= 0.5:
    return default
if emotion not in mapping:
    return default
return mapping[emotion]
```

## 🎯 Performance Benchmarks

Track these metrics:
- **Detection latency**: < 200ms per frame
- **FPS**: > 5 frames per second
- **Memory usage**: < 1GB peak
- **CPU usage**: < 50% average
- **Test execution**: < 5 seconds total

## 📞 Getting Help

### Resources
- Code: Review similar implementations
- Docs: Read inline comments and docstrings
- Tests: Check test cases for usage examples
- Issues: Search closed issues for solutions
- Community: Ask in Streamlit/TensorFlow communities

---

**Remember**: Good code is:
✅ Readable and well-documented
✅ Tested and reliable
✅ Efficient and performant
✅ Secure and error-resilient
✅ Maintainable and extensible

**Happy coding! 🚀**
