import streamlit as st
import random

st.set_page_config(layout="wide", page_title="🌟 SunTool")

# State - SAFE
if 'app_data' not in st.session_state:
    st.session_state.app_data
