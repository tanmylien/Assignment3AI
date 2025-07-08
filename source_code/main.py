from source_code.models import UserProfile, Request, CommandType
from source_code.music_assistant import MusicAssistant
from source_code.fitness_assistant import FitnessAssistant
from source_code.study_assistant import StudyAssistant
from source_code.base_assistant import AIAssistant
from source_code.book_assistant import BookAssistant
from source_code.psychology_assistant import PsychologyAssistant
from datetime import datetime

def classify_command(input_str: str) -> CommandType:
    input_str = input_str.lower()

    if "feel" in input_str or "feeling" in input_str or "listen" in input_str:
        print("\n🧠 I hear you. I know some feelings can be heavy.")
        print("Would you like me to:")
        print("🎵 1) Recommend a song or playlist to soothe your mood")
        print("💬 2) Just listen to what you want to share — I’m here for you.")
        
        for _ in range(2):
            follow_up = input("You can say something like 'playlist' or 'talk to you': ").strip().lower()
            if any(word in follow_up for word in ["song", "playlist", "listen to music", "music", "tune", "songs", "playlists"]):
                return CommandType.MUSIC
            elif any(word in follow_up for word in ["talk", "vent", "listen to me", "share", "express", "tell you", "someone to talk"]):
                return CommandType.PSYCHOLOGY
            else:
                print("Hmm... I didn’t quite understand. Can you try rephrasing?")
        print("❓Still a bit unclear... Let me know if there's anything else I can help with.")
        return CommandType.GENERAL

    if any(word in input_str for word in ["song", "music", "romantic", "listen", "play", "playlist", "mood", "tune", "songs"]):
        return CommandType.MUSIC
    elif any(word in input_str for word in ["workout", "exercise", "gym", "gain muscle", "build muscle", "work out"]):
        return CommandType.FITNESS
    elif any(word in input_str for word in ["study", "review", "math", "homework"]):
        return CommandType.STUDY
    elif any(word in input_str for word in ["book", "novel", "read", "recommend a book", "story", "fantasy", "romance", "thriller"]):
        return CommandType.BOOK
    elif any(word in input_str for word in ["sad", "anxious", "depressed", "cope", "mental", "psychology", "stressed", "burnout", "therapy", "vent"]):
        return CommandType.PSYCHOLOGY
    else:
        return CommandType.GENERAL

def main():
    print("👋 Hey there! I’m your personal AI Assistant.")
    print("I can help you with music, fitness, studying, and more.\n")

    # Ask for user name
    name = input("🧑 What’s your name (or what should I call you)? ").strip()

    # Ask for age
    while True:
        age_input = input(f"🎂 Nice to meet you, {name}! How old are you? ")
        try:
            age = int(age_input)
            break
        except ValueError:
            print("❌ Oops, that doesn’t look like a number. Please enter a valid age.")

    # Ask if the user is premium
    while True:
        premium_input = input("💎 Are you a premium user? (yes/no): ").strip().lower()
        if premium_input in ["yes", "y"]:
            is_premium = True
            break
        elif premium_input in ["no", "n"]:
            is_premium = False
            break
        else:
            print("❌ Please answer with 'yes' or 'no'.")

    # Create UserProfile
    user = UserProfile(name=name, age=age, preferences={}, isPremium=is_premium)

    # Request limit for free users
    # Premium users can ask unlimitedly
    free_limit = 3
    request_count = 0

    # Start assistant loop
    while True:
        if not user.isPremium and request_count >= free_limit:
            print("🚫 Sorry, you have reached your plan limit. 💎 Please upgrade to premium or come back later after reset.")
            break

        # Ask for request
        mood_or_goal = input("\n💬 What can I help you with now?\n"
                             "You can say things like:\n"
                             "— 'Play me something romantic'\n"
                             "— 'I want to build muscle'\n"
                             "— 'Help me study for math'\n"
                             "— 'Recommend me a book to read'\n"
                             "— 'I need someone to listen to me now'\n"
                             "\n👉 Your request: ").strip()

        command_type = classify_command(mood_or_goal)
        user.preferences["raw_input"] = mood_or_goal
        request = Request(input_str=mood_or_goal, timestamp=datetime.now(), command_type=command_type)

        # Select correct assistant
        if command_type == CommandType.MUSIC:
            assistant = MusicAssistant(user)
        elif command_type == CommandType.FITNESS:
            assistant = FitnessAssistant(user)
        elif command_type == CommandType.STUDY:
            assistant = StudyAssistant(user)
        elif command_type == CommandType.BOOK:
            assistant = BookAssistant(user)
        elif command_type == CommandType.PSYCHOLOGY:
            assistant = PsychologyAssistant(user)
        else:
            assistant = AIAssistant(user)

        # Output assistant response
        print("\n💡 " + assistant.greetUser())
        response = assistant.handleRequest(request)
        print("🤖 " + response.message)

        # Ask to continue
        cont = input("\n🔁 Is there anything else I can help you with? (yes/no): ").strip().lower()
        if cont not in ["yes", "y"]:
            print("👋 Alright, take care! Come back anytime. 😊")
            break
        else:
            print(f"\n✅ I'm still here with you, {name}. What would you like to do next?")
            if not user.isPremium:
                request_count += 1

if __name__ == "__main__":
    main()