import streamlit as st
import requests

st.set_page_config(page_title="Demand Prediction", layout="wide")

st.title(" Demand Prediction Service")

BACKEND_URL = "http://localhost:8000"

st.subheader("Backend status")

try:
    r = requests.get(f"{BACKEND_URL}/health")
    if r.status_code == 200:
        st.success("Backend OK")
    else:
        st.error("Backend error")
except Exception as e:
    st.error("Cannot connect to backend")
