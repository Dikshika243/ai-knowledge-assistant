class IntentService:

    SMALL_TALK_RESPONSES = {
        "hi": "Hello! 👋 How can I help you with your document?",
        "hello": "Hello! 👋 How can I help you with your document?",
        "hey": "Hi! 👋 Ask me anything about the uploaded document.",
        "thanks": "You're welcome! 😊",
        "thank you": "You're welcome! 😊",
        "ok": "😊",
        "okay": "😊",
        "bye": "Goodbye! Have a great day! 👋",
        "goodbye": "Goodbye! Have a great day! 👋"
    }

    @classmethod
    def get_response(cls, message: str):

        message = message.strip().lower()

        for key, response in cls.SMALL_TALK_RESPONSES.items():
            if key in message:
                return response

        return None