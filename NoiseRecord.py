import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
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

# Set parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = int(input("Enter noise recording  in seconds: "))
WAVE_OUTPUT_FILENAME = "audio.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

print("Recording...")
frames = []

# Record for specified duration
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop recording and close PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# Save recording to file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("Saved recording to file:", WAVE_OUTPUT_FILENAME)

# Upload file to Firebase storage
remote_file_name = 'audiotest/file.wav'
remote_blob = bucket.blob(remote_file_name)
remote_blob.upload_from_filename(WAVE_OUTPUT_FILENAME)

# Get public URL of uploaded file
url = remote_blob.public_url
print('Uploaded file URL:', url)
