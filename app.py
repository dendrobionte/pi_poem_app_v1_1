import streamlit as st
import re
from collections import OrderedDict

st.set_page_config(page_title="Generador Poético con Pi", layout="wide")

st.title("📐 Generador Poético con los decimales de π")
st.markdown("Transforma cualquier texto en un poema único utilizando los decimales de π como clave matemática y genera tankas japoneses.")

# Limpia y normaliza el texto
def limpiar_texto(texto):
    palabras = re.findall(r"\b[a-záéíóúüñ]+\b", texto.lower())
    palabras_unicas = list(OrderedDict.fromkeys(palabras))
    return palabras_unicas

# Carga los decimales de pi
@st.cache_data
def cargar_decimales_pi():
    with open("pi_decimals.txt", "r") as f:
        return f.read().strip().replace("\n", "")

def generar_versos(palabras, longitud=7):
    return [palabras[i:i+longitud] for i in range(0, len(palabras), longitud) if len(palabras[i:i+longitud]) == longitud]

def to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syms[i]
            n -= val[i]
        i += 1
    return roman_num

def transformar_en_tanka(verso, indice):
    if len(verso) != 7:
        return None
    numero_romano = to_roman(indice)
    return f"{numero_romano}\n{verso[0]}\n{verso[1]} {verso[2]}\n{verso[3]}\n{verso[4]} {verso[5]}\n{verso[6]}"

archivo_subido = st.file_uploader("📄 Sube un archivo .txt", type="txt")

if archivo_subido:
    texto = archivo_subido.read().decode("utf-8")
    palabras = limpiar_texto(texto)
    total = len(palabras)
    st.success(f"✔️ El texto contiene {total} palabras únicas.")

    pi = cargar_decimales_pi()
    usados = set()
    resultado = []
    i = 0

    while len(usados) < total and i + 4 <= len(pi):
        bloque = int(pi[i:i+4])
        if 1 <= bloque <= total and bloque not in usados:
            resultado.append(palabras[bloque - 1])
            usados.add(bloque)
        i += 1

    poema = " ".join(resultado)
    st.markdown("### ✨ Poema generado:")
    st.text_area("Poema:", poema, height=200)
    st.download_button("💾 Descargar poema", poema, file_name="poema_pi.txt", mime="text/plain")

    versos = generar_versos(resultado)
    tankas = [transformar_en_tanka(verso, idx+1) for idx, verso in enumerate(versos) if transformar_en_tanka(verso, idx+1)]

    if tankas:
        st.markdown("### 🈴 Tankas generados:")
        st.text_area("Tankas:", "\n\n".join(tankas), height=400)
        st.download_button("💾 Descargar tankas", "\n\n".join(tankas), file_name="tankas_pi.txt", mime="text/plain")

else:
    st.info("📥 Sube un archivo .txt para comenzar.")