from groq import Groq 
from src.memory import ConversationMemory 

class ChatClient:
    
    
    def __init__(self, config: dict):
        # Groq client - reads GROQ_API_KEY automatically if not passed 
        self._client = Groq(api_key=config["api_key"])
        self._model = config["model"]
        self._system = config["system_prompt"]
        self._max_tokens = config["max_tokens"]
        
    def _build_messages(self, memory: ConversationMemory) -> list[dict]:
        
        
        system_message = {"role": "system", "content": self._system}
        return [system_message] + memory.get_history()
    
    
    def send(self, memory: ConversationMemory) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=self._build_messages(memory),
            max_tokens=self._max_tokens,
            stream=False,
        )
        
        return response.choices[0].message.content
    
    def send_streaming(self, memory: ConversationMemory) -> str:
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=self._build_messages(memory),
            max_tokens=self._max_tokens,
            stream=False,
        )
        
        full_text = response.choices[0].message.content
        print(full_text, end="", flush=True)
        return full_text 