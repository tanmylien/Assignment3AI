import tkinter as tk
from tkinter import scrolledtext, messagebox
from models import UserProfile, Request, CommandType
from music_assistant import MusicAssistant
from fitness_assistant import FitnessAssistant
from study_assistant import StudyAssistant
from base_assistant import AIAssistant
from book_assistant import BookAssistant
from psychology_assistant import PsychologyAssistant
from datetime import datetime
import threading
import requests
import json
import os

def classify_command(input_str: str, chat_gui=None) -> CommandType:
    input_str = input_str.lower()

    if "feel" in input_str or "feeling" in input_str or "listen" in input_str:
        if chat_gui:
            # GUI mode - show options and wait for user response
            chat_gui.add_message("AI Assistant", "🧠 I hear you. I know some feelings can be heavy.", "assistant")
            chat_gui.add_message("AI Assistant", "Would you like me to:", "assistant")
            chat_gui.add_message("AI Assistant", "🎵 1) Recommend a song or playlist to soothe your mood", "assistant")
            chat_gui.add_message("AI Assistant", "💬 2) Just listen to what you want to share — I'm here for you.", "assistant")
            chat_gui.add_message("AI Assistant", "You can say something like 'playlist' or 'talk to you':", "assistant")
            chat_gui.waiting_for_followup = True
            chat_gui.followup_attempts = 0
            return None  # Will be determined by follow-up
        else:
            # Console mode - original main.py logic
            print("\n🧠 I hear you. I know some feelings can be heavy.")
            print("Would you like me to:")
            print("🎵 1) Recommend a song or playlist to soothe your mood")
            print("💬 2) Just listen to what you want to share — I'm here for you.")

            for _ in range(2):
                follow_up = input("You can say something like 'playlist' or 'talk to you': ").strip().lower()
                if any(word in follow_up for word in ["song", "playlist", "listen to music", "music", "tune", "songs", "playlists"]):
                    return CommandType.MUSIC
                elif any(word in follow_up for word in ["talk", "vent", "listen to me", "share", "express", "tell you", "someone to talk"]):
                    return CommandType.PSYCHOLOGY
                else:
                    print("Hmm... I didn't quite understand. Can you try rephrasing?")
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

def call_gemini_api(question, api_key=None):
    """Call Gemini API for general questions"""
    try:
        # Try to get API key from environment variable or use default
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY', 'your-Gemini-API') # Please use your Gemini API's key here

        if api_key == 'YOUR_GEMINI_API_KEY':
            return "Please set your GEMINI_API_KEY environment variable to use AI responses for general questions."

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": question
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text'].strip()
            return "Sorry, I couldn't generate a response."
        else:
            error_data = response.json()
            if 'error' in error_data:
                return f"API Error: {error_data['error']['message']}"
            return "Sorry, there was an error connecting to the AI service."

    except requests.exceptions.Timeout:
        return "Sorry, the request timed out. Please try again."
    except requests.exceptions.RequestException:
        return "Sorry, there was a network error. Please check your connection."
    except Exception:
        return "Sorry, there was an unexpected error. Please try again."

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("1000x750")
        self.root.configure(bg="#2c3e50")

        # User data 
        self.user = None
        self.request_count = 0
        self.free_limit = 3

        # GUI-specific state for handling interactive prompts
        self.waiting_for_input = False
        self.waiting_for_followup = False
        self.waiting_for_continue = False
        self.followup_attempts = 0
        self.input_prompt = ""
        self.current_assistant = None
        self.pending_request = None
        self.conversation_active = True

        # State for handling assistant input requests
        self.pending_input_prompt = None
        self.waiting_for_assistant_input = False

        self.setup_ui()
        self.show_welcome_dialog()

    def setup_ui(self):
        # Main container 
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#34495e", height=80, bd=0, highlightthickness=0)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        header_frame.configure(highlightbackground="#2980b9", highlightcolor="#2980b9", highlightthickness=2)

        title_label = tk.Label(header_frame, text="AI Assistant",
                              font=("Segoe UI", 28, "bold"),
                              fg="#ecf0f1", bg="#34495e")
        title_label.pack(pady=20)

        # Chat area
        chat_container = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        chat_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 8))
        chat_container.configure(highlightbackground="#bdc3c7", highlightcolor="#bdc3c7", highlightthickness=1)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Segoe UI", 12),
            bg="#f8fafd",
            fg="#2c3e50",
            relief=tk.FLAT,
            padx=12,
            pady=10,
            state=tk.DISABLED,
            bd=0,
            highlightthickness=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input area
        input_frame = tk.Frame(main_frame, bg="#223355", height=56)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X)
        input_frame.pack_propagate(False)

        input_container = tk.Frame(input_frame, bg="#34495e")
        input_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self.input_entry = tk.Entry(
            input_container,
            font=("Segoe UI", 13),
            bg="#f8fafd",
            fg="#2c3e50",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=2,
            highlightcolor="#2980b9",
            insertbackground="#2980b9"
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8), ipady=4)
        self.input_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_container,
            text="Send",
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=4,
            activebackground="#2980b9",
            activeforeground="#ecf0f1",
            cursor="hand2",
            highlightthickness=0
        )
        self.send_button.pack(side=tk.RIGHT)
        self.send_button.bind("<Enter>", lambda _: self.send_button.config(bg="#2980b9"))
        self.send_button.bind("<Leave>", lambda _: self.send_button.config(bg="#3498db"))
        self.send_button.config(command=self.send_message)

        # Status bar
        status_frame = tk.Frame(main_frame, bg="#2c3e50", height=30)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)

        self.user_label = tk.Label(status_frame, text="User: Not logged in",
                                  font=("Segoe UI", 10), fg="#bdc3c7", bg="#2c3e50")
        self.user_label.pack(side=tk.LEFT, pady=5)

        self.requests_label = tk.Label(status_frame, text="",
                                      font=("Segoe UI", 10), fg="#bdc3c7", bg="#2c3e50")
        self.requests_label.pack(side=tk.RIGHT, pady=5)

        # Configure text tags for styling- different colors for user and AI
        self.chat_display.tag_configure("user", foreground="#e67e22", font=("Segoe UI", 12, "bold"), lmargin1=40, lmargin2=40, rmargin=10, spacing1=6, spacing3=6)  # Orange for user
        self.chat_display.tag_configure("assistant", foreground="#9b59b6", font=("Segoe UI", 12, "bold"), lmargin1=10, lmargin2=10, rmargin=40, spacing1=6, spacing3=6)  # Purple for AI
        self.chat_display.tag_configure("system", foreground="#e74c3c", font=("Segoe UI", 12), lmargin1=20, lmargin2=20, rmargin=20, spacing1=6, spacing3=6)  # Red for system
        self.chat_display.tag_configure("timestamp", foreground="#95a5a6", font=("Segoe UI", 9))
        self.chat_display.tag_configure("greeting", foreground="#f39c12", font=("Segoe UI", 12, "bold"), lmargin1=10, lmargin2=10, rmargin=40, spacing1=6, spacing3=6)  # Gold for greeting
        self.chat_display.tag_configure("response", foreground="#2ecc71", font=("Segoe UI", 12, "bold"), lmargin1=10, lmargin2=10, rmargin=40, spacing1=6, spacing3=6)  # Green for response

    def show_welcome_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Welcome to AI Assistant")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(bg="#34495e", bd=0, highlightthickness=0)
        dialog.configure(highlightbackground="#2980b9", highlightcolor="#2980b9", highlightthickness=2)

        # Center the dialog
        dialog.transient(self.root)
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Main container
        main_container = tk.Frame(dialog, bg="#34495e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=18, pady=12)

        # Welcome message 
        welcome_label = tk.Label(main_container, text="👋 Hey there! I'm your personal AI Assistant",
                                font=("Segoe UI", 15, "bold"), fg="#ecf0f1", bg="#34495e" , wraplength=440, justify="center")
        welcome_label.pack(pady=(12, 8))

        info_label = tk.Label(main_container, text="I can help you with music, fitness, studying, and more",
                             font=("Segoe UI", 10), fg="#bdc3c7", bg="#34495e", wraplength=420, justify="center")
        info_label.pack(pady=(0, 18))

        # Input section
        input_frame = tk.Frame(main_container, bg="#34495e")
        input_frame.pack(fill=tk.X, pady=(0, 18))

        # Name input 
        name_label = tk.Label(input_frame, text="🧑 What's your name (or what should I call you)?",
                             font=("Segoe UI", 10, "bold"), fg="#ecf0f1", bg="#34495e")
        name_label.pack(anchor=tk.W, pady=(0, 4))

        self.name_entry = tk.Entry(input_frame, font=("Segoe UI", 11), bg="#f8fafd", fg="#2c3e50",
                                  relief=tk.FLAT, bd=0, highlightthickness=2, highlightcolor="#2980b9")
        self.name_entry.pack(fill=tk.X, ipady=5, pady=(0, 12))

        # Age input 
        age_label = tk.Label(input_frame, text="🎂 How old are you?",
                            font=("Segoe UI", 10, "bold"), fg="#ecf0f1", bg="#34495e")
        age_label.pack(anchor=tk.W, pady=(0, 4))

        self.age_entry = tk.Entry(input_frame, font=("Segoe UI", 11), bg="#f8fafd", fg="#2c3e50",
                                 relief=tk.FLAT, bd=0, highlightthickness=2, highlightcolor="#2980b9")
        self.age_entry.pack(fill=tk.X, ipady=5, pady=(0, 12))

        # Premium checkbox 
        self.premium_var = tk.BooleanVar()
        premium_check = tk.Checkbutton(input_frame, text="💎 Are you a premium user?", variable=self.premium_var,
                                      font=("Segoe UI", 10), fg="#ecf0f1", bg="#34495e",
                                      selectcolor="#34495e", activebackground="#34495e",
                                      activeforeground="#ecf0f1", highlightthickness=0)
        premium_check.pack(anchor=tk.W, pady=(0, 10))

        # Buttons section
        button_frame = tk.Frame(main_container, bg="#34495e")
        button_frame.pack(fill=tk.X, pady=(10, 6))

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel",
                              font=("Segoe UI", 10, "bold"), bg="#e74c3c", fg="white",
                              relief=tk.FLAT, bd=0, padx=18, pady=7,
                              command=self.root.quit,
                              cursor="hand2", highlightthickness=0, activebackground="#c0392b")
        cancel_btn.pack(side=tk.LEFT, padx=(0, 8))
        cancel_btn.bind("<Enter>", lambda _: cancel_btn.config(bg="#c0392b"))
        cancel_btn.bind("<Leave>", lambda _: cancel_btn.config(bg="#e74c3c"))

        # Start Chat button
        start_btn = tk.Button(button_frame, text="Start Chat",
                              font=("Segoe UI", 10, "bold"), bg="#27ae60", fg="white",
                              relief=tk.FLAT, bd=0, padx=18, pady=7,
                              command=lambda: self.start_chat(dialog),
                              cursor="hand2", highlightthickness=0, activebackground="#219150")
        start_btn.pack(side=tk.RIGHT, padx=(8, 0))
        start_btn.bind("<Enter>", lambda _: start_btn.config(bg="#219150"))
        start_btn.bind("<Leave>", lambda _: start_btn.config(bg="#27ae60"))

        # Focus on name entry
        self.name_entry.focus()

        # Bind Enter key to start chat
        dialog.bind('<Return>', lambda _: self.start_chat(dialog))

    def start_chat(self, dialog):
        name = self.name_entry.get().strip()
        age_str = self.age_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        try:
            age = int(age_str)
            if age < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "❌ Oops, that doesn't look like a number. Please enter a valid age.")
            return

        is_premium = self.premium_var.get()

        # Create UserProfile 
        self.user = UserProfile(name=name, age=age, preferences={}, isPremium=is_premium)
        self.request_count = 0

        # Update UI
        self.user_label.config(text=f"User: {name} ({age} years old)")
        self.update_requests_label()

        # Add welcome message to chat
        self.add_message("AI Assistant", f"👋 Hey there! I'm your personal AI Assistant.", "assistant")
        self.add_message("AI Assistant", "I can help you with music, fitness, studying, and more.", "assistant")
        self.add_message("AI Assistant", "💬 What can I help you with now?", "assistant")
        self.add_message("AI Assistant", "You can say things like:", "assistant")
        self.add_message("AI Assistant", "— 'Play me something romantic'", "assistant")
        self.add_message("AI Assistant", "— 'I want to build muscle'", "assistant")
        self.add_message("AI Assistant", "— 'Help me study for math'", "assistant")
        self.add_message("AI Assistant", "— 'Recommend me a book to read'", "assistant")
        self.add_message("AI Assistant", "— 'I need someone to listen to me now'", "assistant")
        self.add_message("AI Assistant", "👉 Your request:", "assistant")

        dialog.destroy()
        self.input_entry.focus()

    def update_requests_label(self):
        if self.user:
            if self.user.isPremium:
                self.requests_label.config(text="Premium User - Unlimited requests")
            else:
                remaining = self.free_limit - self.request_count
                self.requests_label.config(text=f"Free User - {remaining} requests remaining")

    def add_message(self, sender, message, tag):
        self.chat_display.config(state=tk.NORMAL)

        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")

        # Add sender
        self.chat_display.insert(tk.END, f"{sender}: ", tag)

        # Add message (bubble effect: indent and spacing by tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, _=None):
        message = self.input_entry.get().strip()
        if not message:
            return

        if not self.user:
            messagebox.showerror("Error", "Please complete the welcome setup first.")
            return

        # Clear input
        self.input_entry.delete(0, tk.END)

        # Add user message to chat
        self.add_message("You", message, "user")

        # Handle assistant input requests
        if self.waiting_for_assistant_input:
            self.waiting_for_assistant_input = False
            self.pending_input_response = message
            return

        # Handle continue conversation logic
        if self.waiting_for_continue:
            self.waiting_for_continue = False
            if message.lower() in ["no", "n"]:
                self.add_message("AI Assistant", "👋 Alright, take care! Come back anytime. 😊", "assistant")
                return
            elif message.lower() in ["yes", "y"]:
                self.add_message("AI Assistant", f"✅ I'm still here with you, {self.user.name}. What would you like to do next?", "assistant")
                # Show the help menu again (same as main.py)
                self.add_message("AI Assistant", "💬 What can I help you with now?", "assistant")
                self.add_message("AI Assistant", "You can say things like:", "assistant")
                self.add_message("AI Assistant", "— 'Play me something romantic'", "assistant")
                self.add_message("AI Assistant", "— 'I want to build muscle'", "assistant")
                self.add_message("AI Assistant", "— 'Help me study for math'", "assistant")
                self.add_message("AI Assistant", "— 'Recommend me a book to read'", "assistant")
                self.add_message("AI Assistant", "— 'I need someone to listen to me now'", "assistant")
                self.add_message("AI Assistant", "👉 Your request:", "assistant")
                # Update request count for free users (same as main.py)
                if not self.user.isPremium:
                    self.request_count += 1
                    self.update_requests_label()
                return
            else:
                # Use Gemini API for other responses
                gemini_response = call_gemini_api(message)
                self.add_message("AI Assistant", gemini_response, "assistant")
                self.add_message("AI Assistant", "🔁 Is there anything else I can help you with? (yes/no):", "assistant")
                self.waiting_for_continue = True
                return

        # Disable input while processing
        self.input_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        # Process in background thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def gui_input(self, prompt=""):
        """Handle input requests from assistants in GUI mode"""
        if prompt.strip():
            self.add_message("AI Assistant", prompt, "assistant")

        # Set up waiting state
        self.pending_input_prompt = prompt
        self.waiting_for_assistant_input = True
        self.pending_input_response = None

        # Re-enable input for user response
        self.input_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.focus()

        # Wait for user response
        while self.waiting_for_assistant_input and self.pending_input_response is None:
            self.root.update()
            threading.Event().wait(0.1)  # Small delay to prevent busy waiting

        return self.pending_input_response or ""

    def gui_print(self, *args, **_):
        """Handle print requests from assistants in GUI mode"""
        message = " ".join(str(arg) for arg in args)
        if message.strip():
            self.add_message("AI Assistant", message, "assistant")

    def process_message(self, message):
        try:
            # Handle follow-up for feeling classification
            if self.waiting_for_followup:
                if any(word in message.lower() for word in ["song", "playlist", "listen to music", "music", "tune", "songs", "playlists"]):
                    command_type = CommandType.MUSIC
                    self.waiting_for_followup = False
                elif any(word in message.lower() for word in ["talk", "vent", "listen to me", "share", "express", "tell you", "someone to talk"]):
                    command_type = CommandType.PSYCHOLOGY
                    self.waiting_for_followup = False
                else:
                    self.followup_attempts += 1
                    if self.followup_attempts < 2:
                        self.root.after(0, self.handle_response, "", "Hmm... I didn't quite understand. Can you try rephrasing?", True)
                        return
                    else:
                        self.root.after(0, self.handle_response, "", "❓Still a bit unclear... Let me know if there's anything else I can help with.", True)
                        command_type = CommandType.GENERAL
                        self.waiting_for_followup = False
            else:
                # Check request limit 
                if not self.user.isPremium and self.request_count >= self.free_limit:
                    limit_msg = "🚫 Sorry, you have reached your plan limit. 💎 Please upgrade to premium or come back later after reset."
                    self.root.after(0, self.handle_response, "", limit_msg, False)
                    return

                # Classify command (same as main.py)
                command_type = classify_command(message, self)
                if command_type is None:  # Waiting for follow-up
                    return

            # Create request (same as main.py)
            self.user.preferences["raw_input"] = message
            request = Request(input_str=message, timestamp=datetime.now(), command_type=command_type)

            # Temporarily replace input/print for assistant execution
            import builtins
            original_input = builtins.input
            original_print = builtins.print
            builtins.input = self.gui_input
            builtins.print = self.gui_print

            try:
                # Select correct assistant or use Gemini API for general questions
                if command_type == CommandType.GENERAL:
                    # Use Gemini API for general questions
                    greeting = ""
                    gemini_response = call_gemini_api(message)
                    self.root.after(0, self.handle_response_with_continue, greeting, gemini_response, True)
                else:
                    # Use existing assistants for specific domains
                    if command_type == CommandType.MUSIC:
                        assistant = MusicAssistant(self.user)
                    elif command_type == CommandType.FITNESS:
                        assistant = FitnessAssistant(self.user)
                    elif command_type == CommandType.STUDY:
                        assistant = StudyAssistant(self.user)
                    elif command_type == CommandType.BOOK:
                        assistant = BookAssistant(self.user)
                    elif command_type == CommandType.PSYCHOLOGY:
                        assistant = PsychologyAssistant(self.user)
                    else:
                        assistant = AIAssistant(self.user)

                    # Get greeting and response - same as main.py
                    greeting = assistant.greetUser()
                    response = assistant.handleRequest(request)

                    # Ask to continue - same as main.py
                    self.root.after(0, self.handle_response_with_continue, greeting, response.message, True)

            finally:
                # Restore original input/print
                builtins.input = original_input
                builtins.print = original_print

        except Exception as e:
            self.root.after(0, self.handle_error, str(e))

    def handle_response_with_continue(self, greeting, response, success):
        if success:
            # Add greeting with emoji - same as main.py format
            self.add_message("AI Assistant", f"💡 {greeting}", "greeting")

            # Add main response with emoji - same as main.py format
            self.add_message("AI Assistant", f"🤖 {response}", "response")

            # Ask to continue - same as main.py
            self.add_message("AI Assistant", "🔁 Is there anything else I can help you with? (yes/no):", "assistant")
            self.waiting_for_continue = True

            # Update request counter only after user chooses to continue (like main.py)
            # This will be done in send_message when user responds
        else:
            self.add_message("System", response, "system")

        # Re-enable input
        self.input_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.focus()

    def handle_response(self, greeting, response, success):
        if success:
            # Add greeting
            if greeting:
                self.add_message("AI Assistant", greeting, "assistant")

            # Add main response
            self.add_message("AI Assistant", response, "assistant")

            # Update request counter
            self.update_requests_label()
        else:
            self.add_message("System", response, "system")

        # Re-enable input
        self.input_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.focus()

    def handle_error(self, error_msg):
        self.add_message("System", f"Error: {error_msg}", "system")

        # Re-enable input
        self.input_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.focus()

def main():
    root = tk.Tk()
    ChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


