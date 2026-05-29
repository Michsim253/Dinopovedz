import streamlit as st
import requests
from PIL import Image
import io

# 1. Nastavenie vzhľadu stránky
st.set_page_config(page_title="DinoPátrač", page_icon="🦕", layout="centered")

# 2. Načítanie kľúča zo Streamlit trezoru
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("Nepodarilo sa načítať API kľúč z trezoru Secrets.")
    API_KEY = None

# 3. Samotný dizajn aplikácie
st.title("🦕 DinoPátrač")
st.write("Vyfoť dinosaura alebo nahraj jeho obrázok a umelá inteligencia ti prezradí, kto to je!")

volba = st.radio("Vyber si spôsob:", ["📸 Použiť foťák", "📁 Nahrať fotku z galérie"])

foto_subor = None
if volba == "📸 Použiť foťák":
    foto_subor = st.camera_input("Zameraj dinosaura a stlač spúšť")
else:
    foto_subor = st.file_uploader("Vyber obrázok dinosaura", type=["jpg", "jpeg", "png"])

# 4. Spracovanie fotografie
if foto_subor is not None and API_KEY is not None:
    image = Image.open(foto_subor)
    st.image(image, caption="Tvoj úlovok", use_container_width=True)
    
    if st.button("🔍 Preskúmať dinosaura"):
        with st.spinner("DinoPátrač komunikuje s Google serverom..."):
            try:
                # Prevedieme obrázok do formátu, ktorý vie prečítať webové rozhranie
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_bytes = img_byte_arr.getvalue()
                
                # Príprava priameho volania pre Google API (univerzálny spôsob pre AQ kľúče)
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
                
                # Špeciálne overenie pre tvoj nový typ kľúča
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                import base64
                base64_image = base64.b64encode(img_bytes).decode('utf-8')
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Identifikuj dinosaura na tomto obrázku. Napíš jeho názov veľkými písmenami, pridaj zaujímavosť, čo jedol a kedy žil. Odpovedaj milo, stručne a v slovenčine."},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ]
                    }]
                }
                
                # Odoslanie požiadavky na Google
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_json = response.json()
                    text_odpovede = res_json['candidates'][0]['content']['parts'][0]['text']
                    st.balloons()
                    st.success("Analýza úspešne dokončená!")
                    st.markdown(f"### 🦖 Výsledok pátrania:\n{text_odpovede}")
                else:
                    st.error(f"Google vrátil chybu (Kód {response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Vyskytla sa neočakávaná chyba: {str(e)}")
