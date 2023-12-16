import streamlit as st

from pytube import YouTube
from pydub import AudioSegment
import os
import io
import time
import ffmpeg
import assemblyai as aai
from dotenv import load_dotenv
from chatbot import ChatGPTFree

# Function to get YouTube video transcript
relativ_output_speech = "./video/speech.wav"


def download_video_and_convert_to_wav(url, input_filename="speech", output_path="./video/", output_speech="speech.wav"):
    start_time = time.time()

    # url input from user
    yt = YouTube(url)

    # Check if speech.wav already exists and delete it
    existing_wav_file = os.path.join(output_path, output_speech)
    if os.path.exists(existing_wav_file):
        os.remove(existing_wav_file)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=output_path, filename=input_filename)

    # save the file as MP3
    base, _ = os.path.splitext(out_file)
    mp3_file = base + '.mp3'
    os.rename(out_file, mp3_file)

    # convert MP3 to WAV
    wav_file = os.path.join(output_path, output_speech)
    command2wav = f"ffmpeg -i {mp3_file} {wav_file}"
    print(f"Running command: {command2wav}")
    os.system(command2wav)

    # remove the original MP3 file
    os.remove(mp3_file)

    # result of success
    print(f"{yt.title} has been successfully downloaded and converted to WAV.")

    end_time = time.time()

    print(f"Audio downloaded and converted to WAV: {wav_file}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    return wav_file


def main():
    st.title("YouTube Video Summarizer")
    # Get user input
    video_url = st.text_input("Enter YouTube URL:")
    st.write("For Example: https://www.youtube.com/watch?v=7TWKKww-F30")
    user_question = st.text_input("Ask a question about the video:")
    st.write("For Example: What should we learnt about this text ?")

    # Process input and display results
    if st.button("Summarize"):
        if not video_url:
            st.warning("Please enter a YouTube URL.")
        elif not user_question:
            st.warning("Please ask a question about the video.")
        else:
            st.info("Summarizing... This may take a moment.")

            # Execute
            output_directory = "./video/"

            # Ensure the output directory exists
            os.makedirs(output_directory, exist_ok=True)

            _ = download_video_and_convert_to_wav(video_url)

            # Load environment variables from .env file
            load_dotenv()
            apiKey = os.getenv("APIKEY")

            aai.settings.api_key = apiKey
            transcriber = aai.Transcriber()

            # transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
            transcript = transcriber.transcribe(relativ_output_speech)

            # ChatGPT Query
            question = user_question + f"from this text that is between the simple quote: '{transcript.text}'"
            user = ChatGPTFree()
            driver = user.logInChatGPT()
            answer = user.questionRequest(question, driver, questionTime=60)

            if answer:
                st.subheader("Summary:")
                st.write(answer)


if __name__ == "__main__":
    main()
