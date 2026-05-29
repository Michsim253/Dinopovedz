import streamlit as st
from PIL import Image
from transformers import pipeline
from gtts import gTTS
import json
import requests
import os

# 1. Nastavenie vzhľadu stránky
st.set_page_config(page_title="DinoPátrač STO", page_icon="🦕", layout="centered")

# 2. Načítanie lokálneho AI modelu
@st.cache_resource
def nacitaj_model():
    return pipeline("image-classification", model="google/vit-base-patch16-224")

with st.spinner("🦕 DinoPátrač prebúdza lokálnu umelú inteligenciu..."):
    try:
        classifier = nacitaj_model()
        model_ready = True
    except Exception as e:
        st.error(f"Nepodarilo sa naštartovať model: {str(e)}")
        model_ready = False

# 3. Načítanie databázy zo súboru dinosaury.json
@st.cache_data
def nacitaj_dino_databazu():
    try:
        if os.path.exists("dinosaury.json"):
            with open("dinosaury.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            st.error("⚠️ Súbor dinosaury.json sa nenašiel! Skontroluj, či si ho vytvorila na GitHube.")
            return {}
    except Exception as e:
        st.error(f"Chyba pri načítaní databázy: {str(e)}")
        return {}

DINO_DATABAZA = nacitaj_dino_databazu()

# 4. Sťahovanie 5 univerzálnych a stabilných zvukov prírody podľa kategórií
def stiahni_zvuk(url, nazov_suboru):
    if not os.path.exists(nazov_suboru):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(nazov_suboru, 'wb') as f:
                    f.write(response.content)
        except Exception:
            pass

stiahni_zvuk("https://actions.google.com/sounds/v1/animals/alligator_hiss.ogg", "dravec.ogg")
stiahni_zvuk("https://actions.google.com/sounds/v1/animals/camel_groan.ogg", "bylinozravec.ogg")
stiahni_zvuk("https://actions.google.com/sounds/v1/animals/hawk_screech.ogg", "raptor.ogg")
stiahni_zvuk("https://actions.google.com/sounds/v1/animals/crow_caw.ogg", "lietajuci.ogg")
stiahni_zvuk("https://actions.google.com/sounds/v1/water/splash.ogg", "vodny.ogg")

# 5. Funkcia na generovanie slovenskej reči
def vygeneruj_pribeh(text, subor_nazov):
    try:
        tts = gTTS(text=text, lang='sk')
        tts.save(subor_nazov)
        st.audio(subor_nazov, format="audio/mp3")
    except Exception as e:
        st.warning("Nepodarilo sa prehrať príbeh sprievodcu.")

# 6. Samotný dizajn aplikácie
st.title("🦕 DinoPátrač STO 🔊")
st.write(f"Aktuálne máme v databáze pripravených **{len(DINO_DATABAZA)} dinosaurov** k okamžitému pátraniu!")

volba = st.radio("Vyber si spôsob:", ["📸 Použiť foťák", "📁 Nahrať fotku z galérie"])

foto_subor = None
if volba == "📸 Použiť foťák":
    foto_subor = st.camera_input("Zameraj objekt")
else:
    foto_subor = st.file_uploader("Vyber obrázok", type=["jpg", "jpeg", "png"])

# 7. Analýza a prepojenie s databázou
if foto_subor is not None and model_ready:
    image = Image.open(foto_subor)
    st.image(image, caption="Tvoj úlovok", use_container_width=True)
    
    if st.button("🔍 Spustiť mega pátranie"):
        with st.spinner("Umelá inteligencia prehľadáva pixely a porovnáva databázu..."):
            try:
                vysledky = classifier(image)
                st.balloons()
                
                # Získame top 3 odhady z modelu pre maximálnu presnosť
                odhady = [res['label'].lower() for res in vysledky[:3]]
                
                najdeny_dino = None
                # Prehľadáme JSON databázu podla kľúčových slov
                for odhad in odhady:
                    for kluc in DINO_DATABAZA:
                        if kluc in odhad or odhad in kluc:
                            najdeny_dino = DINO_DATABAZA[kluc]
                            break
                    if najdeny_dino:
                        break
                
                if najdeny_dino:
                    st.success(f"Našli sme zhodu! Je to: **{najdeny_dino['meno']}**")
                    
                    # 🔊 PREHRÁVANIE ZVUKU PODĽA KATEGÓRIE
                    kat_zvuku = najdeny_dino['zvuk']
                    subor_zvuku = f"{kat_zvuku}.ogg"
                    
                    st.markdown("### 🔊 Vypočuj si autentický zvuk:")
                    if os.path.exists(subor_zvuku):
                        with open(subor_zvuku, 'rb') as f:
                            st.audio(f.read(), format="audio/ogg")
                    else:
                        st.warning("Zvuková kategória sa pripravuje, skús to znova.")
                    
                    # Zobrazenie informácií
                    st.markdown("---")
                    st.markdown(f"🗺️ **Kde žil:** {najdeny_dino['kde_zil']}")
                    st.markdown(f"ℹ️ **Zaujímavosť:** {najdeny_dino['info']}")
                    st.markdown(f"😂 **Vtip na záver:** *{najdeny_dino['vtip']}*")
                    
                    # 🎙️ PRÍBEH V SLOVENČINE
                    text_na_hlas = f"Našli sme zhodu! Je to {najdeny_dino['meno']}. Kde žil? {najdeny_dino['kde_zil']}. Zaujímavosť: {najdeny_dino['info']} A tu je vtip: {najdeny_dino['vtip']}"
                    st.markdown("---")
                    st.markdown("### 🎙️ Vypočuj si príbeh sprievodcu:")
                    vygeneruj_pribeh(text_na_hlas, "pribeh.mp3")
                    
                else:
                    st.warning("Tohto tvora nemám v hlavnej dino-encyklopédii.")
                    st.write(f"Najbližší odhad modelu je: **{vysledky[0]['label']}**")
                    
                    text_na_hlas = f"Tohto tvora bohužiaľ nemám v encyklopédii. Môj odhad je {vysledky[0]['label']}"
                    vygeneruj_pribeh(text_na_hlas, "neznamy.mp3")
                    
            except Exception as e:
                st.error(f"Vyskytla sa chyba pri analýze: {str(e)}")
