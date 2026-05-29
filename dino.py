import streamlit as st

st.set_page_config(page_title="DinoPátrač", page_icon="🦕")

st.title("🦕 DinoPátrač")
st.write("Ak vidíš tento text, tvoj Streamlit a GitHub sú prepojené SPRÁVNE! 🎉")

if st.button("Spustiť balóniky"):
    st.balloons()
    st.success("Funguje to!")
