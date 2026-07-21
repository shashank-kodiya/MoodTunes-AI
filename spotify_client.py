"""
spotify_client.py — Spotify API integration for MoodTunes
Fetches real tracks from Spotify based on detected emotion.
"""
import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Emotion → curated search queries (seeds for Spotify search)
EMOTION_QUERIES = {
    "happy": [
        "happy upbeat pop",
        "feel good hits",
        "sunshine pop dance",
        "uplifting summer playlist",
        "positive energy music",
    ],
    "sad": [
        "sad melancholic acoustic",
        "heartbreak ballads",
        "emotional indie folk",
        "rainy day sad songs",
        "melancholy piano",
    ],
    "angry": [
        "intense hard rock anger",
        "metal rage workout",
        "aggressive rap hip hop",
        "heavy metal energy",
        "intense rock guitar",
    ],
    "neutral": [
        "lo-fi chill study",
        "ambient relaxing focus",
        "calm indie acoustic",
        "peaceful background music",
        "mellow evening playlist",
    ],
    "surprise": [
        "upbeat unexpected pop",
        "energetic surprise indie",
        "exciting synthwave upbeat",
        "fun party dance hits",
        "vibrant electronic beats",
    ],
    "fear": [
        "dark mysterious atmospheric",
        "eerie gothic soundtrack",
        "haunting orchestral dark",
        "suspenseful cinematic music",
        "dark electronic ambient",
    ],
    "disgust": [
        "empowering anthem pop",
        "strong powerful hip hop",
        "confidence boost playlist",
        "empowerment music female",
        "uplifting self worth songs",
    ],
}


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        """Initialize the Spotify API client.

        Args:
            client_id: Your Spotify app Client ID
            client_secret: Your Spotify app Client Secret
        """
        self.client_id = client_id.strip()
        self.client_secret = client_secret.strip()
        self._sp = None
        self._authenticated = False
        self._auth_error = None

    def authenticate(self) -> bool:
        """Attempt authentication. Returns True on success."""
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
            self._sp = spotipy.Spotify(auth_manager=auth_manager)
            # Quick sanity check — fetch one track
            self._sp.search(q="test", type="track", limit=1)
            self._authenticated = True
            self._auth_error = None
            return True
        except Exception as e:
            self._authenticated = False
            self._auth_error = str(e)
            self._sp = None
            return False

    @property
    def is_authenticated(self) -> bool:
        return self._authenticated

    @property
    def auth_error(self) -> str | None:
        return self._auth_error

    def get_tracks_for_emotion(self, emotion: str, limit: int = 6) -> list[dict]:
        """Fetch real Spotify tracks matching the given emotion.

        Args:
            emotion: Detected emotion string (lowercase)
            limit: Number of tracks to return

        Returns:
            List of track dicts with title, artist, album, image_url,
            spotify_url, preview_url, duration_ms, and popularity fields.
        """
        if not self._authenticated or self._sp is None:
            return []

        queries = EMOTION_QUERIES.get(emotion.lower(), EMOTION_QUERIES["neutral"])
        # Pick a random query to add variety on every detection
        query = random.choice(queries)

        try:
            # We ask for more than needed so we can shuffle / sample
            results = self._sp.search(q=query, type="track", limit=min(50, limit * 5))
            items = results.get("tracks", {}).get("items", [])

            tracks = []
            seen = set()
            random.shuffle(items)

            for item in items:
                if len(tracks) >= limit:
                    break
                if not item:
                    continue

                track_id = item.get("id")
                if track_id in seen:
                    continue
                seen.add(track_id)

                artists = ", ".join(a["name"] for a in item.get("artists", []))
                album = item.get("album", {})
                images = album.get("images", [])
                image_url = images[0]["url"] if images else ""
                spotify_url = item.get("external_urls", {}).get("spotify", "")
                preview_url = item.get("preview_url", "")  # 30-sec MP3 (may be None)
                popularity = item.get("popularity", 0)
                duration_ms = item.get("duration_ms", 0)
                mins, secs = divmod(duration_ms // 1000, 60)

                tracks.append({
                    "title": item.get("name", "Unknown"),
                    "artist": artists,
                    "album": album.get("name", ""),
                    "image_url": image_url,
                    "spotify_url": spotify_url,
                    "preview_url": preview_url,
                    "duration": f"{mins}:{secs:02d}",
                    "popularity": popularity,
                    "track_id": track_id,
                })

            return tracks

        except Exception as e:
            print(f"[SpotifyClient] Search error: {e}")
            return []

    def get_track_embed_url(self, track_id: str) -> str:
        """Return the Spotify embed URL for the iframe player."""
        return f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0"
