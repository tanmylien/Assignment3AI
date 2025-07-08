from source_code.base_assistant import AIAssistant
from source_code.models import Request, Response
import random

class PsychologyAssistant(AIAssistant):
    def greetUser(self) -> str:
        return f"🧠 Hello {self.user.name}, I’m here to listen and help however I can."

    def handleRequest(self, request: Request) -> Response:
        while True:
            print("💭 What’s been on your mind lately? What’s been weighing your heart?")
            for attempt in range(3):
                user_input = input("Your answer: ").strip().lower()

                if not user_input or len(user_input.split()) < 3:
                    print("🧐 Hmm… I didn’t quite catch that. Could you share a bit more?")
                    continue

                print("\n" + random.choice([
                    "💬 Thank you for opening up. Let’s work through this together.",
                    "🤝 I’m really glad you shared that. It’s okay to feel this way.",
                    "🌱 You’re not alone — your feelings are valid, and I’m here for you."
                ]))

                print("\nWould you like me to just listen more, or offer some advice to help you cope?")
                follow_up = input("Type 'listen' or 'advice': ").strip().lower()

                if "advice" in follow_up:
                    print("🤖 " + self.offer_coping_advice().message)
                elif "listen" in follow_up:
                    print("🧏 I’m here, feel free to share more if you’d like.")
                else:
                    print("❓ I’m not sure what you meant — I’ll just be here if you want to talk.")

                break  # exit retry loop after a successful entry

            # Ask if they want to continue talking
            print("\n🫂 Would you like to share anything else or keep talking?")
            more = input("Your answer (yes/no): ").strip().lower()

            if more in ["no", "n"]:
                goodbye_msg = random.choice([
                    "🌼 Be kind to yourself. You’re doing better than you think.",
                    "🫶 You’re not alone — I’ll always be here when you need someone to talk to.",
                    "☀️ Take it one moment at a time. I believe in you."
                    "🌈 Take gentle care of yourself — I’ll be here whenever you need someone to talk to.",
                    "💛 You did great opening up today. I'm proud of you. Come back anytime, okay?",
                    "🌻 You’re not alone. Even small steps forward matter. I’m always here when you need me.",
                    "🫶 Wishing you peace and comfort today. Come back anytime — I’ll be here for you.",
                    "🌟 You’ve got this. Remember to rest, breathe, and be kind to yourself. Talk soon!"
                ])
                return self.generateResponse(goodbye_msg)
            elif more in ["yes", "y"]:
                print("🧠 Of course, I'm listening.")
                continue
            else:
                return self.generateResponse("💛 Whether you’d like to keep talking or just take a break — I’m always here when you need me.")

    def offer_coping_advice(self) -> Response:
        tips = [
            "Try the 4-7-8 breathing technique to calm your nervous system.",
            "A short walk in nature can help reset your mood.",
            "Journaling can be a safe space to express your feelings.",
            "Progressive muscle relaxation relieves tension in the body.",
            "Talking to someone you trust often helps lighten emotional load."
            "Try the 4-7-8 breathing technique to calm your nervous system.",
            "A 10-minute walk in nature can improve your mood.",
            "Journaling your thoughts can help you gain clarity and perspective.",
            "Reach out to someone you trust — talking helps lighten the load.",
            "Progressive muscle relaxation is a great way to relieve physical tension.",
            "Try naming your emotions out loud. It can reduce their intensity and help you process them.",
            "Practice grounding by noticing 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
            "Drink a glass of water slowly while breathing deeply to help reconnect with your body.",
            "Write down three small things you’re grateful for today. Even tiny positives can shift your mindset.",
            "Set a 5-minute timer and allow yourself to cry, vent, or write freely — no filter.",
            "Wrap yourself in a blanket like a burrito and take 10 slow breaths. Physical comfort can ease emotional stress.",
            "Put on a playlist that matches your mood — sometimes feeling understood by music helps you process it.",
            "Watch or read something that comforted you as a child. Revisiting safe memories can bring relief.",
            "Repeat to yourself: ‘This feeling is temporary. I can get through this.’",
            "If you can’t fix the problem now, be kind to your body — stretch, drink water, or rest. That’s healing too."
        ]
        return self.generateResponse(f"🧘 Here’s a gentle suggestion that might help:\n{random.choice(tips)}")