import openai
from .prompt_templates import SYSTEM_CONTENT_LECTURES, USER_CONTENT_LECTURES, SYSTEM_CONTENT_MEETINGS, USER_CONTENT_MEETINGS


def text2markdown(
    transcript: str,
    api_key: str,
    system_content: str=SYSTEM_CONTENT_LECTURES,
    user_content: str=USER_CONTENT_LECTURES,
    temperature: float=0.2,


):
    user_content = user_content + transcript
    openai.api_key = api_key

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
    )

    return completion.choices[0].message.content


