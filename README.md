# Assignment #3 AI ASSISTANT

## 📦 How to Run the Program

### Step 1: Clone this repository
Open your terminal and run:
```
git clone https://github.com/tanmylien/Assignment3AI.git

cd Assignment3AI
```
Make sure Python is installed

### Step 2: Set your Gemini API Key

To run this project, you need a Gemini API key. You can register for one at _aistudio.google.com_

First, open the file _source_code/chat_gui.py_

Secondly, find a function **call_gemini_api(...)** around **line 61**

Then, replace a placeholder ***'your-Gemini-API'*** with your actual key

### Step 2: Run the assistant
In the source_code folder, launch the assistant with:
```
PYTHONPATH=. python source_code/chat_gui.py
```
### Step 3: Interact with the assistant
The program will prompt you for your name, age, and whether you’re a premium user.<br/>
<br/>
Then you can type in requests like:<br/>
<br/>
	•	_"Play me something calm"_<br/>
	•	_"I want to build muscle"_<br/>
	•	_"Help me study for math"_<br/>
	•	_"Recommend a good fantasy book"_<br/>
	•	_"I'm feeling overwhelmed"_<br/>

**Free vs Premium Users**<br/>
	•	Free users can interact with assistants, but are limited to 3 high-level requests per session.<br/>
	•	Premium users have unlimited access.<br/>

## 🔍 Overview of the Assistant Functionality

This AI Assistant simulates a modular, multi-functional virtual assistant that can interact with users across various domains. Based on user input and preferences, it dynamically selects the appropriate assistant subclass to handle specific types of requests. Each assistant responds with customized messages and behaviors based on the context.<br/>

### Supported Functionalities:
🎵 **Music Assistant (MUSIC)** <br/>
Recommends music playlists based on the user’s current mood, favorite artists, or activities. Offers a wide variety of emotional tones and genres to suit personal preferences.<br/>
<br/>
💪 **Fitness Assistant (FITNESS)** <br/>
Suggests fitness plans, workout schedules, and exercises tailored to the user’s body goals and available time. Differentiates plans based on intensity and user fitness level. <br/>
<br/>
📚 **Study Assistant (STUDY)** <br/>
Helps users study smarter by offering personalized study tips, topic explanations, and the ability to schedule sessions based on areas of difficulty. <br/>
<br/>
🧠 **Psychology Assistant (PSYCHOLOGY)** <br/>
Acts as a conversational AI psychologist. Listens to the user’s thoughts, offers helpful coping strategies for stress, burnout, or mild depression, and provides insights into psychological phenomena when users are curious. <br/>
<br/>
📖 **Book Assistant (BOOK)** <br/>
Recommends books using keywords in user descriptions and genre preferences. Also provides online links to read or purchase recommended books. <br/>
<br/>
💬 **General Assistant (GENERAL)**
Handles general, undefined inputs in a friendly, helpful way when no specific category is matched. Ensures the conversation continues smoothly even with vague or ambiguous requests.

## Concepts Implemented <br/>
**Custom Data Types** <br/>
Defined UserProfile, Request, and Response in models.py using @dataclass. <br/>
<br/>
**Validation / Type-Safety:** <br/>
Validation logic is in the __post_init__ methods of the data classes to ensure correct data types and constraints. <br/>
<br/>
**Enumeration:** <br/>
CommandType enum in models.py defines valid request types (e.g., MUSIC, STUDY). <br/>
<br/>
**Dynamic Behavior & Object Simulation:** <br/>
In main.py, multiple user profiles are created and handled dynamically using their command types to choose the appropriate assistant. <br/>
<br/>
**Command Parsing (Bonus):** <br/>
classify_command() in main.py uses string matching to simulate intent recognition. <br/>
<br/>
**Inheritance & Polymorphism:** <br/>
The program uses ***inheritance*** to create a modular structure where all assistant types inherit from a common base class:<br/>
<br/>
**AIAssistant** is the base class that defines shared behaviors and method templates such as **greetUser()**, **handleRequest(request)**, and **generateResponse(message)** <br/>
<br/>
Specialized assistants inherit from AIAssistant and override these methods with custom behavior:<br/>
<br/>
	•	MusicAssistant: recommends playlists based on mood<br/>
	•	FitnessAssistant: suggests workouts based on user goals<br/>
	•	StudyAssistant: helps with study routines<br/>
	•	BookAssistant: recommends books by genre or keywords<br/>
	•	PsychologyAssistant: responds to emotional support requests<br/>
<br/>
***Polymorphism*** shows up in the way the program picks the right assistant **while the program is running**, based on what the user says.
<br/>
<br/>
	•	In **main.py**, we use the **classify_command()** function to figure out what kind of help the user wants, like music, books, fitness, or something else.<br/>
	•	Once we know the type, the program creates the right kind of assistant (like MusicAssistant or BookAssistant), but it doesn’t need to treat them differently after that.<br/>
<br/>
No matter which assistant is created, the program simply calls methods like **greetUser()** and **handleRequest(request)**. Because each assistant has its own custom version of these methods, the right response is automatically used. 

## AI-use citations

Inspired by ChatGPT and DeepSeek

OpenAI. (2025). ChatGPT [June 21 version]. https://chat.openai.com

DeepSeek. (2025). DeepSeek-R1-0528 [May 28 version]. https://chat.deepseek.com

Other than the AI-generated emoji responses and the AI-assisted summarization of the README.MD file, all remaining work is my own.

I used AI to generate multiple response variations for each AI Assistant. The ideas were originally mine, I just used AI to help expand the number of hardcoded responses so that users can receive something unique each time.

Because the ChatGPT model I often interact with uses fun emojis to enhance the emotional tone of the conversation, I thought it would be a good idea to add emojis to the AI Assistants’ responses to simulate that experience.
