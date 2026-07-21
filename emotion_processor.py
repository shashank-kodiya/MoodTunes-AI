from collections import Counter
import pandas as pd

class EmotionProcessor:
    """Process and analyze detected emotions from multiple frames."""
    
    def __init__(self):
        """Initialize the emotion processor."""
        self.detected_emotions = []
        self.confidence_scores = []
    
    def add_emotion(self, emotion, confidence):
        """
        Add a detected emotion to the list.
        
        Args:
            emotion (str): Detected emotion
            confidence (float): Confidence score (0-1)
        """
        if emotion is not None:
            self.detected_emotions.append(emotion)
            self.confidence_scores.append(confidence)
    
    def get_emotion_frequency(self):
        """
        Get emotions ranked by frequency.
        
        Returns:
            list: List of (emotion, count) tuples sorted by count (descending)
        """
        if not self.detected_emotions:
            return []
        
        emotion_counts = Counter(self.detected_emotions)
        return sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
    
    def get_top_emotion(self):
        """
        Get the most frequently detected emotion.
        
        Returns:
            tuple: (emotion, count) or (None, 0) if no emotions detected
        """
        freq = self.get_emotion_frequency()
        if freq:
            return freq[0]
        return None, 0
    
    def get_emotion_stats(self):
        """
        Get statistics about detected emotions.
        
        Returns:
            dict: Dictionary with emotion statistics
        """
        if not self.detected_emotions:
            return {
                'total_frames': 0,
                'unique_emotions': 0,
                'top_emotion': None,
                'emotion_distribution': {},
                'average_confidence': 0
            }
        
        emotion_freq = dict(self.get_emotion_frequency())
        
        return {
            'total_frames': len(self.detected_emotions),
            'unique_emotions': len(emotion_freq),
            'top_emotion': self.get_top_emotion()[0],
            'emotion_distribution': emotion_freq,
            'average_confidence': sum(self.confidence_scores) / len(self.confidence_scores)
        }
    
    def get_emotion_dataframe(self):
        """
        Get emotions as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame with emotion and confidence data
        """
        if not self.detected_emotions:
            return pd.DataFrame(columns=['Emotion', 'Confidence', 'Count'])
        
        df = pd.DataFrame({
            'Emotion': self.detected_emotions,
            'Confidence': self.confidence_scores
        })
        
        emotion_counts = df.groupby('Emotion').size().reset_index(name='Count')
        emotion_counts['Avg_Confidence'] = df.groupby('Emotion')['Confidence'].mean().values
        
        return emotion_counts.sort_values('Count', ascending=False)
    
    def reset(self):
        """Reset the processor for a new detection session."""
        self.detected_emotions = []
        self.confidence_scores = []
    
    def get_summary(self):
        """
        Get a summary of emotion detection results.
        
        Returns:
            str: Human-readable summary
        """
        stats = self.get_emotion_stats()
        
        if stats['total_frames'] == 0:
            return "No emotions detected."
        
        summary = f"""
        === Emotion Detection Summary ===
        Total Frames Analyzed: {stats['total_frames']}
        Unique Emotions Detected: {stats['unique_emotions']}
        Top Emotion: {stats['top_emotion']}
        Average Confidence: {stats['average_confidence']:.2%}
        
        Emotion Distribution:
        """
        
        for emotion, count in stats['emotion_distribution'].items():
            percentage = (count / stats['total_frames']) * 100
            summary += f"\n  - {emotion.capitalize()}: {count} ({percentage:.1f}%)"
        
        return summary
