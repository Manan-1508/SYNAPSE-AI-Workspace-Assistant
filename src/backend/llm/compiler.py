from typing import List, Dict, Any, Optional

class ChatHistoryCompiler:
    """
    Compiles chat message logs from SQLite database into standard role-content dictionary
    formats acceptable by Generative AI SDKs and local models.
    """
    def __init__(self, max_history_tokens: int = 4000):
        self.max_history_tokens = max_history_tokens

    def compile(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Converts database messages into API format roles (user/model)."""
        formatted_messages = []
        for msg in messages:
            # Map SQLite sender roles to standard API formats
            role = "user" if msg["sender"] == "user" else "model"
            formatted_messages.append({
                "role": role,
                "parts": [msg["content"]]
            })
        return formatted_messages
