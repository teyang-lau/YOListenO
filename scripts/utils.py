"""
Utility Functions
"""

import os
import re


def save_uploaded_file(uploadedfile, tempDir):
    orig_video_path = os.path.join(tempDir, "orig_video")
    if not os.path.exists(orig_video_path):
        os.makedirs(orig_video_path)
    with open(os.path.join(orig_video_path, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    # st.success("Saved file :{} in tempDir".format(uploadedfile.name))

    return os.path.join(orig_video_path, uploadedfile.name)


def break_chunks(
    tokens: list,
    puncs: list,
    min_chunk: int,
    max_chunk: int,
) -> list:
    """Breaks list into chunks of min and max size based on punctuations

    Args:
        tokens (list): list of elements (does not need to be tokens)
        puncs (list): list of punctuations to split on
        min_chunk (int): min tokens in chunk before splitting
        max_chunk (int): max tokens in chunk before splitting

    Returns:
        list: list of strings in chunks
    """

    chunk_idx = 0  # track current chunk size
    curr_punc_idx = 0  # closest idx of punctuation to chunk size
    prev_punc_idx = 0  # previous idx of punctuation used to break chunk
    chunk_end_indices = []  # initialize to store chunk end indices
    for i, token in enumerate(tokens):
        # track punctuations idx that are smaller than chunk size
        if token in puncs and chunk_idx <= max_chunk:
            curr_punc_idx = i
        # if punctuation idx is bigger than chunk size, attempt to break the chunk
        if chunk_idx > max_chunk:
            # print(chunk_idx, i, curr_punc_idx, prev_punc_idx)
            # split on previous punctuation if chunk has sufficient tokens
            if curr_punc_idx - prev_punc_idx >= min_chunk:
                chunk_end_indices.append(curr_punc_idx)
                prev_punc_idx = curr_punc_idx
                chunk_idx = i - curr_punc_idx - 1
            # else, just split on the current token
            else:
                chunk_end_indices.append(i)
                chunk_idx = -1
        chunk_idx += 1

    # get the tokens into chunks
    s = 0
    token_chunks = []
    for i in chunk_end_indices:
        token_chunks.append(tokens[s : i + 1])
        s = i + 1
    if len(tokens[s:]) >= 100:  # account for last chunk
        token_chunks.append(tokens[s:])

    # join each chunk into string
    token_chunks_joined = []
    for chunk in token_chunks:
        joined = " ".join(chunk)
        joined = re.sub(r" ([^A-Za-z0-9])", r"\1", joined)
        token_chunks_joined.append(joined)

    return token_chunks_joined