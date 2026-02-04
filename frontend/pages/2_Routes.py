import streamlit as st
import requests

st.title("Routes")

BACKEND_URL = "http://localhost:8000"

if st.button("Load routes"):
    r = requests.get(f"{BACKEND_URL}/routes")
    if r.status_code == 200:
        st.json(r.json())
    else:
        st.error("Error loading routes")
