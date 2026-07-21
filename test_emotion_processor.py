"""
Unit tests for emotion processor module
"""
import unittest
import pandas as pd
from emotion_processor import EmotionProcessor


class TestEmotionProcessor(unittest.TestCase):
    """Test cases for EmotionProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = EmotionProcessor()
    
    def test_initialization(self):
        """Test processor initializes correctly"""
        self.assertEqual(len(self.processor.detected_emotions), 0, 
                        "Should start with empty emotions list")
        self.assertEqual(len(self.processor.confidence_scores), 0, 
                        "Should start with empty confidence list")
    
    def test_add_single_emotion(self):
        """Test adding a single emotion"""
        self.processor.add_emotion('happy', 0.95)
        
        self.assertEqual(len(self.processor.detected_emotions), 1, 
                        "Should have 1 emotion")
        self.assertEqual(self.processor.detected_emotions[0], 'happy', 
                        "First emotion should be 'happy'")
        self.assertEqual(self.processor.confidence_scores[0], 0.95, 
                        "Confidence should be 0.95")
    
    def test_add_multiple_emotions(self):
        """Test adding multiple emotions"""
        emotions = [('happy', 0.9), ('happy', 0.85), ('sad', 0.7), ('happy', 0.92)]
        
        for emotion, confidence in emotions:
            self.processor.add_emotion(emotion, confidence)
        
        self.assertEqual(len(self.processor.detected_emotions), 4, 
                        "Should have 4 emotions")
    
    def test_add_none_emotion(self):
        """Test that None emotions are not added"""
        self.processor.add_emotion(None, 0.5)
        
        self.assertEqual(len(self.processor.detected_emotions), 0, 
                        "Should not add None emotions")
    
    def test_get_emotion_frequency(self):
        """Test getting emotion frequency"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        self.processor.add_emotion('sad', 0.7)
        
        frequency = self.processor.get_emotion_frequency()
        
        self.assertEqual(len(frequency), 2, "Should have 2 unique emotions")
        self.assertEqual(frequency[0][0], 'happy', "Happy should be first (most frequent)")
        self.assertEqual(frequency[0][1], 2, "Happy should appear 2 times")
        self.assertEqual(frequency[1][0], 'sad', "Sad should be second")
        self.assertEqual(frequency[1][1], 1, "Sad should appear 1 time")
    
    def test_get_top_emotion(self):
        """Test getting the top emotion"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        self.processor.add_emotion('sad', 0.7)
        
        top_emotion, count = self.processor.get_top_emotion()
        
        self.assertEqual(top_emotion, 'happy', "Top emotion should be 'happy'")
        self.assertEqual(count, 2, "Happy should have count of 2")
    
    def test_get_top_emotion_empty(self):
        """Test getting top emotion when list is empty"""
        top_emotion, count = self.processor.get_top_emotion()
        
        self.assertIsNone(top_emotion, "Should return None for empty list")
        self.assertEqual(count, 0, "Should return 0 count for empty list")
    
    def test_get_emotion_stats(self):
        """Test getting emotion statistics"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        self.processor.add_emotion('sad', 0.7)
        
        stats = self.processor.get_emotion_stats()
        
        self.assertEqual(stats['total_frames'], 3, "Should have 3 total frames")
        self.assertEqual(stats['unique_emotions'], 2, "Should have 2 unique emotions")
        self.assertEqual(stats['top_emotion'], 'happy', "Top emotion should be happy")
        self.assertGreater(stats['average_confidence'], 0, 
                          "Average confidence should be positive")
        self.assertIn('happy', stats['emotion_distribution'], 
                     "Emotion distribution should have 'happy'")
    
    def test_get_emotion_stats_empty(self):
        """Test getting stats for empty processor"""
        stats = self.processor.get_emotion_stats()
        
        self.assertEqual(stats['total_frames'], 0, "Empty processor should have 0 frames")
        self.assertEqual(stats['average_confidence'], 0, "Empty processor should have 0 confidence")
    
    def test_get_emotion_dataframe(self):
        """Test converting emotions to DataFrame"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        self.processor.add_emotion('sad', 0.7)
        
        df = self.processor.get_emotion_dataframe()
        
        self.assertIsInstance(df, pd.DataFrame, "Should return a DataFrame")
        self.assertGreater(len(df), 0, "DataFrame should not be empty")
        self.assertIn('Emotion', df.columns, "DataFrame should have 'Emotion' column")
        self.assertIn('Count', df.columns, "DataFrame should have 'Count' column")
    
    def test_get_emotion_dataframe_empty(self):
        """Test converting empty processor to DataFrame"""
        df = self.processor.get_emotion_dataframe()
        
        self.assertIsInstance(df, pd.DataFrame, "Should return a DataFrame")
        self.assertEqual(len(df), 0, "Empty processor should return empty DataFrame")
    
    def test_reset(self):
        """Test resetting the processor"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('sad', 0.7)
        
        self.processor.reset()
        
        self.assertEqual(len(self.processor.detected_emotions), 0, 
                        "Should have 0 emotions after reset")
        self.assertEqual(len(self.processor.confidence_scores), 0, 
                        "Should have 0 confidence scores after reset")
    
    def test_get_summary(self):
        """Test getting a summary string"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.85)
        
        summary = self.processor.get_summary()
        
        self.assertIsInstance(summary, str, "Should return a string")
        self.assertIn('happy', summary.lower(), "Summary should mention 'happy'")
        self.assertIn('2', summary, "Summary should mention frame count")
    
    def test_get_summary_empty(self):
        """Test getting summary for empty processor"""
        summary = self.processor.get_summary()
        
        self.assertIn('No emotions detected', summary, 
                     "Empty processor summary should mention no emotions")


class TestEmotionProcessorStatistics(unittest.TestCase):
    """Test statistics calculation for EmotionProcessor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = EmotionProcessor()
    
    def test_confidence_calculation(self):
        """Test that average confidence is calculated correctly"""
        self.processor.add_emotion('happy', 0.8)
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('happy', 0.7)
        
        stats = self.processor.get_emotion_stats()
        expected_avg = (0.8 + 0.9 + 0.7) / 3
        
        self.assertAlmostEqual(stats['average_confidence'], expected_avg, places=5, 
                              msg="Average confidence calculation is incorrect")
    
    def test_emotion_distribution_percentages(self):
        """Test emotion distribution calculation"""
        # Add 7 happy and 3 sad emotions
        for _ in range(7):
            self.processor.add_emotion('happy', 0.9)
        for _ in range(3):
            self.processor.add_emotion('sad', 0.7)
        
        stats = self.processor.get_emotion_stats()
        
        self.assertEqual(stats['emotion_distribution']['happy'], 7, 
                        "Happy count should be 7")
        self.assertEqual(stats['emotion_distribution']['sad'], 3, 
                        "Sad count should be 3")
    
    def test_tie_in_emotion_frequency(self):
        """Test handling of tie in emotion frequency"""
        self.processor.add_emotion('happy', 0.9)
        self.processor.add_emotion('sad', 0.7)
        
        frequency = self.processor.get_emotion_frequency()
        
        # Both should appear once, order may vary but both should be present
        self.assertEqual(len(frequency), 2, "Should have 2 emotions")
        emotions = {item[0] for item in frequency}
        self.assertEqual(emotions, {'happy', 'sad'}, "Should contain both emotions")


if __name__ == '__main__':
    unittest.main()
