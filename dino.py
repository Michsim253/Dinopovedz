import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Nastavenie vzhľadu stránky
st.set_page_config(page_title="DinoPátrač", page_icon="🦕", layout="centered")

# 2. Načítanie kľúča zo Streamlit trezoru a nastavenie do systému
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    # Tento riadok povie počítaču, kde presne má kľúč hľadať
    os.environ["GEMINI_API_KEY"] = API_KEY
    genai.configure(api_key=API_KEY)
    
    # Použijeme najstabilnejší model, ktorý podporuje nové kľúče
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Chyba pri načítaní trezoru.")

# 3. Samotný dizajn aplikácie
st.title("🦕 DinoPátrač")
st.write("Vyfoť dinosaura alebo nahraj jeho obrázok a umelá inteligencia ti prezradí, kto to je!")

# Výber medzi foťákom a nahrávaním súboru
volba = st.radio("Vyber si spôsob:", ["📸 Použiť foťák", "📁 Nahrať fotku z galérie"])

foto_subor = None
if volba == "📸 Použiť foťák":
    foto_subor = st.camera_input("Zameraj dinosaura a stlač spúšť")
else:
    foto_subor = st.file_uploader("Vyber obrázok dinosaura", type=["jpg", "jpeg", "png"])

# 4. Spracovanie fotografie po kliknutí na tlačidlo
if foto_subor is not None:
    image = Image.open(foto_subor)
    st.image(image, caption="Tvoj úlovok", use_container_width=True)
    
    if st.button("🔍 Preskúmať dinosaura"):
        with st.spinner("DinoPátrač analyzuje tvoj obrázok..."):
            try:
                # Otázka pre AI v slovenčine
                otazka = (
                    "Identifikuj dinosaura na tomto obrázku. "
                    "Napíš jeho názov veľkými písmenami, pridaj zaujímavosť, "
                    "čo jedol a kedy žil. Odpovedaj milo, stručne a v slovenčine."
                )
                
                # Odoslanie fotky do Gemini
                odpoved = model.generate_content([otazka, image])
                
                # Zobrazenie výsledku
                st.balloons()
                st.success("Analýza úspešne dokončená!")
                st.markdown(f"### 🦖 Výsledok pátrania:\n{odpoved.text}")
                
            except Exception as e:
                # Ak to zlyhá, vypíšeme presnú chybu z Google serveru, aby sme vedeli, čo presne sa deje
                st.error(f"Google hlási chybu: {str(e)}")
