# Emotion to Music Mapping Database
emotion_music_mapping = {
    "happy": {
        "mood": "Happy and Uplifting",
        "songs": [
            {"title": "Walking on Sunshine", "artist": "Katrina & The Waves", "genre": "Pop"},
            {"title": "Good as Hell", "artist": "Lizzo", "genre": "Pop"},
            {"title": "Don't Stop Me Now", "artist": "Queen", "genre": "Rock"},
            {"title": "Shut Up and Dance", "artist": "Walk the Moon", "genre": "Indie Pop"},
            {"title": "Levitating", "artist": "Dua Lipa", "genre": "Disco-Pop"},
        ]
    },
    "sad": {
        "mood": "Melancholic and Reflective",
        "songs": [
            {"title": "Someone Like You", "artist": "Adele", "genre": "Acoustic"},
            {"title": "The Night We Met", "artist": "Lord Huron", "genre": "Indie Folk"},
            {"title": "Hurt", "artist": "Johnny Cash", "genre": "Acoustic"},
            {"title": "Yesterday", "artist": "The Beatles", "genre": "Pop"},
            {"title": "Black", "artist": "Pearl Jam", "genre": "Grunge"},
        ]
    },
    "angry": {
        "mood": "Energetic and Intense",
        "songs": [
            {"title": "Killing in the Name", "artist": "Rage Against the Machine", "genre": "Rock"},
            {"title": "Seven Nation Army", "artist": "The White Stripes", "genre": "Rock"},
            {"title": "Break Stuff", "artist": "Limp Bizkit", "genre": "Nu-Metal"},
            {"title": "Bodies", "artist": "Drowning Pool", "genre": "Metal"},
            {"title": "Bleed It Out", "artist": "Linkin Park", "genre": "Rock"},
        ]
    },
    "neutral": {
        "mood": "Calm and Relaxing",
        "songs": [
            {"title": "Lo-Fi Hip Hop", "artist": "Chillhop Music", "genre": "Lo-Fi"},
            {"title": "Weightless", "artist": "Marconi Union", "genre": "Ambient"},
            {"title": "Re: Stacks", "artist": "Bon Iver", "genre": "Indie Folk"},
            {"title": "Clair de Lune", "artist": "Claude Debussy", "genre": "Classical"},
            {"title": "Coffee", "artist": "Beabadoobee", "genre": "Indie"},
        ]
    },
    "surprise": {
        "mood": "Upbeat and Energetic",
        "songs": [
            {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "genre": "Funk"},
            {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Synthwave"},
            {"title": "Jumpsuit", "artist": "Twenty One Pilots", "genre": "Alternative"},
            {"title": "Mr. Brightside", "artist": "The Killers", "genre": "Indie Rock"},
            {"title": "Such Great Heights", "artist": "Iron & Wine", "genre": "Indie Folk"},
        ]
    },
    "fear": {
        "mood": "Dark and Mysterious",
        "songs": [
            {"title": "Thriller", "artist": "Michael Jackson", "genre": "Pop"},
            {"title": "In the End", "artist": "Linkin Park", "genre": "Rock"},
            {"title": "My Immortal", "artist": "Evanescence", "genre": "Alternative Rock"},
            {"title": "Papaoutai", "artist": "Stromae", "genre": "Electronic"},
            {"title": "Radioactive", "artist": "Imagine Dragons", "genre": "Alternative Rock"},
        ]
    },
    "disgust": {
        "mood": "Cleansing and Empowering",
        "songs": [
            {"title": "Stronger", "artist": "Kanye West", "genre": "Hip-Hop"},
            {"title": "Fighter", "artist": "Christina Aguilera", "genre": "Pop"},
            {"title": "Beautiful", "artist": "Christina Aguilera", "genre": "Pop"},
            {"title": "Roar", "artist": "Katy Perry", "genre": "Pop"},
            {"title": "Born This Way", "artist": "Lady Gaga", "genre": "Pop"},
        ]
    }
}

def get_recommendations(emotion):
    """
    Get song recommendations based on detected emotion.
    
    Args:
        emotion (str): Detected emotion (lowercase)
    
    Returns:
        dict: Emotion mood and list of recommended songs
    """
    emotion = emotion.lower()
    if emotion in emotion_music_mapping:
        return emotion_music_mapping[emotion]
    else:
        # Default to neutral if emotion not found
        return emotion_music_mapping["neutral"]

def get_all_emotions():
    """Get list of all supported emotions."""
    return list(emotion_music_mapping.keys())
