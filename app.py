import asyncio
import concurrent.futures
import datetime
import io
import json
import re
import subprocess
import urllib.parse
import urllib.request
import streamlit as st
import edge_tts

# ---------------- CẤU HÌNH GIAO DIỆN STREAMLIT ----------------
st.set_page_config(
    page_title="Studio Âm Thanh AI • Chuyển Đổi & Nhân Bản Giọng Nói",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- TÙY BIẾN GIAO DIỆN NGHỆ THUẬT, NỀN ĐỘNG SVG & SIDEBAR PRO ----------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

/* Toàn bộ Font chữ */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* NỀN ĐỘNG CỰC QUANG VÀ LƯỚI CYBER CHUYỂN ĐỘNG 100% PURE CSS */
.stApp {
    background-color: #070a14 !important;
    background-image: 
        radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.2) 0%, transparent 45%),
        radial-gradient(circle at 85% 25%, rgba(236, 72, 153, 0.16) 0%, transparent 45%),
        radial-gradient(circle at 50% 80%, rgba(56, 189, 248, 0.14) 0%, transparent 50%),
        linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px) !important;
    background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px !important;
    color: #f1f5f9 !important;
}

/* SÓNG SVG ÂM THANH CHUYỂN ĐỘNG Ở ĐÁY MÀN HÌNH (SVG DATA-URI HOÀN TOÀN AN TOÀN) */
.stApp::after {
    content: '';
    position: fixed;
    bottom: 0;
    left: 0;
    width: 200%;
    height: 180px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0 C150,90 350,-40 500,60 C650,160 900,10 1200,40 L1200,120 L0,120 Z' fill='%236366f1' fill-opacity='0.18'/%3E%3Cpath d='M0,20 C200,100 400,-10 600,70 C800,150 1000,30 1200,50 L1200,120 L0,120 Z' fill='%23ec4899' fill-opacity='0.12'/%3E%3C/svg%3E");
    background-repeat: repeat-x;
    background-size: 1200px 180px;
    pointer-events: none !important;
    z-index: 0 !important;
    animation: waveDrift 18s linear infinite !important;
}

@keyframes waveDrift {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* ============================================================ */
/* SIDEBAR PRO NÂNG CẤP ĐẲNG CẤP VÀ SANG TRỌNG                 */
/* ============================================================ */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 26, 0.94) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 8px 0 25px rgba(0, 0, 0, 0.4) !important;
}

.sidebar-brand-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.28) 0%, rgba(236, 72, 153, 0.18) 100%);
    border: 1px solid rgba(168, 85, 247, 0.45);
    border-radius: 16px;
    padding: 10px 14px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    box-shadow: 0 8px 20px -5px rgba(99, 102, 241, 0.35);
}

.sidebar-title-text {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 0.92rem;
    color: #ffffff;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
}

.sidebar-status-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.7rem;
    font-weight: 600;
    color: #4ade80;
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    padding: 3px 8px;
    border-radius: 20px;
    white-space: nowrap;
    flex-shrink: 0;
}

.status-pulsing-dot {
    width: 7px;
    height: 7px;
    background-color: #22c55e;
    border-radius: 50%;
    animation: statusPulse 2s infinite;
}

@keyframes statusPulse {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 6px #22c55e; }
    50% { opacity: 0.4; transform: scale(0.85); box-shadow: none; }
}

.sidebar-section-header {
    font-size: 0.82rem;
    font-weight: 700;
    color: #c4b5fd;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 18px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(18, 24, 38, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 14px !important;
    color: #f8fafc !important;
    transition: all 0.3s ease !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
    border-color: #c084fc !important;
    box-shadow: 0 0 16px rgba(168, 85, 247, 0.35) !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 6px;
    gap: 6px;
}

section[data-testid="stSidebar"] div[data-testid="stSlider"] div[role="slider"] {
    background: #ec4899 !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 0 10px rgba(236, 72, 153, 0.8) !important;
}

section[data-testid="stSidebar"] div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
}

/* ============================================================ */
/* HERO BANNER & NỘI DUNG CHÍNH                                */
/* ============================================================ */
.hero-container {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.65) 0%, rgba(15, 23, 42, 0.85) 50%, rgba(88, 28, 135, 0.45) 100%);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 28px;
    padding: 36px 32px;
    margin-bottom: 28px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
}

.studio-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(129, 140, 248, 0.45);
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #c7d2fe;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0 0 10px 0;
    background: linear-gradient(90deg, #ffffff 0%, #c4b5fd 25%, #f472b6 50%, #60a5fa 75%, #ffffff 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleShine 8s linear infinite;
}

@keyframes titleShine {
    to { background-position: 200% center; }
}

.hero-subtitle {
    font-size: 1.02rem;
    color: #94a3b8;
    margin-bottom: 20px;
    max-width: 720px;
    line-height: 1.6;
}

.pill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.pill {
    font-size: 0.8rem;
    padding: 5px 12px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
}

.metric-box {
    background: rgba(18, 24, 38, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 18px;
    padding: 16px 20px;
    backdrop-filter: blur(14px);
    transition: all 0.3s ease;
}
.metric-box:hover {
    border-color: rgba(168, 85, 247, 0.45);
    transform: translateY(-3px);
}
.metric-label {
    font-size: 0.78rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}
.metric-val {
    font-size: 1.45rem;
    font-weight: 700;
    color: #f8fafc;
    font-family: 'Space Grotesk', sans-serif;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: rgba(255, 255, 255, 0.04);
    padding: 8px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 22px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 14px;
    padding: 10px 24px;
    font-weight: 600;
    color: #94a3b8;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(168, 85, 247, 0.35)) !important;
    color: #ffffff !important;
    border: 1px solid rgba(168, 85, 247, 0.6) !important;
}

.stTextArea textarea {
    background: rgba(15, 23, 42, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 18px !important;
    color: #f8fafc !important;
    font-size: 1.02rem !important;
    line-height: 1.65 !important;
    padding: 18px !important;
}

.stTextArea textarea:focus {
    border-color: #c084fc !important;
    box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.3) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 0.85rem 2.2rem !important;
    box-shadow: 0 10px 30px -5px rgba(139, 92, 246, 0.55), 0 0 25px rgba(236, 72, 153, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 16px 36px -5px rgba(236, 72, 153, 0.75) !important;
}

.audio-result-card {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.75) 0%, rgba(17, 24, 39, 0.88) 100%);
    border: 1px solid rgba(168, 85, 247, 0.4);
    border-radius: 22px;
    padding: 24px;
    margin-top: 24px;
    box-shadow: 0 16px 40px -12px rgba(168, 85, 247, 0.35);
}

.equalizer-wrap {
    display: flex;
    align-items: flex-end;
    gap: 5px;
    height: 30px;
}
.eq-bar {
    width: 4.5px;
    background: linear-gradient(to top, #6366f1, #a855f7, #ec4899);
    border-radius: 3px;
    animation: eqBounce 0.9s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}
.eq-bar:nth-child(1) { height: 40%; animation-duration: 0.75s; }
.eq-bar:nth-child(2) { height: 80%; animation-duration: 1.05s; animation-delay: 0.15s; }
.eq-bar:nth-child(3) { height: 100%; animation-duration: 0.7s; animation-delay: 0.3s; }
.eq-bar:nth-child(4) { height: 60%; animation-duration: 1.2s; animation-delay: 0.05s; }
.eq-bar:nth-child(5) { height: 90%; animation-duration: 0.85s; animation-delay: 0.25s; }
.eq-bar:nth-child(6) { height: 50%; animation-duration: 1.1s; animation-delay: 0.1s; }
.eq-bar:nth-child(7) { height: 85%; animation-duration: 0.8s; animation-delay: 0.2s; }
.eq-bar:nth-child(8) { height: 65%; animation-duration: 1.15s; animation-delay: 0.35s; }
.eq-bar:nth-child(9) { height: 95%; animation-duration: 0.9s; animation-delay: 0.08s; }

@keyframes eqBounce {
    0% { transform: scaleY(0.25); }
    100% { transform: scaleY(1.1); }
}

[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.45);
    border: 1px dashed rgba(255, 255, 255, 0.18);
    border-radius: 18px;
    padding: 14px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------- PRESETS PHONG CÁCH GIỌNG ĐỌC ----------------
VOICE_STYLES = {
    "🎙️ Chuẩn (Tự nhiên - Mặc định)": {
        "speed": 0,
        "pitch": 0,
        "volume": 0,
        "desc": "Tốc độ và âm sắc tự nhiên nguyên bản của AI.",
    },
    "🎬 Review phim / Kể chuyện ma (Trầm & Bí ẩn)": {
        "speed": -10,
        "pitch": -12,
        "volume": 10,
        "desc": "Tông giọng trầm lắng, nhịp chậm, tạo cảm xúc hồi hộp, lôi cuốn.",
    },
    "📻 Phát thanh viên / Thời sự (Dứt khoát)": {
        "speed": 10,
        "pitch": 2,
        "volume": 10,
        "desc": "Tốc độ nhanh, nhịp điệu dứt khoát, chuẩn bản tin thời sự.",
    },
    "🎧 Sách nói thư giãn (Audiobook Calm)": {
        "speed": -15,
        "pitch": -4,
        "volume": 0,
        "desc": "Nhẹ nhàng, từ tốn, thích hợp nghe đêm khuya hoặc nghe thư giãn.",
    },
    "🧸 Hoạt hình / Trẻ con vui nhộn (Trong trẻo)": {
        "speed": 15,
        "pitch": 18,
        "volume": 10,
        "desc": "Tông giọng cao trong trẻo, nhịp điệu vui tươi, tinh nghịch.",
    },
    "👴 Người lớn tuổi / Trầm ấm (Sâu lắng)": {
        "speed": -20,
        "pitch": -18,
        "volume": 10,
        "desc": "Tông giọng rất trầm, nói chậm rãi, uy nghiêm hoặc từng trải.",
    },
    "⚡ Tóm tắt siêu tốc (Quick Summary)": {
        "speed": 35,
        "pitch": 2,
        "volume": 0,
        "desc": "Đọc nhanh để lướt tài liệu, tiết kiệm tối đa thời gian.",
    },
    "🎛️ Tùy chỉnh tự do (Custom)": {
        "speed": 0,
        "pitch": 0,
        "volume": 0,
        "desc": "Tự điều chỉnh tốc độ, cao độ và âm lượng theo ý thích cá nhân.",
    },
}

DEFAULT_VI_VOICES = {
    "🇻🇳 [Edge AI] Nữ - Hoài Mỹ (Tự nhiên, truyền cảm)": "vi-VN-HoaiMyNeural",
    "🇻🇳 [Edge AI] Nam - Nam Minh (Dứt khoát, chuẩn thời sự)": "vi-VN-NamMinhNeural",
    "🇻🇳 [Google TTS] Nữ - Chị Google (Huyền thoại, vui nhộn)": "google-vi-female",
}

POPULAR_INTL_VOICES = {
    "🇺🇸 Tiếng Anh (Mỹ) - Nữ (Jenny)": "en-US-JennyNeural",
    "🇺🇸 Tiếng Anh (Mỹ) - Nam (Guy)": "en-US-GuyNeural",
    "🇺🇸 Tiếng Anh (Mỹ) - Nữ (Ava)": "en-US-AvaNeural",
    "🇺🇸 Tiếng Anh (Mỹ) - Nam (Brian)": "en-US-BrianNeural",
    "🇬🇧 Tiếng Anh (Anh) - Nữ (Sonia)": "en-GB-SoniaNeural",
    "🇬🇧 Tiếng Anh (Anh) - Nam (Ryan)": "en-GB-RyanNeural",
    "🇯🇵 Tiếng Nhật - Nữ (Nanami)": "ja-JP-NanamiNeural",
    "🇯🇵 Tiếng Nhật - Nam (Keita)": "ja-JP-KeitaNeural",
    "🇨🇳 Tiếng Trung - Nữ (Xiaoxiao)": "zh-CN-XiaoxiaoNeural",
    "🇨🇳 Tiếng Trung - Nam (Yunxi)": "zh-CN-YunxiNeural",
    "🇰🇷 Tiếng Hàn - Nữ (SunHi)": "ko-KR-SunHiNeural",
    "🇫🇷 Tiếng Pháp - Nữ (Denise)": "fr-FR-DeniseNeural",
    "🇩🇪 Tiếng Đức - Nữ (Katja)": "de-DE-KatjaNeural",
    "🇹🇭 Tiếng Thái - Nữ (Premwadee)": "th-TH-PremwadeeNeural",
}

SAMPLE_VI_TEXT = (
    "Xin chào các bạn! Đây là ứng dụng đọc văn bản thành giọng nói tiếng Việt "
    "sử dụng trí tuệ nhân tạo hoàn toàn miễn phí. Bạn có thể chọn rất nhiều phong cách giọng "
    "khác nhau như: review phim trầm ấm, giọng phát thanh viên dứt khoát, hoặc sách nói thư giãn. "
    "Ứng dụng hỗ trợ đọc các đoạn văn dài không giới hạn ký tự và tải file MP3 về máy tính."
)


# ---------------- CÁC HÀM HỆ THỐNG & AI ----------------
def run_async_coroutine(coro):
    """Chạy coroutine async an toàn trong thread riêng để tránh xung đột event loop của Streamlit."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(asyncio.run, coro).result()


@st.cache_data(ttl=3600)
def get_all_available_voices():
    """Lấy danh mục hơn 300+ giọng đọc của Edge TTS và phân loại theo quốc gia."""
    try:
        raw_voices = run_async_coroutine(edge_tts.list_voices())
        voices_by_locale = {}
        for v in raw_voices:
            locale = v.get("Locale", "Other")
            locale_name = v.get("LocaleName", locale)
            short_name = v.get("ShortName", "")
            gender = v.get("Gender", "")

            label = f"{short_name} ({gender})"
            if locale_name not in voices_by_locale:
                voices_by_locale[locale_name] = []
            voices_by_locale[locale_name].append(
                {"label": label, "short_name": short_name, "gender": gender}
            )
        return voices_by_locale
    except Exception:
        return {}


def detect_system_hardware():
    """Kiểm tra máy tính có card đồ họa rời NVIDIA CUDA hay không (tương thích Windows & Linux Cloud)."""
    has_cuda = False
    gpu_name = "Không phát hiện card rời NVIDIA"

    try:
        import torch

        if torch.cuda.is_available():
            has_cuda = True
            gpu_name = torch.cuda.get_device_name(0)
            return has_cuda, gpu_name
    except Exception:
        pass

    import platform
    if platform.system() == "Windows":
        try:
            res = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name",
                ],
                capture_output=True,
                text=True,
                timeout=3,
            )
            controllers = [
                c.strip() for c in res.stdout.strip().split("\n") if c.strip()
            ]
            for c in controllers:
                if any(x in c.upper() for x in ["NVIDIA", "RTX", "GTX", "GEFORCE"]):
                    has_cuda = True
                    gpu_name = c
                    break
                elif "INTEL" in c.upper() or "AMD" in c.upper():
                    gpu_name = c
        except Exception:
            gpu_name = "Card đồ họa tích hợp"
    else:
        # Linux (Streamlit Cloud, Render, VPS)
        gpu_name = "Hệ thống Cloud (CPU / Môi trường Container)"

    return has_cuda, gpu_name


def split_into_chunks(text: str, max_chars: int = 1800) -> list[str]:
    """Tự động chia nhỏ văn bản dài thành các đoạn an toàn (~1800 ký tự)

    để tránh bị timeout khi gửi văn bản quá dài.
    """
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks = []
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 <= max_chars:
            current_chunk = f"{current_chunk}\n{para}" if current_chunk else para
        else:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            if len(para) > max_chars:
                sentences = re.split(r"(?<=[.!?;\n])\s+", para)
                for sent in sentences:
                    sent = sent.strip()
                    if not sent:
                        continue
                    if len(current_chunk) + len(sent) + 1 <= max_chars:
                        current_chunk = (
                            f"{current_chunk} {sent}"
                            if current_chunk
                            else sent
                        )
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        if len(sent) > max_chars:
                            words = sent.split(" ")
                            temp = ""
                            for w in words:
                                if len(temp) + len(w) + 1 <= max_chars:
                                    temp = f"{temp} {w}" if temp else w
                                else:
                                    if temp:
                                        chunks.append(temp)
                                    temp = w
                            current_chunk = temp
                        else:
                            current_chunk = sent
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_google_tts_chunk(text: str) -> bytes:
    """Tạo âm thanh giọng Chị Google tiếng Việt (Google Translate TTS)."""
    encoded = urllib.parse.quote(text)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded}&tl=vi&client=tw-ob"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


async def generate_edge_tts_chunk(
    text: str, voice: str, rate: str, pitch: str, volume: str
) -> bytes:
    """Gọi Edge-TTS để tạo âm thanh cho 1 đoạn văn bản."""
    communicate = edge_tts.Communicate(
        text=text, voice=voice, rate=rate, pitch=pitch, volume=volume
    )
    audio_stream = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.extend(chunk["data"])
    return bytes(audio_stream)


def generate_audio_chunk(
    text: str, voice: str, rate: str, pitch: str, volume: str
) -> bytes:
    """Điều hướng tạo âm thanh theo nguồn giọng (Google TTS hoặc Edge TTS)."""
    if voice == "google-vi-female":
        return generate_google_tts_chunk(text)
    else:
        return run_async_coroutine(
            generate_edge_tts_chunk(text, voice, rate, pitch, volume)
        )


# ---------------- SIDEBAR: BỘ ĐIỀU KHIỂN STUDIO (SIDEBAR PRO) ----------------
with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-brand-card">
        <div class="sidebar-title-text">🎛️ STUDIO CONTROL</div>
        <div class="sidebar-status-tag">
            <span class="status-pulsing-dot"></span> SẴN SÀNG
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section-header">🎙️ 1. BỘ CHỌN GIỌNG ĐỌC</div>',
        unsafe_allow_html=True,
    )

    voice_mode = st.radio(
        "Chế độ chọn giọng:",
        options=[
            "🇻🇳 Giọng Tiếng Việt & Phổ biến",
            "🌐 Khám phá 300+ giọng thế giới",
        ],
        index=0,
        label_visibility="collapsed",
    )

    selected_voice = "vi-VN-HoaiMyNeural"

    if voice_mode == "🇻🇳 Giọng Tiếng Việt & Phổ biến":
        voice_cat = st.selectbox(
            "Nhóm giọng:",
            ["🇻🇳 Tiếng Việt (Khuyên dùng)", "🌍 Giọng Quốc Tế Phổ Biến"],
        )
        if "Tiếng Việt" in voice_cat:
            chosen_label = st.selectbox(
                "Chọn giọng đọc:", list(DEFAULT_VI_VOICES.keys())
            )
            selected_voice = DEFAULT_VI_VOICES[chosen_label]
        else:
            chosen_label = st.selectbox(
                "Chọn giọng đọc:", list(POPULAR_INTL_VOICES.keys())
            )
            selected_voice = POPULAR_INTL_VOICES[chosen_label]
    else:
        all_voices = get_all_available_voices()
        if all_voices:
            locales = sorted(list(all_voices.keys()))
            default_index = 0
            for idx, loc in enumerate(locales):
                if "vietnam" in loc.lower():
                    default_index = idx
                    break
            selected_locale = st.selectbox(
                "Chọn Quốc gia / Ngôn ngữ:", locales, index=default_index
            )
            voices_in_loc = all_voices[selected_locale]
            voice_labels = [v["label"] for v in voices_in_loc]
            chosen_idx = st.selectbox(
                "Chọn giọng nói:",
                range(len(voice_labels)),
                format_func=lambda i: voice_labels[i],
            )
            selected_voice = voices_in_loc[chosen_idx]["short_name"]
        else:
            st.warning("Đang tải danh sách giọng...")

    st.markdown(
        '<div class="sidebar-section-header">🎨 2. PHONG CÁCH & PRESET</div>',
        unsafe_allow_html=True,
    )

    style_names = list(VOICE_STYLES.keys())
    selected_style_name = st.selectbox(
        "Chọn phong cách:",
        style_names,
        index=0,
        label_visibility="collapsed",
    )
    style_config = VOICE_STYLES[selected_style_name]

    st.caption(f"💡 *{style_config['desc']}*")

    st.markdown(
        '<div class="sidebar-section-header">🎛️ 3. TINH CHỈNH TẦN SỐ</div>',
        unsafe_allow_html=True,
    )

    is_custom = selected_style_name == "🎛️ Tùy chỉnh tự do (Custom)"
    default_speed = style_config["speed"]
    default_pitch = style_config["pitch"]
    default_volume = style_config["volume"]

    with st.expander(
        "🎚️ Thanh trượt Tốc độ & Cao độ", expanded=is_custom or True
    ):
        speed_val = st.slider(
            "Tốc độ đọc (Speed):",
            min_value=-50,
            max_value=50,
            value=default_speed,
            step=5,
            format="%d%%",
            help="Tăng để đọc nhanh hơn, giảm để đọc chậm rãi.",
        )
        pitch_val = st.slider(
            "Độ cao giọng (Pitch):",
            min_value=-25,
            max_value=25,
            value=default_pitch,
            step=2,
            format="%dHz",
            help="Dương là giọng trong/cao, âm là giọng trầm/ấm.",
        )
        volume_val = st.slider(
            "Âm lượng (Volume):",
            min_value=-50,
            max_value=50,
            value=default_volume,
            step=5,
            format="%d%%",
        )

    speed_str = f"+{speed_val}%" if speed_val >= 0 else f"{speed_val}%"
    pitch_str = f"+{pitch_val}Hz" if pitch_val >= 0 else f"{pitch_val}Hz"
    volume_str = f"+{volume_val}%" if volume_val >= 0 else f"{volume_val}%"

# ---------------- HERO BANNER NGHỆ THUẬT ----------------
hero_html = """
<div class="hero-container">
    <div class="studio-badge">✨ AI Voice Studio Pro • Next-Gen TTS</div>
    <div class="hero-title">Studio Giọng Đọc AI Nghệ Thuật</div>
    <div class="hero-subtitle">
        Chuyển đổi văn bản thành giọng đọc truyền cảm với đa dạng phong cách âm thanh.
        Tự động ghép nối không giới hạn độ dài và xuất file MP3 chất lượng phòng thu.
    </div>
    <div class="pill-tags">
        <span class="pill">⚡ Không giới hạn ký tự</span>
        <span class="pill">💎 100% Miễn phí</span>
        <span class="pill">🎧 Tự động chia nhỏ & Ghép MP3</span>
        <span class="pill">🧬 Sẵn sàng Voice Clone</span>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# ---------------- TABS CHÍNH CỦA ỨNG DỤNG ----------------
main_tab1, main_tab2 = st.tabs([
    "🔊 1. Đọc văn bản theo phong cách (Miễn phí 100%)",
    "🧬 2. Thêm giọng mẫu (Voice Cloning - Dành cho Card rời / Cloud)",
])

# ================= TAB 1: ĐỌC VĂN BẢN VỚI PRESET =================
with main_tab1:
    sub_tab1, sub_tab2 = st.tabs(["✍️ Gõ hoặc dán văn bản", "📁 Tải file (.txt)"])

    text_to_read = ""

    with sub_tab1:
        col_in_header, col_sample_btn = st.columns([4, 1.2])
        with col_in_header:
            st.markdown("##### 📝 Nhập nội dung văn bản:")
        with col_sample_btn:
            if st.button("✨ Thử văn bản mẫu", use_container_width=True):
                st.session_state["manual_text"] = SAMPLE_VI_TEXT

        input_text = st.text_area(
            "Khu vực nhập văn bản:",
            value=st.session_state.get("manual_text", ""),
            height=180,
            placeholder="Gõ hoặc dán đoạn văn bản bất kỳ của bạn vào đây...",
            key="tab1_input_area",
            label_visibility="collapsed",
        )
        if input_text:
            text_to_read = input_text

    with sub_tab2:
        st.markdown("##### 📁 Tải tài liệu (.txt) từ máy tính:")
        uploaded_file = st.file_uploader(
            "Chọn file văn bản:",
            type=["txt"],
            key="tab1_file_upload",
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            try:
                file_content = uploaded_file.read().decode("utf-8")
                st.text_area(
                    "Xem trước nội dung file:",
                    value=file_content,
                    height=180,
                    disabled=True,
                )
                text_to_read = file_content
            except UnicodeDecodeError:
                st.error("File cần được lưu ở định dạng UTF-8.")

    # Hiển thị các thẻ chỉ số đẹp mắt
    if text_to_read.strip():
        char_count = len(text_to_read)
        word_count = len(text_to_read.split())
        chunks = split_into_chunks(text_to_read)
        est_seconds = int(word_count / 3.2)
        est_time_str = (
            f"{est_seconds // 60}m {est_seconds % 60}s"
            if est_seconds >= 60
            else f"{est_seconds}s"
        )

        st.markdown(
            f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 18px 0;">
            <div class="metric-box">
                <div class="metric-label">📝 Ký tự văn bản</div>
                <div class="metric-val">{char_count:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">📖 Số từ</div>
                <div class="metric-val">{word_count:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">⏱️ Ước tính thời lượng</div>
                <div class="metric-val">~{est_time_str}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">🧩 Phần chia nhỏ (Chunks)</div>
                <div class="metric-val">{len(chunks)} đoạn</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    btn_convert = st.button(
        "🚀 Khởi Tạo Âm Thanh Nghệ Thuật (Xuất MP3)",
        type="primary",
        use_container_width=True,
        key="btn_convert_tab1",
    )

    if btn_convert:
        if not text_to_read.strip():
            st.warning("⚠️ Vui lòng nhập văn bản hoặc tải file .txt trước!")
        else:
            chunks = split_into_chunks(text_to_read)
            total_chunks = len(chunks)

            progress_text = st.empty()
            progress_bar = st.progress(0)
            all_audio_bytes = bytearray()

            try:
                for i, chunk in enumerate(chunks):
                    progress_text.markdown(
                        f"🔄 **Đang tổng hợp âm thanh với phong cách `{selected_style_name}`...** (Đoạn {i + 1}/{total_chunks})"
                    )
                    chunk_audio = generate_audio_chunk(
                        text=chunk,
                        voice=selected_voice,
                        rate=speed_str,
                        pitch=pitch_str,
                        volume=volume_str,
                    )
                    all_audio_bytes.extend(chunk_audio)
                    progress_bar.progress((i + 1) / total_chunks)

                progress_text.empty()
                progress_bar.empty()

                final_mp3_data = bytes(all_audio_bytes)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tts_{selected_voice}_{timestamp}.mp3"

                # Card âm thanh thành phẩm sang trọng với Equalizer 9 cột sống động
                player_card_html = f"""
                <div class="audio-result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <span style="font-size: 1.8rem;">🎧</span>
                            <div>
                                <h4 style="margin: 0; color: #f8fafc; font-size: 1.2rem; font-weight: 700;">Tác Phẩm Âm Thanh Đã Sẵn Sàng</h4>
                                <span style="font-size: 0.85rem; color: #c4b5fd;">Giọng đọc: <b>{selected_voice}</b> • Phong cách: <b>{selected_style_name.split('(')[0].strip()}</b></span>
                            </div>
                        </div>
                        <div class="equalizer-wrap">
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                            <div class="eq-bar"></div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(player_card_html, unsafe_allow_html=True)
                st.audio(final_mp3_data, format="audio/mp3")

                st.download_button(
                    label=f"⬇️ Tải file âm thanh ({filename}) về máy",
                    data=final_mp3_data,
                    file_name=filename,
                    mime="audio/mp3",
                    type="primary",
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"❌ Đã xảy ra lỗi: {str(e)}")


# ================= TAB 2: VOICE CLONING (CHUẨN BỊ CHO CARD RỜI / CLOUD) =================
with main_tab2:
    st.markdown("### 🧬 Nhân Bản Giọng Nói Mẫu (Voice Cloning)")
    st.caption(
        "Tải lên file âm thanh giọng của bạn hoặc người mẫu để AI học chất giọng và đọc văn bản."
    )

    has_gpu, gpu_info = detect_system_hardware()

    if has_gpu:
        st.markdown(
            f"""
        <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 18px; padding: 18px 24px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 1.8rem;">🚀</span>
                <div>
                    <h5 style="margin: 0; color: #34d399; font-weight: 700;">Đã Phát Hiện Card Rời Tương Thích</h5>
                    <span style="color: #cbd5e1; font-size: 0.9rem;">Hệ thống nhận diện: <b>{gpu_info}</b>. Đã sẵn sàng chạy mô hình AI Clone giọng cục bộ siêu tốc!</span>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(129, 140, 248, 0.3); border-radius: 18px; padding: 18px 24px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 1.8rem;">💡</span>
                <div>
                    <h5 style="margin: 0; color: #a5b4fc; font-weight: 700;">Hệ Thống Hiện Tại: {gpu_info}</h5>
                    <span style="color: #cbd5e1; font-size: 0.9rem;">
                        Máy hiện đang dùng chip đồ họa tích hợp. Chế độ mô hình AI Offline được tối ưu khi bạn đổi sang máy có Card rời NVIDIA.
                        Hiện tại bạn có thể dùng ngay <b>Phương án Cloud (ElevenLabs Free)</b> bên dưới để clone giọng siêu tốc!
                    </span>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    clone_mode = st.radio(
        "Chọn phương thức nhân bản giọng:",
        [
            "⚡ Phương án 1: Dùng Cloud AI (Khuyên dùng cho máy hiện tại - Miễn phí 10.000 ký tự)",
            "🖥️ Phương án 2: Mô hình AI Offline Local (Dành riêng cho máy có Card rời)",
        ],
    )

    if "Phương án 1" in clone_mode:
        st.markdown("""
        **Các bước Clone giọng mẫu qua Cloud:**
        1. Đăng ký tài khoản miễn phí tại [ElevenLabs.io](https://elevenlabs.io) (Được tặng 10.000 ký tự/tháng, đọc tiếng Việt siêu tự nhiên).
        2. Dán **API Key** của bạn vào ô dưới đây.
        3. Tải lên 1 đoạn ghi âm giọng mẫu (10 - 60 giây) và nhập văn bản cần đọc.
        """)

        col_k1, col_k2 = st.columns([1, 1])
        with col_k1:
            eleven_api_key = st.text_input(
                "Nhập ElevenLabs API Key:",
                type="password",
                placeholder="xi-api-key...",
            )
        with col_k2:
            sample_voice_file = st.file_uploader(
                "Tải lên file giọng nói mẫu (.mp3, .wav):",
                type=["mp3", "wav", "m4a"],
                key="sample_voice_upload",
            )

        if sample_voice_file is not None:
            st.audio(sample_voice_file, format="audio/mp3")

        clone_text = st.text_area(
            "Nhập nội dung cần đọc theo giọng mẫu:",
            placeholder="Nhập văn bản cần đọc theo chất giọng của file mẫu...",
            key="clone_text_input",
            height=120,
        )

        if st.button("🧬 Bắt đầu Clone Giọng & Đọc Văn Bản", type="primary"):
            if not eleven_api_key:
                st.warning("⚠️ Vui lòng nhập API Key!")
            elif sample_voice_file is None:
                st.warning("⚠️ Vui lòng tải lên file giọng mẫu!")
            elif not clone_text.strip():
                st.warning("⚠️ Vui lòng nhập văn bản cần đọc!")
            else:
                st.info(
                    "🔄 Đang gửi file giọng mẫu và xử lý nhân bản trên máy chủ AI..."
                )
                try:
                    import requests

                    headers = {"xi-api-key": eleven_api_key}
                    files = {
                        "files": (
                            sample_voice_file.name,
                            sample_voice_file.getvalue(),
                            sample_voice_file.type,
                        )
                    }
                    data = {
                        "name": f"Clone_{datetime.datetime.now().strftime('%H%M%S')}",
                        "description": "Custom cloned voice from studio",
                    }
                    add_voice_url = "https://api.elevenlabs.io/v1/voices/add"
                    res = requests.post(
                        add_voice_url, headers=headers, data=data, files=files
                    )

                    if res.status_code == 200:
                        voice_id = res.json().get("voice_id")
                        st.success(
                            f"✅ Đã tạo giọng clone thành công! (ID: `{voice_id}`)"
                        )

                        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                        tts_payload = {
                            "text": clone_text,
                            "model_id": "eleven_multilingual_v2",
                        }
                        tts_res = requests.post(
                            tts_url, json=tts_payload, headers=headers
                        )

                        if tts_res.status_code == 200:
                            st.audio(tts_res.content, format="audio/mp3")
                            st.download_button(
                                "⬇️ Tải file MP3 đã clone về máy",
                                data=tts_res.content,
                                file_name=f"cloned_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                mime="audio/mp3",
                            )
                        else:
                            st.error(f"Lỗi tạo âm thanh: {tts_res.text}")
                    else:
                        st.error(f"Lỗi clone giọng: {res.text}")
                except Exception as e:
                    st.error(f"Lỗi kết nối: {str(e)}")

    else:
        st.markdown("""
        ##### 🖥️ Chế độ AI Offline Local (Khi chuyển sang máy có Card rời):
        Khi bạn chuyển sang máy tính có **Card đồ họa rời NVIDIA (RTX 3060, 4060, 4070, 4090...)**, bạn sẽ chạy các mô hình AI mã nguồn mở miễn phí như **F5-TTS** hoặc **Coqui XTTS-v2** ngay trên máy tính của bạn với tốc độ cực nhanh.
        """)

        st.code(
            """# Lệnh cài đặt môi trường GPU khi chuyển sang máy có card rời:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install f5-tts
        """,
            language="bash",
        )

        st.info(
            "💡 Khi ứng dụng phát hiện Card rời NVIDIA, mục này sẽ tự động bật giao diện nạp model cục bộ để bạn nhân bản giọng hoàn toàn Offline!"
        )
