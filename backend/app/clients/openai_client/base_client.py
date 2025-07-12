from openai import OpenAI

class OpenAIBaseClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def chat_completion(self, messages: list, model: str = "gpt-4", temperature: float = 0.3) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content