import streamlit as st
from PIL import Image
from transformers import pipeline

# 1. Nastavenie vzhľadu stránky
st.set_page_config(page_title="DinoPátrač", page_icon="🦕", layout="centered")

# 2. Načítanie lokálneho AI modelu do pamäte aplikácie (zabezpečíme, aby sa nenačítaval dokola)
@st.cache_resource
def nacitaj_model():
    # Použijeme ultra-ľahký a rýchly model MobileNet, ktorý nepotrebuje silný počítač
    return pipeline("image-classification", model="google/vit-base-patch16-224")

with st.spinner("🦕 DinoPátrač prebúdza lokálnu umelú inteligenciu... (Prvé spustenie môže trvať minútku)"):
    try:
        classifier = nacitaj_model()
        model_ready = True
    except Exception as e:
        st.error(f"Nepodarilo sa naštartovať lokálny model: {str(e)}")
        model_ready = False

# 3. Samotný dizajn aplikácie
st.title("🦕 DinoPátrač (Lokálna verzia)")
st.write("Táto verzia beží priamo v aplikácii a nepotrebuje žiadne API kľúče ani internetové pripojenie!")

volba = st.radio("Vyber si spôsob:", ["📸 Použiť foťák", "📁 Nahrať fotku z galérie"])

foto_subor = None
if volba == "📸 Použiť foťák":
    foto_subor = st.camera_input("Zameraj objekt a stlač spúšť")
else:
    foto_subor = st.file_uploader("Vyber obrázok", type=["jpg", "jpeg", "png"])

# 4. Lokálna analýza fotografie
if foto_subor is not None and model_ready:
    image = Image.open(foto_subor)
    st.image(image, caption="Tvoj úlovok", use_container_width=True)
    
    if st.button("🔍 Preskúmať lokálne"):
        with st.spinner("Umelá inteligencia analyzuje pixely obrázka..."):
            try:
                # Spustenie lokálnej klasifikácie
                vysledky = classifier(image)
                
                st.balloons()
                st.success("Analýza úspešne dokončená!")
                st.markdown("### 🦖 Čo na obrázku vidí lokálna AI:")
                
                # Vypíšeme top 3 najpravdepodobnejšie veci, ktoré model našiel
                for i, res in enumerate(vysledky[:3]):
                    label = res['label']
                    pravdepodobnost = round(res['score'] * 100, 1)
                    st.write(f"{i+1}. **{label}** (Istota: {pravdepodobnost}%)")
                    
            except Exception as e:
                st.error(f"Vyskytla sa chyba pri analýze: {str(e)}")
