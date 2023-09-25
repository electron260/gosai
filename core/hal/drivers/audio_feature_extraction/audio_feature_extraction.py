from core.hal.drivers.driver import BaseDriver
import time 

class Driver(BaseDriver):

    def __init__(self, name, parent, max_fps = 120):
        super().__init__(name, parent)
        self.fps = max_fps

        #register to driver event (for example camera driver)
        self.register_to_driver("microphone", "audio_stream")


        #create module event
        self.create_event("audio_emotion")
        self.create_event("audio_transcription")
        self.create_event("audio_speaker_id")

        self.fps = max_fps

    def pre_run(self):
        # runs to do at the start of the driver
        super().pre_run()

    def loop(self):
        start_t = time.time()

        # update event
        audio, sr = self.parent.get_driver_event_data("microphone","audio_stream")
        

        
        dt = max(1 / self.fps - (time.time() - start_t), 0.0001)
        time.sleep(dt)  #to temporize