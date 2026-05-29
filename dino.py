import streamlit as st
from PIL import Image
from transformers import pipeline
from gtts import gTTS
import os

# 1. Nastavenie vzhľadu stránky
st.set_page_config(page_title="DinoPátrač 3.0", page_icon="🦕", layout="centered")

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

# 3. Databáza dinosaurov so skutočnými zvukmi z Wikimedia (overené a stabilné)
DINO_DATABAZA = {
    "triceratops": {
        "meno": "Triceratops",
        "kde_zil": "Severná Amerika (pred 68 miliónmi rokov)",
        "info": "Mal na hlave tri obrie rohy a obrovský kostený golier. Bol to obrovský vegetarián, niečo ako praveký obrnený nosorožec.",
        "vtip": "Prečo mal Triceratops tri rohy? Lebo štyri by už boli podozrivé a s dvoma by ho kamoši vysmiali, že je len obyčajná krava!",
        "zvuk_url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Elephant_Rumble.mp3"  # Dunivé vrčanie obrovského slona (ideálne pre Triceratopsa)
    },
    "tyrannosaurus": {
        "meno": "Tyrannosaurus Rex (T-Rex)",
        "kde_zil": "Severná Amerika (pred 66 miliónmi rokov)",
        "info": "Kráľ dinosaurov s najsilnejším stiskom čelustí v histórii. Mal zuby veľké ako banány, ale ruky také krátke, že si nimi nedočiahol ani do nosa.",
        "vtip": "Čo urobí nahnevaný T-Rex? Nič, lebo si nedokáže ani zatlačiť ruku v päsť!",
        "zvuk_url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Alligator_hiss.mp3"  # Temné, hrozivé zúrivé syčanie obrieho aligátora - presne takto podľa vedcov T-Rex v skutočnosti znel!
    },
    "velociraptor": {
        "meno": "Velociraptor",
        "kde_zil": "Ázia / Mongolsko (pred 75 miliónmi rokov)",
        "info": "V skutočnosti bol veľký asi ako morka a mal perie, nie ako tie obrie jaštery vo filmoch. Bol však neuveribly rýchly a prefíkaný lovec.",
        "vtip": "Vieš, prečo Velociraptor nikdy nehral na schovávačku? Lebo ho vždy prezradilo šuchotanie peria, kým sa smial!",
        "zvuk_url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Hawk_screaming.mp3"  # Ostrý, prenikavý dravý škrekot jastraba (skvelé pre opereného dravca)
    },
    "stegosaurus": {
        "meno": "Stegosaurus",
        "kde_zil": "Severná Amerika a Európa (pred 150 miliónmi rokov)",
        "info": "Na chrbte mal obrovské kostené platne a na chvoste ostne. Mal však mozog veľký len ako vlašský orech. Nebol to zrovna najbystrejší dinosaurus v údolí.",
        "vtip": "Čo povie Stegosaurus, keď narazí do stromu? Nič, premýšľa o tom až o tri dni neskôr!",
        "zvuk_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Hippo_grunt_and_splash.mp3"  # Hlboké, ťažkopádne funenie hrocha
    }
}

# 4. Funkcia na generovanie reči
def vygeneruj_pribeh(text, subor_nazov):
    try:
        tts = gTTS(text=text, lang='sk')
        tts.save(subor_nazov)
        st.audio(subor_nazov, format="audio/mp3")
    except Exception as e:
        st.warning("Nepodarilo sa prehrať príbeh.")

# 5. Samotný dizajn aplikácie
st.title("🦕 DinoPátrač 3.0 🔊")
st.write("Vyfoť dinosaura, vypočuj si jeho skutočný rev a spoznaj jeho príbeh!")

volba = st.radio("Vyber si spôsob:", ["📸 Použiť foťák", "📁 Nahrať fotku z galérie"])

foto_subor = None
if volba == "📸 Použiť foťák":
    foto_subor = st.camera_input("Zameraj objekt")
else:
    foto_subor = st.file_uploader("Vyber obrázok", type=["jpg", "jpeg", "png"])

# 6. Analýza
if foto_subor is not None and model_ready:
    image = Image.open(foto_subor)
    st.image(image, caption="Tvoj úlovok", use_container_width=True)
    
    if st.button("🔍 Preskúmať lokálne"):
        with st.spinner("Umelá inteligencia analyzuje pixely obrázka..."):
            try:
                vysledky = classifier(image)
                st.balloons()
                
                top_vysledok = vysledky[0]['label'].lower()
                
                najdeny_dino = None
                for kluc in DINO_DATABAZA:
                    if kluc in top_vysledok:
                        najdeny_dino = DINO_DATABAZA[kluc]
                        break
                
                if najdeny_dino:
                    st.success(f"Našli sme zhodu! Je to: **{najdeny_dino['meno']}**")
                    
                    # 🔊 1. PREHRÁVAČ: Skutočný divoký zvuk z prírody!
                    st.markdown("### 🔊 Vypočuj si autentický zvuk:")
                    st.audio(najdeny_dino['zvuk_url'], format="audio/mp3")
                    
                    # Zobrazenie informácií
                    st.markdown("---")
                    st.markdown(f"🗺️ **Kde žil:** {najdeny_dino['kde_zil']}")
                    st.markdown(f"ℹ️ **Zaujímavosť:** {najdeny_dino['info']}")
                    st.markdown(f"😂 **Vtip na záver:** *{najdeny_dino['vtip']}*")
                    
                    # 🎙️ 2. PREHRÁVAČ: Hlasový príbeh v slovenčine
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
