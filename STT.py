import asyncio
import pyaudio
import numpy as np
from faster_whisper import WhisperModel
import threading
import queue
import time
import wave
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from soundplayer import SoundInit

def is_speech(data, threshold=5000):
    audio_data = np.frombuffer(data, dtype=np.int16)
    energy = np.sum(np.abs(audio_data))
    return energy > threshold

class LiveSTT:
    def __init__(self, model_name="base", record_seconds=10, device_index=1, sound_player=None):
        self.model = WhisperModel(model_name)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = record_seconds
        self.device_index = device_index
        self.sound_player = sound_player

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      input_device_index=self.device_index,
                                      frames_per_buffer=self.CHUNK)
        self.queue = queue.Queue()
        self.text_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.audio_queue = queue.Queue()
        print("LiveSTT initialized")
        
    
    async def _put_text(self, text):
        await self.text_queue.put(text)

    def capture_audio(self):
        while True:
            data = self.stream.read(self.CHUNK)
            if is_speech(data) and not self.sound_player.is_playing.is_set():
                self.queue.put(data)
            else:
                if not self.queue.empty():
                    audio_chunks = []
                    while not self.queue.empty():
                        audio_chunks.append(self.queue.get())
                    if audio_chunks:
                        self.transcribe_audio(b''.join(audio_chunks))

    def transcribe_audio(self, audio_data):
        temp_filename = "temp.wav"
        with wave.open(temp_filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
        
        try:
            segments, _ = self.model.transcribe(temp_filename,
                                                vad_filter=True,
                                                vad_parameters=dict(min_silence_duration_ms=500))
            if not segments:
                print("No speech detected.")
            else:
                for segment in segments:
                    if segment.text.strip():  
                        asyncio.run(self._put_text(segment.text))
                else:
                        pass

        except Exception as e:
            pass
        finally:
            os.remove(temp_filename)
            
    
    async def get_text(self):
            return await self.text_queue.get()
            

    def run(self):
        capture_thread = threading.Thread(target=self.capture_audio)
        capture_thread.start()
        print("Live STT system is running...")  
        
        
    async def arun(self):
        self.run()
        while True:
            await asyncio.sleep(0.1)  

if __name__ == "__main__":
    pass
    # obj = LiveSTT()
    # obj.run()
    # agent = SoundInit()