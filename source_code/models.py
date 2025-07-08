from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Dict

class CommandType(Enum):
    # Recommends music playlists based on user's mood, favorite artists, or activiies
    MUSIC = "MUSIC" 
    # Recommends fitness schedule and exericse, creates detailed workout plans based on user's body goal 
    # and time available for working out.
    FITNESS = "FITNESS" 
    # Recommends study tips, schedules study sessions, explains topics which user is struggling
    STUDY = "STUDY" 
    # General conversations
    GENERAL = "GENERAL" 
    # A personal AI psychologist who will listen to user's thoughts, offer advices to help user cope with 
    # temporary stress, mild depression; Analyze and explain some interesting psychological phenomena that
    # users are curious about
    PSYCHOLOGY = "PSYCHOLOGY" 
    # Recommends books based on keywords in user's description, favorite genre, and provides the links
    # for users to buy those books or read them online
    BOOK = "BOOK" 
    # A personal AI nutritionist who helps monitor and optimize user's daily intake. It tracks consumed foods,
    # calculates macro- and micronutrients and sends alerts to users when they exceed recommended dietary limits.
    # Recommends foods to increase or reduce based on deficiences or overconsumption patterns.
    NUTRITION = "NUTRITION" # NOT DONE YET
    # Provides user with general legal information, guidance on legal topics, and access to relevant resources
    # based on user queries
    LEGAL = "LEGAL" # NOT DONE YET
    # Helps user manage their personal finances by offering tailored insighs, budgeting suggestions, and alerts
    # related to financial health
    FINANCIAL = "FINANCIAL" # NOT DONE YET

@dataclass
class UserProfile:
    name: str
    age: int
    preferences: Dict[str, str]
    isPremium: bool

    def __post_init__(self):
        if not self.name:
            raise ValueError("Please enter your name. User name cannot be empty.")
        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError("Please enter your age. Age cannot be a negative number.")
        if not isinstance (self.preferences, dict):
            raise ValueError("Preferences must be a dictionary.")

@dataclass
class Request:
    input_str: str
    timestamp: datetime
    command_type: CommandType

    def __post_init__(self):
        if not self.input_str:
            raise ValueError("Input cannot be empty")

@dataclass
class Response:
    message: str
    confidence: float
    actionPerformed: bool

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")