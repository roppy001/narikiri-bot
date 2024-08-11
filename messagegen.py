from openai import OpenAI


class MessageGenConfig:
    def __init__(self):
        pass


class MessageGen:
    def __init__(self, config: MessageGenConfig, prompt):
        self._client = OpenAI()
        self._config = config
        self._prompt = prompt

    def api_access(self, messages):
        return self._client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)

    def reply_gen(self, question_message, past_messages):
        user_content = []

        for mes in past_messages:
            user_content.append({
                "type": "text",
                "text": mes
            })

        user_content.append({
            "type": "text",
            "text": "以下の質問に答えてください:\n" + question_message
        })

        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "あなたはChatbotとして、以下の制約条件を厳密に守ってロールプレイを行い、"
                        +"質問に回答してください\n\n" + self._prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": user_content
            }
        ]

        response = self.api_access(messages)

        return response.choices[0].message.content

    def talk_gen(self, past_messages):
        user_content = []

        for mes in past_messages:
            user_content.append({
                "type": "text",
                "text": mes
            })

        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "あなたはChatbotとして、以下の制約条件を厳密に守ってロールプレイを行い、"
                        +"雑談に参加し何かメッセージを伝えてください。\n\n" + self._prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": user_content
            }
        ]

        response = self.api_access(messages)

        return response.choices[0].message.content
