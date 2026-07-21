"""
Unit tests for emotion-to-music mapping
"""
import unittest
from emotion_music_map import get_recommendations, get_all_emotions


class TestEmotionMusicMapping(unittest.TestCase):
    """Test cases for emotion to music mapping"""
    
    def test_get_recommendations_happy(self):
        """Test getting recommendations for happy emotion"""
        recommendations = get_recommendations('happy')
        
        self.assertIn('mood', recommendations, "Should have 'mood' key")
        self.assertIn('songs', recommendations, "Should have 'songs' key")
        self.assertEqual(len(recommendations['songs']), 5, "Should have 5 songs")
        self.assertEqual(recommendations['mood'], 'Happy and Uplifting', 
                        "Mood should be 'Happy and Uplifting'")
    
    def test_get_recommendations_sad(self):
        """Test getting recommendations for sad emotion"""
        recommendations = get_recommendations('sad')
        
        self.assertIn('mood', recommendations, "Should have 'mood' key")
        self.assertIn('songs', recommendations, "Should have 'songs' key")
        self.assertEqual(len(recommendations['songs']), 5, "Should have 5 songs")
    
    def test_get_recommendations_angry(self):
        """Test getting recommendations for angry emotion"""
        recommendations = get_recommendations('angry')
        
        self.assertIn('mood', recommendations, "Should have 'mood' key")
        self.assertIn('songs', recommendations, "Should have 'songs' key")
        self.assertEqual(len(recommendations['songs']), 5, "Should have 5 songs")
    
    def test_get_recommendations_neutral(self):
        """Test getting recommendations for neutral emotion"""
        recommendations = get_recommendations('neutral')
        
        self.assertIn('mood', recommendations, "Should have 'mood' key")
        self.assertIn('songs', recommendations, "Should have 'songs' key")
        self.assertEqual(len(recommendations['songs']), 5, "Should have 5 songs")
    
    def test_get_recommendations_surprise(self):
        """Test getting recommendations for surprise emotion"""
        recommendations = get_recommendations('surprise')
        
        self.assertIn('mood', recommendations, "Should have 'mood' key")
        self.assertIn('songs', recommendations, "Should have 'songs' key")
        self.assertEqual(len(recommendations['songs']), 5, "Should have 5 songs")
    
    def test_get_recommendations_fear(self):
        """Test getting recommendations for fear emotion"""
        recommendations = get_recommendations('fear')
        
        self.assertIn('mood', recommendations, "Should have 'mood' key")
        self.assertIn('songs', recommendations, "Should have 'songs' key")
        self.assertEqual(len(recommendations['songs']), 5, "Should have 5 songs")
    
    def test_get_recommendations_invalid_emotion(self):
        """Test getting recommendations for invalid emotion"""
        recommendations = get_recommendations('invalid_emotion')
        
        # Should default to neutral
        self.assertEqual(recommendations['mood'], 'Calm and Relaxing', 
                        "Should default to neutral mood")
    
    def test_song_structure(self):
        """Test that songs have correct structure"""
        recommendations = get_recommendations('happy')
        songs = recommendations['songs']
        
        for song in songs:
            self.assertIn('title', song, "Song should have 'title'")
            self.assertIn('artist', song, "Song should have 'artist'")
            self.assertIn('genre', song, "Song should have 'genre'")
            self.assertIsInstance(song['title'], str, "Title should be string")
            self.assertIsInstance(song['artist'], str, "Artist should be string")
            self.assertIsInstance(song['genre'], str, "Genre should be string")
    
    def test_get_recommendations_case_insensitive(self):
        """Test that emotion names are case-insensitive"""
        rec1 = get_recommendations('happy')
        rec2 = get_recommendations('HAPPY')
        rec3 = get_recommendations('Happy')
        
        self.assertEqual(rec1['mood'], rec2['mood'], 
                        "Should handle uppercase emotion")
        self.assertEqual(rec1['mood'], rec3['mood'], 
                        "Should handle mixed case emotion")
    
    def test_get_all_emotions(self):
        """Test getting list of all emotions"""
        emotions = get_all_emotions()
        
        self.assertIsInstance(emotions, list, "Should return a list")
        self.assertGreater(len(emotions), 0, "Should have at least one emotion")
        self.assertIn('happy', emotions, "Should include 'happy'")
        self.assertIn('sad', emotions, "Should include 'sad'")
        self.assertIn('angry', emotions, "Should include 'angry'")
        self.assertIn('neutral', emotions, "Should include 'neutral'")
    
    def test_all_emotions_have_recommendations(self):
        """Test that all emotions have recommendations"""
        emotions = get_all_emotions()
        
        for emotion in emotions:
            recommendations = get_recommendations(emotion)
            self.assertIn('mood', recommendations, 
                         f"Emotion '{emotion}' should have mood")
            self.assertIn('songs', recommendations, 
                         f"Emotion '{emotion}' should have songs")
            self.assertGreater(len(recommendations['songs']), 0, 
                             f"Emotion '{emotion}' should have at least one song")


class TestMusicMappingConsistency(unittest.TestCase):
    """Test consistency of music mapping data"""
    
    def test_all_songs_have_complete_info(self):
        """Test that all songs have complete information"""
        emotions = get_all_emotions()
        
        for emotion in emotions:
            recommendations = get_recommendations(emotion)
            songs = recommendations['songs']
            
            for song in songs:
                self.assertTrue(len(song['title']) > 0, 
                              f"Song in '{emotion}' should have non-empty title")
                self.assertTrue(len(song['artist']) > 0, 
                              f"Song in '{emotion}' should have non-empty artist")
                self.assertTrue(len(song['genre']) > 0, 
                              f"Song in '{emotion}' should have non-empty genre")
    
    def test_no_duplicate_songs_per_emotion(self):
        """Test that there are no duplicate songs within an emotion"""
        emotions = get_all_emotions()
        
        for emotion in emotions:
            recommendations = get_recommendations(emotion)
            songs = recommendations['songs']
            titles = [song['title'] for song in songs]
            
            self.assertEqual(len(titles), len(set(titles)), 
                           f"Emotion '{emotion}' should not have duplicate songs")
    
    def test_mood_descriptions_exist(self):
        """Test that all emotions have mood descriptions"""
        emotions = get_all_emotions()
        
        for emotion in emotions:
            recommendations = get_recommendations(emotion)
            mood = recommendations['mood']
            
            self.assertIsInstance(mood, str, 
                                f"Mood for '{emotion}' should be a string")
            self.assertGreater(len(mood), 0, 
                             f"Mood for '{emotion}' should not be empty")


if __name__ == '__main__':
    unittest.main()
