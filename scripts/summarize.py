import openai

USER_CONTENT = "Summarise in no more than {} words:\n"

def summarize(
    text: str,
    api_key: str,
    summarized_max_len: int = 200,
    user_content: str = USER_CONTENT,
    temperature: float = 0.2,
    max_tokens: int = 500,
) -> str:
    """Summarize text using GPT3.5

    Args:
        text (str): text for summarizing
        api_key (str): openai api key
        summarized_max_len (int, optional): max length of summarized content. Defaults to 200.
        user_content (str, optional): user role content prompt for conversation. Defaults to USER_CONTENT.
        temperature (float, optional): control creativity of output. Higher is more varied and creative. Defaults to 0.2.
        max_tokens (int, optional): max tokens for the conversation. Defaults to 500.

    Returns:
        str: summarized text
    """
    openai.api_key = api_key
    user_content = user_content.format(summarized_max_len) + text
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": user_content},
        ],
    )

    return completion.choices[0].message.content