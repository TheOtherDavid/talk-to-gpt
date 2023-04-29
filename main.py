import audio
import gpt
import whisper
import time
import logging_utils

logger = logging_utils.get_logger()

def main():
    #First we record ten seconds of audio
    input("Press any key to record.")
    filename = f"audio_{time.strftime('%Y%m%d_%H%M%S')}.wav"
    audio_prompt = audio.record_audio_until_keystroke(filename)

    #Then we transcribe the audio
    transcribed_text = whisper.transcribe_audio(audio_prompt)
    print(transcribed_text)
    #Then we send the text to GPT and get the response
    response = gpt.get_gpt_response(transcribed_text)
    #Then we print the response.
    print(response)
    logger.info(response)
    #Then we send the response to the speaker
    audio.convert_text_to_audio(response)
    print("program complete")


if __name__ == '__main__':
    response = main()