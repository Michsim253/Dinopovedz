import streamlit as st
import requests
from PIL import Image
import io

# 1. Nastavenie vzhľadu stránky
st.set_page_config(page_title="DinoPátrač", page_icon="🦕", layout="centered")

# 2. Načítanie Hugging Face tokenu zo Streamlit trezoru
if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
else:
    st.error("⚠️ V trezore Secrets chýba kľúč s názvom HF_TOKEN. Skontroluj nastavenia v Streamlite.")
    HF_TOKEN = None

# API adresa pre vizuálny model - v2 verzia kvôli stabilite pripojenia
API_URL = "https://api-inference.huggingface.co/v1/models/Salesforce/blip-image-captioning-large"

# Definícia hlavičiek (headers) - tu bola chyba, teraz je to opravené!
if HF_TOKEN:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
else:
    headers = {}

# 3. Samotný dizajn aplikácie
st.title("🦕 DinoPátrač")
st.write("Vyfoť dinosaura alebo nahraj jeho obrázok a umelá inteligencia ti prezradí, kto to je!")

volba = st.radio("Vyber si spôsob:", ["📸 Použiť foťák", "📁 Nahrať fotku z galérie"])

foto_subor = None
if volba == "📸 Použiť foťák":
    foto_subor = st.camera_input("Zameraj dinosaura a stlač spúšť")
else:
    foto_subor = st.file_uploader("Vyber obrázok dinosaura", type=["jpg", "jpeg", "png"])

# 4. Spracovanie fotografie po kliknutí na tlačidlo
if foto_subor is not None and HF_TOKEN is not None:
    image = Image.open(foto_subor)
    st.image(image, caption="Tvoj úlovok", use_container_width=True)
    
    if st.button("🔍 Preskúmať dinosaura"):
        with st.spinner("DinoPátrač analyzuje tvoj obrázok cez Hugging Face..."):
            try:
                # Prevedieme obrázok do bytov pre odoslanie
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_bytes = img_byte_arr.getvalue()
                
                # Odoslanie fotky na Hugging Face server
                response = requests.post(API_URL, headers=headers, data=img_bytes)
                
                if response.status_code == 200:
                    vysledok = response.json()
                    # Ošetrenie výstupu z v2 API rozhrania
                    if isinstance(vysledok, list) and len(vysledok) > 0:
                        popis_en = vysledok[0].get('generated_text', 'Nepodarilo sa vygenerovať popis.')
                    else:
                        popis_en = str(vysledok)
                    
                    st.balloons()
                    st.success("Analýza úspešne dokončená!")
                    st.markdown("### 🦖 Výsledok pátrania:")
                    st.write(f"**Umelá inteligencia na obrázku vidí:** {popis_en}")
                    st.info("💡 Tip: Ak je na fotke známy dinosaurus (napr. T-Rex), model vypíše priamo jeho názov!")
                else:
                    st.error(f"Hugging Face hlási chybu ({response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Vyskytla sa chyba: {str(e)}")
