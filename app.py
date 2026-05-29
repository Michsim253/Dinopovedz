import streamlit as str
import json
import requests
import random

# Nastavenie dizajnu stránky
str.set_page_config(page_title="Dino-Vyhľadávač 100", page_icon="🦖", layout="centered")

str.title("🦖 Megalomanský Dino-Vyhľadávač v100")
str.subheader("Prehľadávaj databázu 100 pravekých tvorov s extra pikoškami!")

# Načítanie dát z tvojho GitHub JSONu
URL_DATABAZY = "https://raw.githubusercontent.com/tvoj-github-profil/tvoj-repodinar/main/dinosaury.json" # <--- SEM AKO VŽDY DOSAĎ SVOJU REÁLNU URL

@str.cache_data
def nacitat_data():
    try:
        odpoved = requests.get(URL_DATABAZY)
        return json.loads(odpoved.text)
    except Exception as e:
        str.error(f"Nepodarilo sa načítať databázu: {e}")
        return {}

data_dino = nacitat_data()

# Zoznam fascinujúcich pikošiek podľa kľúčov v tvojom JSONe
pikosky = {
    "tyrannosaurus": "T-Rex mal taký dokonalý zrak, že videl lepšie ako dnešný orol, a jeho čuch bol porovnateľný s čuchom stopovacieho psa. Korisť zacítil na kilometre!",
    "triceratops": "Kostený golier Triceratopsa nebol len na obranu. Vedci zistili, že bol pretkaný stovkami ciev, takže ním pravdepodobne reguloval telesnú teplotu ako slon ušami.",
    "velociraptor": "Skutočné Velociraptory mali na perách gombíkovité výrastky (ako dnešné vtáky), čo stopercentne dokazuje, že boli kompletne operené. Lietat však nevedeli.",
    "stegosaurus": "Hoci mal mozog veľký ako vlašský orech, Stegosaurus mal v bokoch pri chvoste akési 'druhé centrum' nervov, ktoré pomáhalo ovládať jeho obrovský chvost plný ostňov.",
    "brontosaurus": "Keď Brontosaurus kráčal, kvôli jeho gigantickej váhe sa zem triasla tak silno, že menšie zvieratá v okolí upadali do paniky už z vibrácií na kilometre ďaleko.",
    "apatosaurus": "Jeho gigantický chvost tvorilo až 82 stavcov. Keď ním švihol v obrane, špička chvosta prekonala rýchlosť zvuku (cca 1200 km/h) a vytvorila ranu ako z dela.",
    "brachiosaurus": "Brachiosaurus musel mať neskutočne obrovské a silné srdce (vážiace okolo 200 kg), aby dokázalo vytlačiť krv cez dlhý krk až hore do hlavy proti gravitácii.",
    "diplodocus": "Diplodocus mal nezvyčajné zuby, ktoré vyzerali ako kolíky a mal ich len v prednej časti úst. Používal ich ako hrable na bleskové ošklbávanie listov z vetiev.",
    "spinosaurus": "Jeho kosti boli extrémne husté a ťažké (na rozdiel od iných dravcov, ktorí ich mali duté). To mu pomáhalo ponárať sa pod vodu a stabilne tam loviť ryby.",
    "ankylosaurus": "Kostené platne Ankylosaura boli tak dokonale vyvinuté, že mal pancierom chránené dokonca aj očné viečka. Keď zavrel oči, bol z neho nepriestrelný trezor.",
    "pterodactyl": "Mláďatá Pterodaktylov dokázali podľa najnovších výskumov lietať takmer okamžite po vyliahnutí z vajíčka, nepotrebovali žiadne lekcie lietania od rodičov.",
    "pteranodon": "Napriek obriemu rozpätiu krídel vážil Pteranodon len okolo 25 až 30 kilogramov. Jeho kosti boli totiž tenké ako papier a duté, naplnené vzduchom.",
    "mosasaurus": "Mosasaurus mal na podnebí úst druhý rad zubov! Akonáhle korisť prehltol, tieto zadné zuby sa do nej zasekli a nepustili ju von, fungovali ako spätný háčik.",
    "parasaurolophus": "Počítačové simulácie ukázali, že vzduch prúdiaci cez jeho dutý hrebeň vytváral taký ultranízky infrazvuk, že ním vedel komunikovať cez celé husté pralesy.",
    "allosaurus": "Allosaurus mal prekvapivo slabý stisk čelustí (slabší ako dnešný lev), ale jeho lebka fungovala ako sekera. Útočil tak, že hornou čelusťou zhora zasekával korisť.",
    "carnotaurus": "Jeho oči smerovali mierne dopredu, čo znamená, že Carnotaurus mal stereoskopické videnie – dokázal dokonale odhadnúť vzdialenosť koristi pred útokom.",
    "iguanodon": "Keď v 19. storočí našli prvý palcový bodec Iguanodona, vedci si najprv mysleli, že patrí na nos a nakreslili ho ako obrieho nosorožca. Až neskôr zistili pravdu!",
    "dilophosaurus": "V skutočnosti meral cez 6 metrov a vážil pol tony. Bol to najväčší dravec svojej éry a žiadny jed nepľul – na usmrtenie koristi mu stačili mohutné čeluste.",
    "pachycephalosaurus": "Jeho kostená helma na hlave bola tvorená špeciálnou hubovitou kosťou, ktorá pri nárazoch fungovala ako dokonalý tlmič nárazov, aby nedostal otras mozgu.",
    "archaeopteryx": "Jeho perie malo čiernu farbu. Zistili to vedci pomocou elektrónových mikroskopov, v ktorých objavili bunky obsahujúce tmavý pigment (melanín).",
    "giganotosaurus": "Hoci bol dlhší ako T-Rex, jeho mozog bol o polovicu menší a mal tvar dlhého banánu. Väčšinu mozgu zaberalo centrum pre spracovanie čuchu.",
    "baryonyx": "Analýza jeho zubov ukázala, že okrem rýb nepohrdol ani suchozemskou korisťou. V jeho žalúdku sa našli nestrávené kosti mladého Iguanodona.",
    "therizinosaurus": "Jeho gigantické metrové pazúry boli na konci sploštené. Používal ich nielen na obranu a konáre, ale pravdepodobne nimi rozhrabával aj obrie praveké termitiská.",
    "oviraptor": "Oviraptor mal na hlave hrebeň, ktorý pravdepodobne slúžil na to, aby sa jednotliví členovia skupiny spoznali v hustej vegetácii alebo na dvorenie partnerkám.",
    "deinonychus": "Objav Deinonycha v roku 1964 spôsobil revolúciu. Dovtedy si ľudia mysleli, že dinosaury sú len lenivé studenokrvné jaštery. Deinonychus ukázal, že boli bleskurýchle a teplokrvné.",
    "troodon": "Mal najväčší pomer mozgu k telu zo všetkých dinosaurov. Keby nevyhynuli, vedci špekulujú, že by sa z nich vyvinuli inteligentné bytosti chodiace po dvoch.",
    "quetzalcoatlus": "Tento gigant nelietal mávaním krídel ako vták, ale využíval teplé vzdušné prúdy ako obrovský klzák. Na zemi behal po štyroch rýchlosťou až 30 km/h.",
    "argentinosaurus": "Aby takýto 90-tonový gigant prežil, musel denne zožrať odhadom 500 až 1000 kilogramov rastlín. Jeho trávenie produkovalo obrovské množstvo metánu.",
    "cryolophosaurus": "Jeho zamrznutá fosília bola objavená v nadmorskej výške až 4 000 metrov nad morom na hore Kirkpatrick v Antarktíde, kde ju museli vedci pracne vysekávať zo skaly.",
    "gallimimus": "Jeho oči boli umiestnené na bokoch hlavy, čo mu dávalo takmer 360-stupňový prehľad o okolí. Vďaka tomu ho žiadny dravý raptor nedokázal prekvapiť zozadu.",
    "gigantoraptor": "Tento obrí operenec mal mohutný zobák úplne bez zubov. Vedci sa dodnes sporia, či ním lúskal obrie orechy, alebo ním trhal mäso malých dinosaurov."
}

# Univerzálny zoznam všeobecných pikošiek, ak hľadaný dino nemá špecifickú
vseobecne_pikosky = [
    "Medzi životom T-Rexa a Stegosaura ubehlo viac času než medzi T-Rexom a nami! T-Rex je nám časovo bližší než Stegosaurus jemu.",
    "Dinosaury technicky nikdy úplne nevyhynuli. Vtáky sú priamymi žijúcimi potomkami malých dravých dinosaurov z jurského obdobia.",
    "Väčšina dinosaurov sa dožívala prekvapivo nízkeho veku. T-Rex rástol extrémne rýchlo a máloktorý jedinec sa dožil viac ako 30 rokov.",
    "Praveká Zem sa točila rýchlejšie! V ére prvých dinosaurov mal rok až 385 dní a deň trval len niečo vyše 22 hodín."
]

# Vyhľadávacie okno
hladane_meno = str.text_input("Zadaj názov dinosaura (napr. T-Rex, Triceratops, Argentinosaurus...):").strip().lower()

if hladane_meno:
    # Premenovanie populárnych výrazov na kľúče
    synonyma = {"t-rex": "tyrannosaurus", "rex": "tyrannosaurus", "tyranosaurus": "tyrannosaurus"}
    if hladane_meno in synonyma:
        hladane_meno = synonyma[hladane_meno]
    
    # Vyhľadanie v JSON dátach
    if hladane_meno in data_dino:
        dino = data_dino[hladane_meno]
        
        str.success(f"📌 Nájdený tvor: **{dino['meno']}**")
        str.write(f"🌍 **Kde a kedy žil:** {dino['kde_zil']}")
        str.write(f"📖 **Predstavenie:** {dino['info']}")
        
        # Sekcia pre Extra Vedeckú pikošku (Možnosť B)
        str.markdown("---")
        str.markdown("### 💡 Vedecká pikoška, o ktorej málokto vie:")
        # Ak máme pre neho konkrétnu pikošku, daj ju, inak vyber náhodnú všeobecnú
        pikoska_text = pikosky.get(hladane_meno, random.choice(vseobecne_pikosky))
        str.info(pikoska_text)
        str.markdown("---")
        
        # Zábavný vtip a zvuk na záver
        str.warning(f"😂 **Dino-Vtip:** {dino['vtip']}")
        
        ikony_zvukov = {"dravec": "🦖 ROOOAAARRR!", "bylinozravec": "🦕 CHRUMP-CHMÚÚÚ!", "raptor": "🦅 SSSHRRR-KLIK!", "lietajuci": "🦅 KRAAA-KRAAA!", "vodny": "🌊 GLU-GLU-BLURP!"}
        zvuk_kategoria = dino.get("zvuk", "bylinozravec")
        str.code(f"🔊 Zvuk tvora: {ikony_zvukov.get(zvuk_kategoria, '🦕 ...ticho...')}")
        
    else:
        str.error("❌ Takého dinosaura v našej stovke nemáme. Skontroluj preklepy alebo skús iného!")

# Pätička aplikácie
str.markdown("---")
if data_dino:
    str.caption(f"Aktuálne máme v databáze pripravených **{len(data_dino)} dinosaurov** k okamžitému pátraniu!")
