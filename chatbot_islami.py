import streamlit as st
import google.generativeai as genai
import random
import re
from datetime import datetime

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="NurChat - Chatbot Islami Aman",
    page_icon="🕌",
    layout="centered"
)

# ========== API KEY ==========
API_KEY = "AIzaSyAhHstmNSgP2zcSU4ccatuR_3lb0NEW5nI"

# ========== KONFIGURASI MODEL YANG BENAR ==========
try:
    genai.configure(api_key=API_KEY)
    
    # Gunakan model yang PASTI tersedia
    # Pilihan model yang valid untuk Gemini API:
    # - "gemini-1.5-flash" (cepat, gratis, rekomendasi)
    # - "gemini-1.5-pro" (lebih akurat)
    # - "gemini-1.0-pro" (versi lama)
    
    AVAILABLE_MODELS = ["gemini-1.5-flash", "gemini-1.5-pro","gemini-2.5-flash", "gemini-1.0-pro"]
    MODEL_NAME = "gemini-2.5-flash"  # Ganti jika perlu
    
    model = genai.GenerativeModel(MODEL_NAME)
    st.success(f"✅ Model {MODEL_NAME} berhasil dimuat!")
    
except Exception as e:
    st.error(f"❌ Gagal memuat model: {str(e)}")
    st.info("💡 Coba periksa API Key atau koneksi internet Anda")
    st.stop()

# ========== DAFTAR KATA TERLARANG ==========
FORBIDDEN_WORDS = [
    "anjing", "babi", "sial", "brengsek", "goblok", "idiot", "bego",
    "tolol", "memek", "kontol", "peler", "ngentot", "jembut",
    "sex", "seks", "porno", "bugil", "telanjang", "bokep",
    "mesum", "vibrator", "pelacur", "psk",
    "bunuh", "membunuh", "darah", "bunuh diri",
    "narkoba", "sabu", "ganja", "cocaine", "heroin",
    "judi", "togel", "slot", "casino",
]

# ========== TOPIK ISLAMI ==========
ISLAMIC_TOPICS = [
    "shalat", "sholat", "wudhu", "puasa", "zakat", "haji", "umroh",
    "quran", "alquran", "surat", "ayat", "tajwid", "doa", "dzikir",
    "hadits", "rasulullah", "nabi", "islam", "iman", "akhlak", "adab",
    "ramadhan", "idul fitri", "idul adha"
]

# ========== FUNGSI KEAMANAN ==========
def contains_forbidden_words(text):
    text_lower = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            return True, word
    return False, None

def is_islamic_topic(text):
    text_lower = text.lower()
    for topic in ISLAMIC_TOPICS:
        if topic in text_lower:
            return True
    return False

def get_safe_islamic_response(question):
    """Dapatkan respons Islami yang aman"""
    
    # Cek kata terlarang
    has_forbidden, bad_word = contains_forbidden_words(question)
    if has_forbidden:
        return f"""🙏 **Maaf, kata '{bad_word}' tidak pantas untuk diucapkan.**

Rasulullah SAW bersabda:
> *"Barang siapa yang beriman kepada Allah dan hari akhir, hendaklah dia berkata yang baik atau diam."* (HR. Bukhari & Muslim)

Mari bertanya tentang hal-hal yang bermanfaat ya! 😊"""
    
    # Cek apakah topik Islam
    if not is_islamic_topic(question) and len(question.split()) > 3:
        return """🕌 **Ayo tanya tentang Islam saja ya!**

✅ Contoh pertanyaan:
• Bagaimana tata cara wudhu?
• Apa surat pendek yang mudah dihafal?
• Doa sebelum makan apa?
• Bagaimana akhlak yang baik?

Coba tanyakan sesuatu tentang Islam ya! 🌟"""
    
    # Prompt untuk chatbot
    safe_prompt = f"""Kamu adalah Asisten Islami yang ramah untuk anak-anak.

Aturan:
1. Jawab pertanyaan tentang Islam dengan bahasa sederhana
2. Maksimal 3-4 kalimat
3. Gunakan emoji yang ramah
4. Awali dengan "Assalamu'alaikum" jika sesuai

Pertanyaan: {question}

Jawab dengan ramah:"""

    try:
        response = model.generate_content(safe_prompt)
        return response.text
    except Exception as e:
        # Tampilkan error detail untuk debugging
        error_msg = str(e)
        if "API key" in error_msg:
            return "❌ **API Key tidak valid!**\n\nSilakan periksa API Key Anda. Dapatkan API Key gratis di: https://aistudio.google.com/"
        elif "quota" in error_msg.lower():
            return "⚠️ **Kuota API habis!**\n\nKuota gratis Gemini API可能有 batasan. Coba lagi nanti atau gunakan API Key lain."
        else:
            return f"🙏 **Maaf, ada gangguan teknis.**\n\nError: {error_msg[:100]}\n\nCoba lagi ya, insyaAllah bisa! 😊"

# ========== CSS TAMPILAN ==========
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
    }
    .judul-utama {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(45deg, #FFD700, #fcd34d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subjudul {
        text-align: center;
        color: #fef3c7;
        font-size: 18px;
    }
    .safety-badge {
        background-color: #10b981;
        color: white;
        padding: 5px 20px;
        border-radius: 30px;
        display: inline-block;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ========== TAMPILAN UTAMA ==========
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<p style="font-size: 60px; text-align: center;">🕌📿</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="judul-utama">NurChat</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subjudul">Asisten Islami untuk Belajar Agama dengan Aman 😊</p>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;"><span class="safety-badge">🔒 Dilindungi Filter Keamanan</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("## 🕌 **Assalamu'alaikum!**")
    st.caption(f"📅 {datetime.now().strftime('%A, %d %B %Y')}")
    
    st.markdown("---")
    st.markdown("### 💡 **Tips:**")
    st.info("""
    ✅ Tanyakan tentang:
    - Shalat, wudhu, puasa
    - Doa harian
    - Akhlak mulia
    - Al-Qur'an
    """)
    
    st.markdown("### 🔧 **Status:**")
    try:
        # Test koneksi
        test_response = model.generate_content("Halo")
        st.success("✅ API Connected")
    except:
        st.error("❌ API Error - Cek koneksi")

# ========== INISIALISASI CHAT ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Assalamu'alaikum! 👋 Aku NurChat. Ada yang ingin ditanyakan tentang Islam? 🕌"
    })

# ========== MENAMPILKAN PESAN ==========
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👨‍🎓"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])

# ========== INPUT DARI USER ==========
if prompt := st.chat_input("Ketik pertanyaan tentang Islam di sini... 🕌"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔍 Mencari jawaban..."):
            safe_answer = get_safe_islamic_response(prompt)
            st.markdown(safe_answer)
            st.session_state.messages.append({"role": "assistant", "content": safe_answer})

# ========== TOMBOL PERTANYAAN CEPAT ==========
st.markdown("---")
st.markdown("### 🎯 **Contoh Pertanyaan:**")

quick_questions = [
    "🤲 Doa sebelum makan apa?",
    "🕌 Bagaimana tata cara wudhu?",
    "📖 Surat Al-Fatihah artinya apa?",
    "💫 Apa itu puasa Ramadhan?",
]

cols = st.columns(2)
for i, question in enumerate(quick_questions):
    col = cols[i % 2]
    with col:
        if st.button(f"{question}", use_container_width=True, key=f"quick_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user", avatar="👨‍🎓"):
                st.markdown(question)
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🔍 Mencari jawaban..."):
                    answer = get_safe_islamic_response(question)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

# ========== TOMBOL HAPUS ==========
if st.button("🗑️ Mulai Percakapan Baru", use_container_width=True):
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Assalamu'alaikum! 👋 Yuk belajar Islam lagi! 🕌"
    }]
    st.rerun()

st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #fef3c7; font-size: 12px;">
🕌 NurChat • Chatbot Islami yang Aman
</p>
""", unsafe_allow_html=True)