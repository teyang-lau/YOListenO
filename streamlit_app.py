import streamlit as st
import tempfile
import re
from scripts.utils import save_uploaded_file, break_chunks
from scripts.whisper_transcribe import wtranscribe
from scripts import text2markdown, summarize
# from scripts import credentials # REMOVE CREDENTIALS

# create temp dir for storing video and outputs
temp_dir = tempfile.TemporaryDirectory()
temp_path = temp_dir.name

__, col, __ = st.columns([1, 3, 1])
with col:
    st.image("./images/notebook_logo_transparent.png")

with st.expander("How to Use YOListenO"):
    instruct = """
    1. Upload a lecture/meeting audio or video file
    2. Select whether you want the output as a lecture or meeting note
    3. (Optional): Adjust advanced settings for better fine-tuning and click "Submit" for each adjusted tab
    4. (Optional): Use your own OpenAI api key under advanced settings as the default has a limit
    5. Click "Start YOListenO" and let the magic begin! 
    """
    st.write(instruct)


st.write("# Upload Audio/Video:\n")

file = st.file_uploader(
    "Choose a File", accept_multiple_files=False, type=["mp3", "wav", "mp4", "mov", "mpeg"],
)

if file is not None:
    # save uploaded file to temp location
    file_details = {"FileName": file.name, "FileType": file.type}
    file_path = save_uploaded_file(file, temp_path)

    # user options
    with st.expander("Settings", expanded=True):
        note_type = st.selectbox(
                'Desired Note Type:',
                ('Lecture', 'Meeting')
        )
        if note_type == 'Lecture':
            sys_content = text2markdown.SYSTEM_CONTENT_LECTURES
            use_content = text2markdown.USER_CONTENT_LECTURES
        elif note_type == 'Meeting':
            sys_content = text2markdown.SYSTEM_CONTENT_MEETINGS
            use_content = text2markdown.USER_CONTENT_MEETINGS
    
    # user advanced settings
    with st.expander("Advanced Settings"):
        system, user, additional = st.tabs(["System Content", "User Content", "Additional Settings"])

        with system:
            with st.form("system_content_form"):
                system_content = st.text_area(
                    label='System Content (leave as default if unsure)',
                    value=sys_content,
                    help='Provide system role to set behavior of the assistant and provide high level instructions for the conversation',
                    placeholder=sys_content
                )   
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit System Content")
            
            st.subheader('Preview')
            st.info(system_content)

        with user:
            with st.form("user_content_form"):
                user_content = st.text_area(
                    label='User Content  (leave as default if unsure)',
                    value=use_content,
                    help='Specific instructions from the user for the assistant',
                    placeholder=use_content
                )   
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit User Content")
            
            st.subheader('Preview')
            st.info(user_content)
        
        with additional:
            with st.form("add_settings_form"):
                temp = st.number_input(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.2,
                    step=0.1,
                    help="How creative and random the markdown output is. 0 will give straightforward, deterministic responses, while 1 will give wildly varied responses.",
                )
                transcript_max_token_len = st.number_input(
                    "Transcript Max Token Length",
                    min_value=0,
                    max_value=4000,
                    value=2500,
                    step=100,
                    help="The number of tokens in transcript before chunking is used. This is a workaround for very long transcripts as GPT3.5 cannot handle >4k tokens."
                )
                summarized_chunk_max_len = st.number_input(
                    "Chunking Summary Max Length",
                    min_value=50,
                    max_value=500,
                    value=200,
                    step=50,
                    help="The maximum length of each summarized chunk if chunking is performed for very long transcripts."
                )
                apikey = st.text_input(
                    label='API Key (Optional)',
                    type="password",
                    help="Use your own OpenAI key if possible. Else, it will use mine but there is a limit every month."
                )

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit Additional Settings")

    convert_bt = st.button("Start YOListenO!")
    if convert_bt:
        
        if not apikey:
            # apikey = credentials.api_key # CHANGE THIS TO SECRET 
            apikey = st.secrets["API_KEY"]

        # transcribe
        with st.spinner(text="YOListenO working its magic: Transcribing..."):
            transcript = wtranscribe(
                model='base',
                audio=file_path,
                temperature=0.2,
            )
            transcript_orig = transcript

        # tokenize and check length. 
        tokens = re.findall(r"[\w']+|[.,!?;]", transcript)
        if len(tokens) > transcript_max_token_len:
            # break into smaller chunks, summarize each chunk, and merge back together
            with st.spinner(text="YOListenO working its magic: Chunking & Summarizing..."):
                # perform chunking
                chunks = break_chunks(tokens, [".", ",", "!", "?", ";"], 700, 1100)
                # summarise each chunk
                summarized_chunks = []
                for chunk in chunks:
                    summary = summarize.summarize(
                        text=chunk,
                        api_key=apikey,
                        summarized_max_len=summarized_chunk_max_len,
                    )
                    summarized_chunks.append(summary)
                # join summarised chunks into transcript
                transcript = ' '.join(summarized_chunks)

        # convert to markdown
        with st.spinner(
            text="YOListenO working its magic: CONVERSION IN PROGRESS ..."
        ):
            result = text2markdown.text2markdown(
                transcript=transcript, 
                api_key=apikey,
                system_content=system_content,
                user_content=user_content,
                temperature=temp,
            )

        tab_transcript, tab_markdown, tab_raw= st.tabs(
            [
                "Transcript and Audio",
                "Markdown Preview",
                "Raw Markdown"
            ]
        )

        # display transcript and audio
        with tab_transcript:
            audio_file = open(file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes)
            st.info(transcript_orig)

        with tab_markdown:
            st.header('Preview')
            st.divider()
            st.markdown(result)

        with tab_raw:
            st.header('Raw Output')
            st.divider()
            st.text(result)


with st.expander("About YOListenO"):
    __, col2, __ = st.columns([1, 1, 1])
    with col2:
        st.image("./images/notebook_logo_transparent.png")

    about = """
    **[YOListenO (You Only Listen Once)](https://github.com/teyang-lau/YOListenO)** is an AI tool making use of OpenAI's 
    [Whisper](https://github.com/openai/whisper) and [GPT3.5](https://platform.openai.com/docs/guides/chat)
    for turning audio/video lectures/meetings into markdown notes.
    
    **Created by:**
    * LAU TeYang
    """
    st.write(about)
    st.write("")
