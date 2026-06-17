import streamlit as st
import json

@st.cache_data(show_spinner=False)
def load_payload(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return (
            data.get("trends", []),
            data.get("metrics", {}),
            data.get("model", {}),
            data.get("generated_at", ""),
        )

    return data, {}, {}, ""