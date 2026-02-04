import streamlit as st
import requests

st.title("Zones")

BACKEND_URL = "http://localhost:8000"

if st.button("Load zones"):
    r = requests.get(f"{BACKEND_URL}/zones")
    if r.status_code == 200:
        st.json(r.json())
    else:
        st.error("Error loading zones")
