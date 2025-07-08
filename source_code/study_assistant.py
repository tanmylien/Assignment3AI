from source_code.base_assistant import AIAssistant
from source_code.models import Request, Response

class StudyAssistant(AIAssistant):
    def greetUser(self) -> str:
        return f"📚 Hello {self.user.name}, let’s power through your study goals!"

    def handleRequest(self, request: Request) -> Response:
        # Step 1: Ask which subject
        subject = input("🧠 Tell me which subject you’d like to review:\n📘 Your answer: ").strip()
        if not subject:
            return self.generateResponse("⚠️ I didn’t catch that. Please tell me which subject you'd like to review.")
        self.user.preferences["subject"] = subject

        print(f"\n✅ Great! Let’s review some key points in {subject} together!")

        # Step 2: Ask what kind of help
        while True:
            choice = input("\n💡 Would you like to (a) schedule a study session or (b) get help with a topic you’re struggling with?\n👉 Your answer: ").lower()

            if "schedule" in choice or "session" in choice or choice == "a":
                return self.schedule_study_session(subject)
            elif "explain" in choice or "topic" in choice or choice == "b":
                topic = input(f"\n🤔 What topic in {subject} are you having trouble with?\n📝 Topic: ").strip()
                print("\n📖 Okay! Let me break it down for you...\n")
                explanation = self.explain_topic(topic)
                print(explanation.message)

                # Step 3: Follow-up check
                follow_up = input("\n🧠 Do you feel more confident now? (yes/no): ").strip().lower()
                if follow_up == "no":
                    analogy_response = self.explain_with_analogy(topic)
                    return analogy_response
                else:
                    return self.generateResponse("🙌 Awesome! Let me know if you'd like to review anything else.")
            else:
                print("❌ Sorry, I couldn’t understand what you want. Please choose either (a) schedule or (b) explain a topic.")

    def schedule_study_session(self, subject: str) -> Response:
        return self.generateResponse(
            f"📅 Study session scheduled for {subject} using spaced repetition: 1st in 1 day, 2nd in 3 days, and 3rd in a week. Let’s make it stick! 🧠")

    def explain_topic(self, topic: str) -> Response:
        return self.generateResponse(
            f"Here’s a simplified explanation of **{topic}** with examples to help clarify the core idea.\n [Later we will use OpenAI to provide a detailed answer to the user]")

    def explain_with_analogy(self, topic: str) -> Response:
        analogies = {
            "oop": "Think of Object-Oriented Programming like organizing a kitchen: classes are recipes, objects are dishes made from recipes.",
            "recursion": "Recursion is like Russian nesting dolls—each function call contains a smaller version of the same problem.",
            "pointers": "A pointer is like a bookmark in a book—it doesn’t hold information itself, but tells you where to find it."
        }
        explanation = analogies.get(topic.lower(), f"Let me rephrase {topic} using a real-life analogy to help it click.")
        return self.generateResponse(f"🔁 No worries! Here's another way to think about it:\n{explanation}")