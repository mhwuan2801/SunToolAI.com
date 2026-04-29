import streamlit as st
import random

st.markdown("""
<style>
.btn {height:60px;border-radius:20px;font-size:1.2rem;font-weight:bold;}
.ai {background:linear-gradient(135deg,#ff6b6b,#feca57);color:white;padding:2rem;border-radius:25px;text-align:center;}
</style>
""",unsafe_allow_html=True)

# Data
if 'data' not in st.session_state:
    st.session_state.data = {'user':'','balance':1000000,'wins':0,'games':0,'history':[]}

# Login
if not st.session_state.data['user']:
    st.header("🌟 **SUNTOOL**")
    col1,col
