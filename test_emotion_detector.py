"""
Unit tests for emotion detector module
"""
import unittest
import numpy as np
from emotion_detector import EmotionDetector


class TestEmotionDetector(unittest.TestCase):
    """Test cases for EmotionDetector class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = EmotionDetector()
    
    def test_detector_initialization(self):
        """Test that detector initializes with all components"""
        self.assertIsNotNone(self.detector.face_cascade, "Face cascade should not be None")
        self.assertIsNotNone(self.detector.model, "Model should not be None")
        self.assertIsNotNone(self.detector.emotion_labels, "Emotion labels should not be None")
    
    def test_emotion_labels_count(self):
        """Test that there are 7 emotion labels"""
        expected_count = 7
        actual_count = len(self.detector.emotion_labels)
        self.assertEqual(actual_count, expected_count, 
                        f"Expected {expected_count} emotions, got {actual_count}")
    
    def test_valid_emotion_labels(self):
        """Test that emotion labels are valid"""
        expected_labels = {'angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'}
        actual_labels = set(self.detector.emotion_labels)
        self.assertEqual(actual_labels, expected_labels, 
                        "Emotion labels do not match expected set")
    
    def test_detect_emotion_empty_frame(self):
        """Test emotion detection on empty frame returns None"""
        # Create a black frame (no face)
        empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        emotion, confidence, face_box = self.detector.detect_emotion(empty_frame)
        
        self.assertIsNone(emotion, "Should return None emotion for frame with no face")
        self.assertEqual(confidence, 0, "Should return 0 confidence for no face")
        self.assertIsNone(face_box, "Should return None face_box for frame with no face")
    
    def test_detect_emotion_frame_shape(self):
        """Test that detector handles different frame sizes"""
        # Test with different frame sizes
        sizes = [(480, 640, 3), (720, 1280, 3), (240, 320, 3)]
        
        for size in sizes:
            frame = np.zeros(size, dtype=np.uint8)
            try:
                emotion, confidence, box = self.detector.detect_emotion(frame)
                # Should not raise exception
                self.assertIsNotNone(emotion is None or isinstance(emotion, str))
            except Exception as e:
                self.fail(f"Detector should handle frame size {size}, but raised {e}")
    
    def test_draw_emotion_on_frame_with_face(self):
        """Test drawing emotion on frame with face detection"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        face_box = (100, 100, 80, 80)  # x, y, w, h
        
        result_frame = self.detector.draw_emotion_on_frame(
            frame, "happy", 0.95, face_box
        )
        
        self.assertIsNotNone(result_frame, "Should return a frame")
        self.assertEqual(result_frame.shape, frame.shape, "Frame shape should not change")
    
    def test_draw_emotion_on_frame_no_face(self):
        """Test drawing emotion on frame without face"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        result_frame = self.detector.draw_emotion_on_frame(
            frame, "happy", 0.95, None
        )
        
        self.assertIsNotNone(result_frame, "Should return original frame when no face")
        np.testing.assert_array_equal(result_frame, frame, 
                                      "Frame should be unchanged when no face box")
    
    def test_get_emotion_labels(self):
        """Test getting emotion labels"""
        labels = self.detector.get_emotion_labels()
        
        self.assertIsInstance(labels, list, "Should return a list")
        self.assertEqual(len(labels), 7, "Should have 7 labels")
        self.assertIn('happy', labels, "Should contain 'happy'")
        self.assertIn('sad', labels, "Should contain 'sad'")


class TestEmotionDetectorEdgeCases(unittest.TestCase):
    """Test edge cases for EmotionDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = EmotionDetector()
    
    def test_very_small_frame(self):
        """Test handling of very small frames"""
        small_frame = np.zeros((10, 10, 3), dtype=np.uint8)
        emotion, confidence, box = self.detector.detect_emotion(small_frame)
        
        # Should handle gracefully without crashing
        self.assertTrue(emotion is None or isinstance(emotion, str))
    
    def test_very_large_frame(self):
        """Test handling of very large frames"""
        large_frame = np.zeros((1440, 2560, 3), dtype=np.uint8)
        emotion, confidence, box = self.detector.detect_emotion(large_frame)
        
        # Should handle gracefully without crashing
        self.assertTrue(emotion is None or isinstance(emotion, str))
    
    def test_grayscale_frame_conversion(self):
        """Test that detector handles frame conversion properly"""
        # Create a simple frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        
        # Should not raise exception
        emotion, confidence, box = self.detector.detect_emotion(frame)
        self.assertTrue(emotion is None or isinstance(emotion, str))


if __name__ == '__main__':
    unittest.main()
