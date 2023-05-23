import whisper

# requires command-line tool ffmpeg (not python ffmpeg) installed on computer
# download ffmpeg and put into C drive
# add ffmpeg/binary folder to Windows system variables PATH and restart computer


def wtranscribe(
    model: "Whisper",
    audio: str,
    initial_prompt: str = "Hello, this is a recorded lecture",
    temperature: float = 0.2,
) -> dict:
    """_summary_

    Args:
        model (Whisper): _description_
        audio (str): _description_
        initial_prompt (str, optional): _description_. Defaults to "Hello, this is a recorded lecture".
        temperature (float, optional): _description_. Defaults to 0.2.

    Returns:
        dict: _description_
    """

    wmodel = whisper.load_model(model)
    result = wmodel.transcribe(
        audio=audio,
        initial_prompt=initial_prompt,
        temperature=temperature
    )

    return result["text"]


if __name__ == "__main__":
    wtranscribe()
