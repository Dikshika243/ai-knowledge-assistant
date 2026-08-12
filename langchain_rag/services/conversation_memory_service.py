from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
)


class ConversationMemoryService:

    def __init__(self):
        self._history: list[BaseMessage] = []

    def add_user_message(self, message: str) -> None:
        self._history.append(
            HumanMessage(content=message)
        )

    def add_ai_message(self, message: AIMessage) -> None:
        self._history.append(message)

    def get_history(self) -> list[BaseMessage]:
        return self._history

    def clear(self) -> None:
        self._history.clear()