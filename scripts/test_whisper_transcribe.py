from .whisper_transcribe import wtranscribe


def test_can_transcribe_to_text():
    result = wtranscribe("base", "../samples/audio/sample2.mp3")
    assert isinstance(result, str)


# def test_can_get_same_temperature_output():
#     result = wtranscribe("base", "../samples/audio/sample2.mp3", temperature=0.2)
#     result1 = wtranscribe("base", "../samples/audio/sample2.mp3", temperature=0.2)

#     assert result.lower() == result1.lower()


# def test_can_get_different_temperature_output():
#     result = wtranscribe("base", "../samples/audio/sample2.mp3", temperature=0.2)
#     result1 = wtranscribe("base", "../samples/audio/sample2.mp3", temperature=0.8)

#     assert result.lower() != result1.lower()
