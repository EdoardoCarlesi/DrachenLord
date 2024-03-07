import streamlit as st
import pandas as pd
import drachenlord as dl



def main():
    """
    """

    st.title('Drachenlord Screamer Detector')
    
    #if 'noise_value' not in st.session_state:
    #    st.session_state.noise_value = 50
    
    #if 'duration_value' not in st.session_state:
    #    st.session_state.duration_value = 3

    # Initialize bar value with a default
    #noise_value = st.slider('Set noise threshold value', min_value=0, max_value=100, value=st.session_state.noise_value)
    #duration_value = st.slider('Set recording duration value', min_value=1, max_value=10, value=st.session_state.duration_value)

    #while True:

    #   if noise_value != st.session_state.noise_value or duration_value != st.session_state.duration_value: 
    #    st.session_state.noise_value = noise_value
    #    st.session_state.duration_value = duration_value
    #while noise_value == st.session_state.noise_value or duration_value == st.session_state.duration_value: 

    dl.main_loop(20) #noise_value, duration_value)


if __name__ == '__main__':
    """
    """

    main()
