# 2. Načítanie Hugging Face tokenu zo Streamlit trezoru
if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
else:
    st.error("⚠️ V trezore Secrets chýba kľúč s názvom HF_TOKEN. Skontroluj nastavenia v Streamlite.")
    HF_TOKEN = None
