import streamlit as str
import json
import requests
import random
from google import genai
from google.genai import types
from PIL import Image

# Nastavenie dizajnu stránky
str.set_page_config(page_title="Dino AI Skener", page_icon="📸", layout="centered")

str.title("📸 Dino AI Skener 100")
str.subheader("Nahraj fotku alebo obrázok a AI spozná, o ktorého dinosaura ide!")

# Bezpečné načítanie API kľúča zo Streamlit Secrets
if "GEMINI_API_KEY" in str.secrets:
    api_key = str.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    str.warning("🔑 V nastaveniach Streamlitu chýba GEMINI_API_KEY. Aplikácia beží v textovom režime.")
    client = None

# Načítanie dát z tvojho GitHub JSONu
URL_DATABAZY = "https://raw.githubusercontent.com/tvoj-github-profil/tvoj-repodinar/main/dinosaury.json" # <--- SEM DOSAĎ SVOJU URL

@str.cache_data
def nacitat_data():
    try:
        odpoved = requests.get(URL_DATABAZY)
        return json.loads(odpoved.text)
    except Exception as e:
        str.error(f"Nepodarilo sa načítať databázu: {e}")
        return {}

data_dino = nacitat_data()

# Načítanie pikošiek (ponechané z minulej verzie pre encyklopédiu)
pikosky = {
    "tyrannosaurus": "T-Rex mal taký dokonalý zrak, že videl lepšie ako dnešný orol, a jeho čuch bol porovnateľný s čuchom stopovacieho psa. Korisť zacítil na kilometre!",
    "triceratops": "Kostený golier Triceratopsa nebol len na obranu. Vedci zistili, že bol pretkaný stovkami ciev, takže ním pravdepodobne reguloval telesnú teplotu ako slon ušami.",
    "velociraptor": "Skutočné Velociraptory mali na perách gombíkovité výrastky (ako dnešné vtáky), čo stopercentne dokazuje, že boli kompletne operené. Lietat však nevedeli.",
    "stegosaurus": "Hoci mal mozog veľký ako vlašský orech, Stegosaurus mal v bokoch pri chvoste akési 'druhé centrum' nervov, ktoré pomáhalo ovládať jeho obrovský chvost plný ostňov.",
    "brontosaurus": "Keď Brontosaurus kráčal, kvôli jeho gigantickej váhe sa zem triasla tak silno, že menšie zvieratá v okolí upadali do paniky už z vibrácií na kilometre ďaleko.",
    "spinosaurus": "Jeho kosti boli extrémne husté a ťažké (na rozdiel od iných dravcov, ktorí ich mali duté). To mu pomáhalo ponárať sa pod vodu a stabilne tam loviť ryby.",
    "ankylosaurus": "Kostené platne Ankylosaura boli tak dokonale vyvinuté, že mal pancierom chránené dokonca aj očné viečka. Keď zavrel oči, bol z neho nepriestrelný trezor."
}
vseobecne_pikosky = [
    "Medzi životom T-Rexa a Stegosaura ubehlo viac času než medzi T-Rexom a nami! T-Rex je nám časovo bližší než Stegosaurus jemu.",
    "Dinosaury technicky nikdy úplne nevyhynuli. Vtáky sú priamymi žijúcimi potomkami malých dravých dinosaurov z jurského obdobia."
]

# --- SEKCOA PRE NAHRÁVANIE OBRÁZKA ---
nahraty_subor = str.file_uploader("Vyber obrázok dinosaura (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if nahraty_subor and client and data_dino:
    # Zobrazenie nahratého obrázka v aplikácii
    obrazok = Image.open(nahraty_subor)
    str.image(obrazok, caption="Tvoj nahratý obrázok", use_container_width=True)
    
    with str.spinner("🤖 AI skenuje obrázok a hľadá zhodu v databáze..."):
        try:
            # Vytvorenie zoznamu kľúčov, ktoré máme v databáze, aby AI vedela, čo hľadáme
            dino_kluce = ", ".join(data_dino.keys())
            
            # Inštrukcia pre AI
            prompt = f"""
            Pozri sa na tento obrázok. Urči, o akého dinosaura alebo pravekého tvora ide. 
            Následne vyber JEDNO JEDINÉ slovo zo zoznamu povolených kľúčov nižšie, ktoré najlepšie prislúcha tomuto tvorovi.
            Ak na obrázku nie je dinosaurus zo zoznamu, alebo si nie si istý, vyber kľúč, ktorý sa mu najviac podobá.
            Odpovedz iba týmto jedným slovom v malých písmenách, ničím iným!
            
            Povolené kľúče: {dino_kluce}
            """
            
            # Volanie Google Gemini AI modelu v2026
            odpoved_ai = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[obrazok, prompt]
            )
            
           # Vyčistenie odpovede od bodiek, medzier a nečistôt
            hladane_meno = odpoved_ai.text.strip().lower().replace(".", "").replace("-", "")
            
            # INTELIGENTNÝ PREKLADAČ: Ak AI odpovie skratkou alebo inak, preložíme to na tvoj kľúč
            prekladac_men = {
                "t-rex": "tyrannosaurus", "trex": "tyrannosaurus", "tyranosaurus": "tyrannosaurus",
                "pterodaktyl": "pterodactyl", "pteranodón": "pteranodon", "mosasaurus": "mosasaurus"
            }
            if hladane_meno in prekladac_men:
                hladane_meno = prekladac_men[hladane_meno]
            
            # Skontrolujeme, či sa slovo od AI aspoň NACHÁDZA v nejakom kľúči
            najdeny_kluc = None
            for kluc in data_dino.keys():
                if kluc in hladane_meno or hladane_meno in kluc:
                    najdeny_kluc = kluc
                    break
            
            # Vyhľadanie v JSON dátach na základe rozhodnutia AI
            if najdeny_kluc:
                dino = data_dino[najdeny_kluc]
                
                str.success(f"🎯 AI Skener úspešne určil tvora: **{dino['meno']}**")
                str.write(f"🌍 **Kde a kedy žil:** {dino['kde_zil']}")
                str.write(f"📖 **Predstavenie:** {dino['info']}")
                
                str.markdown("---")
                str.markdown("### 💡 Vedecká pikoška, o ktorej málokto vie:")
                pikoska_text = pikosky.get(najdeny_kluc, random.choice(vseobecne_pikosky))
                str.info(pikoska_text)
                str.markdown("---")
                
                str.warning(f"😂 **Dino-Vtip:** {dino['vtip']}")
                
                ikony_zvukov = {"dravec": "🦖 ROOOAAARRR!", "bylinozravec": "🦕 CHRUMP-CHMÚÚÚ!", "raptor": "🦅 SSSHRRR-KLIK!", "lietajuci": "🦅 KRAAA-KRAAA!", "vodny": "🌊 GLU-GLU-BLURP!"}
                zvuk_kategoria = dino.get("zvuk", "bylinozravec")
                str.code(f"🔊 Zvuk tvora: {ikony_zvukov.get(zvuk_kategoria, '🦕 ...ticho...')}")
            else:
                str.error(f"❌ AI síce na fotke rozpoznala slovo '{odpoved_ai.text.strip()}', ale to sa žiaľ nezhoduje so žiadnym zo 100 dinosaurov v tvojom JSON súbore. Skús odfotiť iného známeho dinosaura!")
str.markdown("---")
str.caption(f"Skenujeme s podporou databázy {len(data_dino)} dinosaurov.")
