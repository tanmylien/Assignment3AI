from source_code.base_assistant import AIAssistant
from source_code.models import Request, Response

class BookAssistant(AIAssistant):
    def greetUser(self) -> str:
        return f"📚 Hi {self.user.name}, let’s find your next great read!"

    def handleRequest(self, request: Request) -> Response:
        input_lower = request.input_str.lower()

        # Genre-based recommendations
        genre_map = {
            "romance": ("The Love Hypothesis by Ali Hazelwood", "https://www.goodreads.com/book/show/56732449-the-love-hypothesis"),
            "fantasy": ("A Court of Thorns and Roses by Sarah J. Maas", "https://www.goodreads.com/book/show/16096824-a-court-of-thorns-and-roses"),
            "mystery": ("The Girl with the Dragon Tattoo by Stieg Larsson", "https://www.goodreads.com/book/show/2429135.The_Girl_with_the_Dragon_Tattoo"),
            "sci-fi": ("Project Hail Mary by Andy Weir", "https://www.goodreads.com/book/show/54493401-project-hail-mary"),
            "thriller": ("The Silent Patient by Alex Michaelides", "https://www.goodreads.com/book/show/40097951-the-silent-patient"),
            "historical": ("The Nightingale by Kristin Hannah", "https://www.goodreads.com/book/show/21853621-the-nightingale"),
            "self-help": ("Atomic Habits by James Clear", "https://www.goodreads.com/book/show/40121378-atomic-habits"),
            "young adult": ("They Both Die at the End by Adam Silvera", "https://www.goodreads.com/book/show/33385229-they-both-die-at-the-end"),
        }

        # Keyword matching
        for genre, (title, link) in genre_map.items():
            if genre in input_lower:
                return self.recommend_book(title, link, genre)

        # Prompt user if no genre match
        if "book" in input_lower or "recommend" in input_lower:
            follow_up = input("📖 What kind of story or genre are you in the mood for? (e.g., fantasy, romance, thriller): ").strip().lower()
            for genre, (title, link) in genre_map.items():
                if genre in follow_up:
                    return self.recommend_book(title, link, genre)
            return self.generateResponse("🔍 I couldn’t quite find a match yet, but I’m expanding my bookshelf!")

        return super().handleRequest(request)

    def recommend_book(self, title: str, link: str, genre: str) -> Response:
        message = f"📚 Based on your interest in {genre.title()}, I recommend: '{title}'\n🔗 You can check it out here: {link}"
        return self.generateResponse(message)