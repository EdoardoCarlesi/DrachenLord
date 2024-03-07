import logging
import logging.handlers
import librosa
import queue
import threading
import time
import urllib.request
import os
from collections import deque
from pathlib import Path
from typing import List
import av
import numpy as np
import pydub
import streamlit as st
import drachenlord as dl
from streamlit_webrtc import WebRtcMode, webrtc_streamer

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)


@st.cache_data  # type: ignore
def get_ice_servers():
    """Use Twilio's TURN server because Streamlit Community Cloud has changed
    its infrastructure and WebRTC connection cannot be established without TURN server now.  # noqa: E501
    We considered Open Relay Project (https://www.metered.ca/tools/openrelay/) too,
    but it is not stable and hardly works as some people reported like https://github.com/aiortc/aiortc/issues/832#issuecomment-1482420656  # noqa: E501
    See https://github.com/whitphx/streamlit-webrtc/issues/1213
    """

    # Ref: https://www.twilio.com/docs/stun-turn/api
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    return token.ice_servers

def main():
    st.header("Drachenlord screamer")
    st.markdown(
        """
        Raise the volume of your voice and DrachenLord will get mad at you
        """
    )
    
    #sound_only_page = "Sound only (sendonly)"
    #app_mode = st.selectbox("Choose the app mode", [sound_only_page])
    app_sst()

def app_sst(time_delta=5): 
    

    #chart = st.line_chart(y_axis=(-500, 3000))

    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": get_ice_servers()},
        media_stream_constraints={"video": False, "audio": True},
    )

    status_indicator = st.empty()

    if not webrtc_ctx.state.playing:
        return

    status_indicator.write("Loading...")
    text_output = st.empty()
    stream = None
    frame_rate = 1

    # Restart these variables!
    time_start = time.time()
    sound_tot = 0
    n_sound = 1

    threshold = 1500
    data = []

    while True:

        if webrtc_ctx.audio_receiver:

            sound_chunk = pydub.AudioSegment.empty()
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                status_indicator.write("No frame arrived.")
                continue

            status_indicator.write("Running. Say something!")

            for audio_frame in audio_frames:
                sound = pydub.AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                sound_chunk += sound
                
                time_now = time.time()
                chunk_val = np.mean(np.abs(sound_chunk.get_array_of_samples()))
                sound_tot += chunk_val 
                n_sound += 1

                data.append(chunk_val)

                if len(data) == 100:
                    med = np.mean(data)
                    data = [d - med for d in data]
                    #chart.line_chart(data)
                    data = data[50:]

                if (time_now - time_start) > time_delta:
                    sound_vol = sound_tot/n_sound
                    time_start = time.time()
                    n_sound = 0
                    sound_tot = 0

                    this_file = dl.get_random_audio_file()
                    
                    if sound_vol > threshold:

                        print("Sound detected!")
                        time.sleep(1)
                        # Play the chosen MP3 file
                        dl.play_audio(this_file)
                        audio_len = librosa.get_duration(filename=this_file)
                        print(f"Audio len: {audio_len}")
                        time.sleep(audio_len)
        
                #print(audio_frame, sound, sound_chunk)
                #print(len(sound_chunk.get_array_of_samples())) 
                #print(np.mean(sound_chunk.get_array_of_samples())) 
        else:
            status_indicator.write("AudioReciver is not set. Abort.")
            break


if __name__ == "__main__":
    import os

    DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
        "%(message)s",
        force=True,
    )

    logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

    st_webrtc_logger = logging.getLogger("streamlit_webrtc")
    st_webrtc_logger.setLevel(logging.DEBUG)

    fsevents_logger = logging.getLogger("fsevents")
    fsevents_logger.setLevel(logging.WARNING)

    main()
