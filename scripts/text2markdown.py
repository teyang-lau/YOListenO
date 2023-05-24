import openai
from .prompt_templates import SYSTEM_CONTENT_LECTURES, USER_CONTENT_LECTURES, SYSTEM_CONTENT_MEETINGS, USER_CONTENT_MEETINGS


def text2markdown(
    transcript: str,
    api_key: str,
    system_content: str=SYSTEM_CONTENT_LECTURES,
    user_content: str=USER_CONTENT_LECTURES,
    temperature: float=0.2,
) -> str:
    """Convert transcript into summarized markdown note

    Args:
        transcript (str): transcript for conversion
        api_key (str): openai api key
        system_content (str, optional): System role content prompt for chat completion. Defaults to SYSTEM_CONTENT_LECTURES.
        user_content (str, optional): User role content prompt for chat completion. Defaults to USER_CONTENT_LECTURES.
        temperature (float, optional): Controls creativity of the output. Higher is more varied and creative. Defaults to 0.2.

    Returns:
        str: converted summarized raw markdown note
    """
    user_content = user_content + transcript
    openai.api_key = api_key

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
    )

    return completion.choices[0].message.content


