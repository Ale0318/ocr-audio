import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(
    page_title="VisionText AI",
    page_icon="📸",
    layout="wide"
)

# =========================
# ESTILOS VISUALES
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f3e7ff, #e0c3fc, #c2e9fb);
    background-attachment: fixed;
}

h1, h2, h3 {
    color: #2d1b4e;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
}

.stButton>button {
    background-color: #7b2cbf;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #9d4edd;
    color: white;
}

textarea, input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# VARIABLES
# =========================
text = ""

# =========================
# FUNCIÓN TTS
# =========================
def text_to_speech(input_language, output_language, text, tld):

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    trans_text = translation.text

    tts = gTTS(
        trans_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"

    tts.save(f"temp/{my_file_name}.mp3")

    return my_file_name, trans_text

# =========================
# LIMPIAR AUDIOS ANTIGUOS
# =========================
def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

# =========================
# HEADER
# =========================
st.title("📸 VisionText AI")
st.markdown("### Extrae texto desde imágenes y conviértelo en audio multilenguaje")

st.markdown("---")

# =========================
# SUBHEADER
# =========================
st.subheader("🖼️ Selecciona una imagen desde cámara o archivos")

# =========================
# CÁMARA
# =========================
cam_ = st.checkbox("📸 Activar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Tomar fotografía")
else:
    img_file_buffer = None

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("⚙️ Centro de Control")

    st.subheader("📷 Procesamiento de Cámara")

    filtro = st.radio(
        "Aplicar filtro",
        ('Sí', 'No')
    )

# =========================
# SUBIR IMAGEN
# =========================
bg_image = st.file_uploader(
    "📤 Subir imagen",
    type=["png", "jpg", "jpeg"]
)

if bg_image is not None:

    uploaded_file = bg_image

    st.image(
        uploaded_file,
        caption='Imagen cargada',
        use_container_width=True
    )

    # Guardar imagen
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    st.success(f"✅ Imagen guardada como {uploaded_file.name}")

    img_cv = cv2.imread(f'{uploaded_file.name}')

    img_rgb = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(img_rgb)

    st.markdown("### ✨ Texto Detectado")
    st.info(text)

# =========================
# PROCESAMIENTO CÁMARA
# =========================
if img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(img_rgb)

    st.success("✅ Texto reconocido correctamente")

    st.markdown("### ✨ Texto Detectado")
    st.info(text)

# =========================
# TRADUCTOR
# =========================
with st.sidebar:

    st.markdown("---")

    st.subheader("🌍 Parámetros de Traducción")

    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()

    # Lenguaje entrada
    in_lang = st.selectbox(
        "🌐 Lenguaje de entrada",
        (
            "Ingles",
            "Español",
            "Bengali",
            "Koreano",
            "Mandarin",
            "Japones"
        ),
    )

    if in_lang == "Ingles":
        input_language = "en"

    elif in_lang == "Español":
        input_language = "es"

    elif in_lang == "Bengali":
        input_language = "bn"

    elif in_lang == "Koreano":
        input_language = "ko"

    elif in_lang == "Mandarin":
        input_language = "zh-cn"

    elif in_lang == "Japones":
        input_language = "ja"

    # Lenguaje salida
    out_lang = st.selectbox(
        "🗣️ Lenguaje de salida",
        (
            "Ingles",
            "Español",
            "Bengali",
            "Koreano",
            "Mandarin",
            "Japones"
        ),
    )

    if out_lang == "Ingles":
        output_language = "en"

    elif out_lang == "Español":
        output_language = "es"

    elif out_lang == "Bengali":
        output_language = "bn"

    elif out_lang == "Koreano":
        output_language = "ko"

    elif out_lang == "Mandarin":
        output_language = "zh-cn"

    elif out_lang == "Japones":
        output_language = "ja"

    # Acento
    english_accent = st.selectbox(
        "🎙️ Selecciona el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )

    if english_accent == "Default":
        tld = "com"

    elif english_accent == "India":
        tld = "co.in"

    elif english_accent == "United Kingdom":
        tld = "co.uk"

    elif english_accent == "United States":
        tld = "com"

    elif english_accent == "Canada":
        tld = "ca"

    elif english_accent == "Australia":
        tld = "com.au"

    elif english_accent == "Ireland":
        tld = "ie"

    elif english_accent == "South Africa":
        tld = "co.za"

    display_output_text = st.checkbox("📄 Mostrar traducción")

# =========================
# BOTÓN
# =========================
st.markdown("---")

if st.button("🎧 Traducir y Generar Audio"):

    if text.strip() != "":

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )

        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )

        audio_bytes = audio_file.read()

        st.success("🔊 Audio generado exitosamente")

        st.markdown("## 🔊 Resultado de Audio")

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )

        if display_output_text:

            st.markdown("## 📄 Texto Traducido")

            st.info(output_text)

    else:
        st.warning("⚠️ Primero debes cargar una imagen con texto")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    "<center>🧠 Desarrollado con OCR + IA + Traducción Automática</center>",
    unsafe_allow_html=True
)
