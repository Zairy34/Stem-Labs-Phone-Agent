import pygame
import os
import threading
import time

class SoundInit:
    def __init__(self) -> None:
        self.path_mp3file =  r'D:\Artificial-intelligance\Challanges\UI\Voiceovers'
        pygame.mixer.init()
        self.is_playing = threading.Event()

    def play_sound(self, file_name):
        try:
            pygame.mixer.music.load(os.path.join(self.path_mp3file, file_name))
            self.is_playing.set()  # Set the flag to indicate audio is playing
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            self.is_playing.clear()  # Clear the flag when audio stops playing
        except Exception as e:
            print(f"Error playing {file_name}: {e}")
            self.is_playing.clear()

    

if __name__ == "__main__":
    pass