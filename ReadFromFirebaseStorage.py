import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import pyaudio
import wave

# Initialize Firebase app with credentials
cred = credentials.Certificate('website-pde2101-firebase-adminsdk-jrepn-1483e61246.json')
options = {
    'storageBucket': 'website-pde2101.appspot.com'
}
firebase_admin.initialize_app(cred, options)

# Get a reference to the Firebase storage bucket
bucket = storage.bucket()

# Get reference to the audio file to be downloaded
remote_file_name = 'audiotest3/output.wav'
remote_blob = bucket.blob(remote_file_name)

# Download the file's content as a string
audio_content = remote_blob.download_as_string()

# Write the audio content to a local .wav file
local_file_name = 'audio_local.wav'
with wave.open(local_file_name, 'wb') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(audio_content)

# Play the audio using PyAudio
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
with wave.open(local_file_name, 'rb') as wf:
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
stream.stop_stream()
stream.close()
audio.terminate()
