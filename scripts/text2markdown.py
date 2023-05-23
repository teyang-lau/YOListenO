import openai

SYSTEM_CONTENT = """You are an assistant that only speaks in Markdown. Do not write text that isn't formatted as markdown.

Example formatting:

<h1 style="text-align: center;">YOListenO</h1>

## Summary

This audio recording documents a test of a workflow using AI to transcribe lecture audios to markdown formatted notes.

## Main Points

- point 1
- point 2

## Action Items

- point 1
- point 2

## Follow Up Questions

- point 1
- point 2

## Potential Arguments

- point 1
- point 2"""

USER_CONTENT = """Write a Title for the transcript that is under 15 words and center it using <h1 style="text-align: center;">Title</h1>

Write "Summary" as a Heading 1.

Write a summary of the provided transcript.

Then return a list of the main points in the provided transcript. Then return a list of action items. Then return a list of follow up questions. Then return a list of potential arguments against the transcript.

For each list, return a Heading 2 before writing the list items. Limit each list item to 100 words, and return no more than 5 points per list.

Transcript:
"""

def text2markdown(
    transcript: str,
    api_key: str,
    system_content: str=SYSTEM_CONTENT,
    user_content: str=USER_CONTENT,
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


