from openai import OpenAI

class MessageGenConfig:
    def __init__(self):
        pass

class MessageGenPrompt:
    def __init__(self, head_reply, head_talk, body):
        self.head_reply = head_reply
        self.head_talk = head_talk
        self.body = body

class MessageGen:
    def __init__(self, config : MessageGenConfig, prompt : MessageGenPrompt):
        self._client = OpenAI()
        self._config = config
        self._prompt = prompt

    def api_access(self,messages):
        return self._client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)

    def reply_gen(self):
        messages = [
                        {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "あなたは優秀な知識人です。ユーザからの質問に答えてください。"
                            }
                        ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "有名なラーメン屋さんを5つ教えてください"
                                }
                            ]
                        }
                    ]

        response = self.api_access(messages)

        return response.choices[0].message.content

    def talk_gen(self):
        pass

