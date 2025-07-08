from source_code.base_assistant import AIAssistant
from source_code.models import Request, Response

class MusicAssistant(AIAssistant):
    def greetUser(self) -> str:
        return f"🎵 Hey {self.user.name}, ready for some music vibes?"
    
    def handleRequest(self, request: Request) -> Response:
        mood_map = {
            "tense": "Soothing Instrumentals",
            "gloomy": "Rainy Day Vibes",
            "fun": "Party Starters",
            "energetic": "High BPM Hits",
            "gentle": "Soft Acoustic",
            "romantic": "Love Songs",
            "calm": "Lofi Chill",
            "relax": "Ambient Escape",
            "depressed": "Emotional Ballads",
            "chill": "Evening Chillout",
            "happy": "Feel Good Hits",
            "sad": "Sad Vibes",
            "worry": "Rainy Day Lo-fi",
            "anxious": "Soothing Instrumentals",
            "stressed": "Ambient Chill",
            "overwhelmed": "Piano for Focus",
            "excited": "Dance Party Mix",
            "confident": "Empowerment Anthems",
            "motivated": "Hype & Grind",
            "inspired": "Creative Flow",
            "grateful": "Morning Gratitude Vibes",
            "focused": "Deep Focus Beats",
            "productive": "Work Vibes",
            "studying": "No Distraction Lo-fi",
            "background": "Ambient Study Mix",
            "lonely": "Companion Songs",
            "broken": "Healing Melodies",
            "insecure": "Gentle Affirmations",
            "burnout": "Mental Reset",
            "defeated": "Rebuild Energy",
            "nostalgic": "Throwback Classics",
            "dreamy": "Ethereal Chill",
            "romanticized": "Movie Soundtrack Moments",
            "artistic": "Paint & Chill",
            "in love": "You are mine and I am yours",
            "kpop": "Top 100 New Kpop Hits",
        }

        artist_map = {
            "taylor swift": "Taylor Swift Essentials",
            "bts": "BTS Army Playlist",
            "drake": "Drake Hits",
            "coldplay": "Coldplay Chill Mix",
            "blackpink": "BLACKPINK Essentials",
            "ed sheeran": "Ed Sheeran Acoustic Vibes"
        }

        activity_map = {
            "study": "Lo-fi Study Mix",
            "run": "Power Run Beats",
            "clean": "Motivation Mix",
            "sleep": "Nighttime Ambience",
            "drive": "Roadtrip Vibes",
            "cook": "Kitchen Grooves",
            "work out": "Fitness Music Motivation",
            "shower": "Singing in the Shower",
        }

        input_lower = request.input_str.lower()

        # Mood-based recommendation
        for mood, playlist in mood_map.items():
            if mood in input_lower:
                return self.recommend_playlist(playlist)

        # Artist-based recommendation
        for artist, playlist in artist_map.items():
            if artist in input_lower or f"like {artist}" in input_lower:
                return self.recommend_by_artist(artist, playlist)

        # Activity-based recommendation
        for activity, playlist in activity_map.items():
            if activity in input_lower:
                return self.recommend_by_activity(activity, playlist)

        # If 
        if "playlist" in input_lower or "play list" in input_lower or "music" in input_lower:
            follow_up = input("🎧 What kind of vibe, artist, or activity are you in the mood for? ").strip().lower()

            # Check again for mood
            for mood, playlist in mood_map.items():
                if mood in follow_up:
                    return self.recommend_playlist(playlist)
            for artist, playlist in artist_map.items():
                if artist in follow_up:
                    return self.recommend_by_artist(artist, playlist)
            for activity, playlist in activity_map.items():
                if activity in follow_up:
                    return self.recommend_by_activity(activity, playlist)

            return self.generateResponse("🎵 I couldn't match your vibe just yet, but I'm working on expanding my music brain!")

        return super().handleRequest(request)

    def recommend_playlist(self, mood_name: str) -> Response:
        return self.generateResponse(f"Based on your mood, here's a '{mood_name}' playlist 🎶")
    
    # Recommend songs or playlists by your favorite artist
    def recommend_by_artist(self, artist: str, playlist: str) -> Response:
        return self.generateResponse(f"If you like {artist.title()}, try this playlist: '{playlist}' 🎤")
    
    # Recommend songs or playlists by your activities
    def recommend_by_activity(self, activity: str, playlist: str) -> Response:
        return self.generateResponse(f"For {activity}, I recommend: '{playlist}' 🎧")