import asyncio
from STT import LiveSTT
from soundplayer import SoundInit
from LLM import Getting_response
from data_prepration import getting_values,data_creation
import random
from dotenv import load_dotenv,set_key
import os
import pandas as pd



class Assistant:
    def __init__(self):
        self.sound_player = SoundInit()
        self.model = Getting_response(model="Llama3-8b-8192")
        self.live_stt = LiveSTT(sound_player=self.sound_player)
        self.data = getting_values()

    async def audio_mapper(self, response):
        try:
            random_int = random.randint(0, 3)
            return f"{random_int}_{self.data[response]}"
        except KeyError:
            return None

    async def stt_worker(self):
        await self.live_stt.arun()

    async def llm_worker(self):
        while True:
            await asyncio.to_thread(self.sound_player.play_sound, "greetings.mp3")
            try:
                text = await self.live_stt.get_text()
                if text:
                    print(f"You said 🔊  :     {text}")
                    response = await self.model.process(text)
                    print(f"LLM response 🤖:     {response}")
                    audio_file = await self.audio_mapper(response)
                    if audio_file:
                        await asyncio.to_thread(self.sound_player.play_sound, audio_file)
                    else:
                        print("No matching audio file found.")
            except Exception as e:
                print(f"Error in LLM worker: {e}")

    async def run(self):
        await asyncio.gather(
            self.stt_worker(),
            self.llm_worker()
        )




if __name__ == "__main__":
    agent = Assistant()
    asyncio.run(agent.run())
    