from core.hal.drivers.driver import BaseDriver
import numpy as np
from scipy.signal import resample
from core.hal.drivers.speech_to_text.fast_whisper.fast_whisper import WhisperModel
import time
import samplerate
import webrtcvad

class Driver(BaseDriver):

    def __init__(self, name: str, parent):
        super().__init__(name, parent)

        #create driver event
        self.register_to_driver("microphone", "audio_stream")
        
        self.create_event("activity")

    def pre_run(self):
        """Runs once at the start of the driver"""
        super().pre_run()

        self.blocks = []

        self.patience = 0
        self.window = []
        self.vad = webrtcvad.Vad(2)

        # self.model, self.utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
        #                             model='silero_vad',
        #                             force_reload=True)



        
        self.create_callback_on_event("activity", self.activity, "microphone", "audio_stream")

    def activity(self, data):
        """Estimates the frequency of the input data"""

        frame = data["block"][:, 0]
        # change the time needed depending on the Activity detection Module 
       
       
        
        #self.blocks.extend(block)
        sample_rate = data["samplerate"]
        # convert the sample rate 
        
        frame = samplerate.resample(frame, 16000 * 1.0 / 48000, 'sinc_best')  


        frame = np.int16(frame * 32768)

        print(len(frame))
        # get speech timestamps from full audio file
        #self.model(audio, 16000).item()
        pred = self.vad.is_speech(frame.tobytes(), 16000)
        
        self.window.append(pred)
        if len(self.window) <= 3 :
            self.window.append(pred)
        elif len(self.window) == 4 :
            if True in self.window :
                pred = True 

            self.window = self.window[1:]

        

        print('confidence : ', pred)
        self.set_event_data(
            "activity",
            {
                "confidence": pred,
            },
        )
        self.blocks = []


        

        


        # self.set_event_data("frequency", {
        #     "max_frequency": freq[np.argmax(rfft)],
        #     "rfft": list(rfft[freq<self.MAX_FREQUENCY]),
        #     "amplitude": np.max(rfft),
        #     "blocksize": len(block),
        # })
