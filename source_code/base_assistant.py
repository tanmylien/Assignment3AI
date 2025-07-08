from source_code.models import UserProfile, Request, Response

class AIAssistant:
    def __init__(self, user: UserProfile):
        self.user = user

    def greetUser(self) -> str:
        return f"Hello, {self.user.name}! How can I assist you today?"

    def handleRequest(self, request: Request) -> Response:
        return self.generateResponse("I'm here to help!", confidence=0.7)

    def generateResponse(self, message: str, confidence: float = 1.0) -> Response:
        return Response(message=message, confidence=confidence, actionPerformed=True)
