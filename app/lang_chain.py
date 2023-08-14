import openai


class LangChainAgent:
    def __init__(self, openai_api_key):
        # openai_api_key = "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"
        openai.api_key = openai_api_key

    def start(self, context):
        self.messages = [{"role": "system", "content": context}]
        self.messages.append({"role": "user", "content": '{"CUSTOMER":"START"}'})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        self.messages.append(response.choices[0].message)
        print(response)

        return response.choices[0].message.content

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        self.messages.append(response.choices[0].message)
        print(response)
        return response.choices[0].message.content

    def send_context_and_message(self, context, message):
        self.messages = [{"role": "system", "content": context}]
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        self.messages.append(response.choices[0].message)
        print(response)

        return response.choices[0].message.content
