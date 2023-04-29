import os
import requests
from io import BytesIO

def transcribe_audio(audio_segment):
    url = 'https://api.openai.com/v1/audio/transcriptions'
    api_key = os.environ["API_KEY"]

    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': 'whisper-1'
    }
    
    # Convert the audio_segment to a BytesIO object in the desired format
    audio_file = BytesIO()
    audio_segment.export(audio_file, format="mp4")
    audio_file.seek(0)
    
    files = {
        'file': ('audio.mp4', audio_file, 'audio/mp4')
    }

    response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code == 200:
        json_response = response.json()
        # Extract the transcribed text from the response
        transcribed_text = json_response['text']
        return transcribed_text
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""