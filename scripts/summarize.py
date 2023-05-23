import openai

USER_CONTENT = "Summarise in no more than {} words:\n"

def summarize(
    text: str,
    api_key: str,
    summarized_max_len: int = 200,
    user_content: str = USER_CONTENT,
    temperature: float = 0.2,
    max_tokens: int = 2000,
):

    openai.api_key = api_key
    user_content = "Summarise in no more than {} words:\n".format(summarized_max_len) + text
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": user_content},
        ],
    )

    return completion.choices[0].message.content