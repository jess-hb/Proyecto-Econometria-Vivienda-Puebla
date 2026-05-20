"""
scrapiiiiiing
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import pandas as pd
import re
import time
import random
import os
import base64



USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
]



PAGINA_INICIO = 6       
PAGINA_FIN    = 10       

TIPOS        = ["departamentos", "casas"]
ARCHIVO_CSV  = "propiedades_puebla.csv"
ARCHIVO_URLS = "urls_visitadas.txt"


def limpiar_precio(texto):
    if not texto:
        return None
    match = re.search(r"[\d,]+", texto.replace(".", ""))
    if match:
        return int(match.group().replace(",", ""))
    return None

def limpiar_numero(texto):
    if not texto:
        return None
    match = re.search(r"\d+\.?\d*", texto)
    if match:
        return float(match.group())
    return None

def tiene_amenidad(texto, palabras):
    texto_lower = texto.lower()
    return 1 if any(p in texto_lower for p in palabras) else 0

def extraer_coordenadas(contenido):
    """Coordenadas guardadas en base64 en variables JS."""
    try:
        lat_b64 = re.search(r'mapLatOf\s*=\s*"([^"]+)"', contenido)
        lng_b64 = re.search(r'mapLngOf\s*=\s*"([^"]+)"', contenido)
        if lat_b64 and lng_b64:
            lat = float(base64.b64decode(lat_b64.group(1)).decode("utf-8"))
            lon = float(base64.b64decode(lng_b64.group(1)).decode("utf-8"))
            return lat, lon
    except Exception:
        pass
    return None, None

def extraer_direccion(contenido):
    """Dirección extraída del <title> de la página."""
    try:
        match = re.search(r"<title>(.*?)</title>", contenido, re.IGNORECASE)
        if match:
            titulo = match.group(1)
            titulo = re.sub(r"\s*-\s*Inmuebles24.*$", "", titulo).strip()
            titulo = re.sub(r"^.*?\ben\s+(?:Venta|Renta)\s+en\s+", "", titulo, flags=re.IGNORECASE).strip()
            titulo = re.sub(r"\.\s*Provincia de Puebla.*$", "", titulo).strip()
            return titulo
    except Exception:
        pass
    return None

def extraer_feature_json(contenido, feature_id):
    """
    Extrae el valor de un featureId del JSON embebido en la página.
    Ejemplo: "CFT5":{"featureId":"CFT5","label":"antigüedad","value":"4"}
    """
    try:
        patron = rf'"{feature_id}"\s*:\s*\{{[^}}]*"value"\s*:\s*"([^"]+)"'
        match = re.search(patron, contenido)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None



def obtener_urls(page_listado, tipo, pagina):
    if pagina == 1:
        url = f"https://www.inmuebles24.com/{tipo}-en-venta-en-puebla.html"
    else:
        url = f"https://www.inmuebles24.com/{tipo}-en-venta-en-puebla-pagina-{pagina}.html"

    print(f"\n  Abriendo: {url}")
    try:
        page_listado.goto(url, timeout=60000)
        time.sleep(25)
        page_listado.wait_for_selector("[data-qa='posting PROPERTY']", timeout=60000)
    except PlaywrightTimeout:
        print(f"  ⚠ Timeout en página {pagina}. ¿Cloudflare? Espera y vuelve a correr.")
        return []

    time.sleep(random.uniform(3, 5))

    tarjetas = page_listado.query_selector_all("[data-qa='posting PROPERTY']")
    resultados = []
    urls_vistas = set()

    for t in tarjetas:
        e = t.query_selector("a")
        if not e:
            continue
        href = e.get_attribute("href")
        if not href:
            continue
        if not href.startswith("http"):
            href = "https://www.inmuebles24.com" + href
        if href in urls_vistas:
            continue
        urls_vistas.add(href)

        try:
            precio_txt = t.query_selector("[data-qa='POSTING_CARD_PRICE']").inner_text()
            precio = limpiar_precio(precio_txt)
        except Exception:
            precio = None

        resultados.append({"url": href, "precio_mxn": precio})

    print(f"  ✓ {len(resultados)} propiedades encontradas")
    return resultados


def extraer_detalle(page_detalle, url, precio_listado=None, tipo=""):
    try:
        page_detalle.goto(url, timeout=30000)
        time.sleep(random.uniform(3, 5))
        contenido = page_detalle.content()


        try:
            precio_txt = page_detalle.query_selector("[data-qa='POSTING_CARD_PRICE']").inner_text()
            precio = limpiar_precio(precio_txt) or precio_listado
        except Exception:
            precio = precio_listado


        m2 = None
        try:
            features = page_detalle.query_selector_all("li[data-qa='POSTING_CARD_FEATURES-feature']")
            for f in features:
                t = f.inner_text().lower()
                if "m²" in t or "m2" in t:
                    m2 = limpiar_numero(t)
                    break
        except Exception:
            pass
        if m2 is None:
            match = re.search(r"(\d+)\s*m[²2]", contenido)
            if match:
                m2 = float(match.group(1))


        recamaras = None
        match = re.search(r"(\d+)\s*rec[aá]mara", contenido, re.IGNORECASE)
        if match:
            recamaras = int(match.group(1))


        banos = None
        val = extraer_feature_json(contenido, "CFT2")
        if val:
            banos = int(val)
        else:
            match = re.search(r"(\d+)\s*ba[ñn]o", contenido, re.IGNORECASE)
            if match:
                banos = int(match.group(1))



        medios_banos = None
        val = extraer_feature_json(contenido, "CFT3")
        if val:
            medios_banos = int(val)


        estacionamientos = None
        match = re.search(r"(\d+)\s*estacionamiento", contenido, re.IGNORECASE)
        if match:
            estacionamientos = int(match.group(1))

      
        antiguedad = None
        val = extraer_feature_json(contenido, "CFT5")
        if val and val.isdigit():
            antiguedad = int(val)
        else:
            # Fallback: meta tag "Antigüedad 4 años"
            match = re.search(r"Antig[üu]edad\s+(\d+)\s*a[ñn]os?", contenido, re.IGNORECASE)
            if match:
                antiguedad = int(match.group(1))

       
        if "departamento" in tipo.lower():
            pisos = 1
        elif "casa" in tipo.lower():
            pisos = 2
        else:
            pisos = None

       
        direccion = extraer_direccion(contenido)

       
        lat, lon = extraer_coordenadas(contenido)

       
        roof_garden = tiene_amenidad(contenido, ["roof garden", "rooftop", "azotea privada", "terraza en azotea"])
        alberca     = tiene_amenidad(contenido, ["alberca", "piscina", "pool"])

        return {
            "precio_mxn"      : precio,
            "m2"              : m2,
            "recamaras"       : recamaras,
            "banos"           : banos,
            "medios_banos"    : medios_banos,
            "estacionamientos": estacionamientos,
            "antiguedad_anos" : antiguedad,
            "pisos"           : pisos,
            "direccion"       : direccion,
            "latitud"         : lat,
            "longitud"        : lon,
            "roof_garden"     : roof_garden,
            "alberca"         : alberca,
            "url"             : url,
        }

    except Exception as e:
        print(f"  ✗ Error en {url[:60]}: {e}")
        return None


if __name__ == "__main__":

    print(f"Corriendo páginas {PAGINA_INICIO} a {PAGINA_FIN} de {TIPOS}")

    urls_visitadas = set()
    if os.path.exists(ARCHIVO_URLS):
        with open(ARCHIVO_URLS) as f:
            urls_visitadas = set(f.read().splitlines())

    todos_los_datos = []
    if os.path.exists(ARCHIVO_CSV):
        df_prev = pd.read_csv(ARCHIVO_CSV)
        todos_los_datos = df_prev.to_dict("records")
        print(f"Retomando desde {len(todos_los_datos)} registros previos.")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--lang=es-MX",
            ]
        )

        context = browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1366, "height": 768},
            locale="es-MX",
            timezone_id="America/Mexico_City",
        )

        page_listado = context.new_page()
        page_listado.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        page_detalle = context.new_page()
        page_detalle.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        try:
            for tipo in TIPOS:
                print(f"\n{'='*45}")
                print(f"TIPO: {tipo.upper()} | Páginas {PAGINA_INICIO}-{PAGINA_FIN}")
                print(f"{'='*45}")

                for pagina in range(PAGINA_INICIO, PAGINA_FIN + 1):

                    if pagina > PAGINA_INICIO:
                        espera = random.uniform(15, 25)
                        print(f"Esperando {espera:.1f}s...")
                        time.sleep(espera)

                    items = obtener_urls(page_listado, tipo, pagina)

                    for item in items:
                        url            = item["url"]
                        precio_listado = item["precio_mxn"]

                        if url in urls_visitadas:
                            print(f"  → Ya visitada, saltando.")
                            continue

                        print(f"  Extrayendo: {url[:65]}...")
                        datos = extraer_detalle(page_detalle, url, precio_listado, tipo)

                        if datos:
                            datos["tipo"] = tipo
                            todos_los_datos.append(datos)
                            precio_fmt = f"${datos['precio_mxn']:,}" if datos['precio_mxn'] else "N/A"
                            print(
                                f"     💰 {precio_fmt} | "
                                f"📐 {datos['m2']}m² | "
                                f"🛏 {datos['recamaras']} rec | "
                                f"🚿 {datos['banos']} baños | "
                                f"🚽 {datos['medios_banos']} med | "
                                f"🏗 {datos['antiguedad_anos']} años | "
                                f"🏢 {datos['pisos']} pisos | "
                                f"🏊 alberca={datos['alberca']} | "
                                f"🌿 roof={datos['roof_garden']}"
                            )

                        urls_visitadas.add(url)
                        with open(ARCHIVO_URLS, "a") as f:
                            f.write(url + "\n")

                        if len(todos_los_datos) % 10 == 0 and todos_los_datos:
                            pd.DataFrame(todos_los_datos).to_csv(
                                ARCHIVO_CSV, index=False, encoding="utf-8-sig"
                            )
                            print(f"  💾 Guardado: {len(todos_los_datos)} propiedades")

                        time.sleep(random.uniform(2, 4))

        except KeyboardInterrupt:
            print("\nInterrumpido. Guardando datos...")

        finally:
            browser.close()

            if todos_los_datos:
                df = pd.DataFrame(todos_los_datos)
                df = df.drop_duplicates(subset=["url"])
                df = df.drop_duplicates(subset=["precio_mxn", "m2", "recamaras", "direccion"])
                df.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8-sig")

                print(f"\n{'='*45}")
                print("SCRAPING TERMINADO")
                print(f"{'='*45}")
                print(f"Total propiedades : {len(df)}")
                print(f"Con coordenadas   : {df['latitud'].notna().sum()}")
                print(f"Con dirección     : {df['direccion'].notna().sum()}")
                print(f"Con antigüedad    : {df['antiguedad_anos'].notna().sum()}")
                print(f"Con medios baños  : {df['medios_banos'].notna().sum()}")
                print(f"Con alberca       : {df['alberca'].sum()}")
                print(f"Con roof garden   : {df['roof_garden'].sum()}")
                print(f"\nArchivo: {ARCHIVO_CSV}")
                print(df[["tipo","precio_mxn","m2","recamaras","banos","medios_banos","antiguedad_anos","pisos","alberca","roof_garden"]].head(10))
            else:
                print("No se obtuvieron datos.")
