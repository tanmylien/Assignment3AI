from source_code.base_assistant import AIAssistant
from source_code.models import Request, Response

class FitnessAssistant(AIAssistant):
    def greetUser(self) -> str:
        return f"💪 Hey {self.user.name}, let’s build some muscle and confidence together!"

    def handleRequest(self, request: Request) -> Response:
        input_text = request.input_str.lower()

        # Step 1: Ask what muscle group to target
        muscle_groups = {
            "chest": "Chest Sculpting Routine",
            "triceps": "Triceps Toner Program",
            "shoulder": "Shoulder Definition Circuit",
            "legs": "Leg Power Workout",
            "glutes": "Glute Builder Plan",
            "forearms": "Forearm Strength Set",
            "abs": "Core Crusher Circuit",
            "back": "Back Strength Workout",
            "biceps": "Bicep Blast Session"
        }

        while "muscle" not in self.user.preferences:
            print("💭 What muscle group would you like to build? (e.g., chest, legs, glutes, abs, forearms, biceps,...)")
            selected = input("Your answer: ").lower()

            for muscle, plan in muscle_groups.items():
                if muscle in selected:
                    self.user.preferences["muscle"] = muscle
                    self.user.preferences["plan"] = plan
                    print(f"✅ Got it! Here's your recommended workout: '{plan}' 💪")
                    break
            else:
                print("❌ Sorry, I didn’t recognize that muscle group. Please try again.\n")

        # Step 2: Ask if they want a schedule
        print("🗓️ Would you like a personal workout schedule to match your goals? (yes/no)")
        wants_schedule = input("Your answer: ").strip().lower()

        if wants_schedule not in ["yes", "y"]:
            return self.generateResponse("No worries! Happy exercising! 💪 Let me know if you need anything else.")

        # Step 3: Ask long-term goal
        print("🎯 What is your long-term fitness goal? (e.g., lose weight, tone body, build muscle)")
        goal = input("Your answer: ").strip().lower()
        self.user.preferences["goal"] = goal

        # Step 4: Ask days/week (loop until valid)
        while True:
            print("📆 How many days per week can you work out? (1–7)")
            try:
                days = int(input("Your answer: ").strip())
                if 1 <= days <= 7:
                    break
                else:
                    print("❌ Please enter a number between 1 and 7.\n")
            except ValueError:
                print("❌ That wasn't a valid number. Try again with a number between 1 and 7.\n")

        # Step 5: Generate hardcoded schedule
        schedule = self.generateSchedule(goal, days)
        return self.generateResponse(f"✅ Based on your goal '{goal}' and availability of {days} days/week, here's your custom schedule:\n\n{schedule}")

    def generateSchedule(self, goal: str, days: int) -> str:
        plans = {
            "lose weight": {
                1: "1x/week: Full-body HIIT + 30-min walk",
                3: "Mon/Wed/Fri: Cardio + Bodyweight Circuits",
                5: "Mon–Fri: Cardio + Strength Intervals",
                7: "Daily: HIIT (3x) + LISS Cardio (4x)"
            },
            "tone body": {
                1: "1x/week: Pilates + light resistance",
                3: "Mon/Wed/Fri: Resistance Band Training",
                5: "Mon–Fri: Alternating upper/lower splits",
                7: "Daily: Short full-body tone + stretching"
            },
            "build muscle": {
                1: "1x/week: Full-body Strength Circuit",
                3: "Mon/Wed/Fri: Push, Pull, Legs split",
                5: "5-day Muscle Split (Chest, Back, Legs, Shoulders, Arms)",
                7: "Bodybuilding-style training w/ active recovery"
            }
        }

        match = plans.get(goal, plans["build muscle"])
        # Return closest plan available
        if days >= 7:
            return match.get(7)
        elif days >= 5:
            return match.get(5)
        elif days >= 3:
            return match.get(3)
        else:
            return match.get(1)

