import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import base64
import os
from emotion_detector import EmotionDetector
from emotion_processor import EmotionProcessor
from emotion_music_map import get_recommendations, get_all_emotions
from spotify_client import SpotifyClient
# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎵 MoodTunes – Emotion Music AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ── Helper: load image as base64 ─────────────────────────────────────────────
def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
hero_b64     = img_to_base64(os.path.join(ASSETS, "hero_banner.png"))
emotions_b64 = img_to_base64(os.path.join(ASSETS, "emotion_cards.png"))
music_b64    = img_to_base64(os.path.join(ASSETS, "music_bg.png"))

# ── Emotion meta-data ────────────────────────────────────────────────────────
EMOTION_META = {
    "happy":    {"emoji": "😄", "color": "#FFD700", "gradient": "linear-gradient(135deg,#FFD700,#FF8C00)", "desc": "Feeling joyful"},
    "sad":      {"emoji": "😢", "color": "#4FC3F7", "gradient": "linear-gradient(135deg,#4FC3F7,#1565C0)", "desc": "Feeling melancholic"},
    "angry":    {"emoji": "😠", "color": "#FF5252", "gradient": "linear-gradient(135deg,#FF5252,#B71C1C)", "desc": "Feeling intense"},
    "neutral":  {"emoji": "😐", "color": "#80CBC4", "gradient": "linear-gradient(135deg,#80CBC4,#00695C)", "desc": "Feeling calm"},
    "surprise": {"emoji": "😲", "color": "#CE93D8", "gradient": "linear-gradient(135deg,#CE93D8,#6A1B9A)", "desc": "Feeling amazed"},
    "fear":     {"emoji": "😨", "color": "#B39DDB", "gradient": "linear-gradient(135deg,#B39DDB,#311B92)", "desc": "Feeling nervous"},
    "disgust":  {"emoji": "🤢", "color": "#A5D6A7", "gradient": "linear-gradient(135deg,#A5D6A7,#1B5E20)", "desc": "Feeling uneasy"},
}

GENRE_COLORS = {
    "Pop": "#FF6B9D", "Rock": "#FF4500", "Indie": "#7B68EE",
    "Acoustic": "#DEB887", "Ambient": "#40E0D0", "Lo-Fi": "#9370DB",
    "Classical": "#DAA520", "Funk": "#FF7F50", "Metal": "#778899",
    "Electronic": "#00CED1", "Hip-Hop": "#FF6347", "Nu-Metal": "#CD5C5C",
    "Grunge": "#6B8E23", "Indie Folk": "#F4A460", "Disco-Pop": "#FF69B4",
    "Indie Rock": "#9932CC", "Indie Pop": "#DDA0DD", "Alternative Rock": "#20B2AA",
    "Synthwave": "#9400D3", "Alternative": "#FF0099",
}

# ── Master CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

  /* Global reset */
  html, body, [class*="css"] {{
      font-family: 'Inter', sans-serif;
  }}
  .stApp {{
      background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 40%, #12002a 100%);
      color: #e8e8f5;
  }}

  /* ── Hero banner ── */
  .hero-section {{
      position: relative;
      border-radius: 24px;
      overflow: hidden;
      margin-bottom: 2rem;
      box-shadow: 0 25px 80px rgba(130,80,255,0.4);
  }}
  .hero-section img {{
      width: 100%;
      max-height: 340px;
      object-fit: cover;
      display: block;
      border-radius: 24px;
      filter: brightness(0.75) saturate(1.3);
  }}
  .hero-overlay {{
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg, rgba(10,10,26,0.92) 0%, rgba(10,10,26,0.55) 55%, transparent 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 2.5rem 3rem;
  }}
  .hero-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.8rem;
      font-weight: 800;
      background: linear-gradient(90deg, #c084fc, #60a5fa, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.15;
      margin: 0 0 0.5rem;
  }}
  .hero-subtitle {{
      font-size: 1.05rem;
      color: #b0b8d4;
      margin: 0 0 1.4rem;
      font-weight: 400;
  }}
  .hero-badges {{
      display: flex;
      gap: 0.6rem;
      flex-wrap: wrap;
  }}
  .badge {{
      padding: 5px 14px;
      border-radius: 50px;
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
  }}
  .badge-ai   {{ background: rgba(139,92,246,0.25); border: 1px solid #7c3aed; color: #c4b5fd; }}
  .badge-live {{ background: rgba(16,185,129,0.20); border: 1px solid #059669; color: #6ee7b7; }}
  .badge-ml   {{ background: rgba(59,130,246,0.20); border: 1px solid #2563eb; color: #93c5fd; }}

  /* ── Stat cards ── */
  .stat-grid {{ display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap; }}
  .stat-card {{
      flex:1; min-width:140px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 1.2rem 1.4rem;
      backdrop-filter: blur(12px);
      text-align: center;
      transition: transform .2s, box-shadow .2s;
      position: relative; overflow: hidden;
  }}
  .stat-card::before {{
      content:''; position:absolute; inset:-1px;
      border-radius:16px;
      background: linear-gradient(135deg, rgba(139,92,246,0.3), transparent 60%);
      opacity:0; transition:opacity .3s;
  }}
  .stat-card:hover {{ transform:translateY(-4px); box-shadow:0 12px 40px rgba(139,92,246,0.25); }}
  .stat-card:hover::before {{ opacity:1; }}
  .stat-number {{ font-size:2rem; font-weight:800; color:#fff; line-height:1; }}
  .stat-label  {{ font-size:0.78rem; color:#7c8ba1; text-transform:uppercase; letter-spacing:.06em; margin-top:.35rem; }}
  .stat-icon   {{ font-size:1.6rem; margin-bottom:.5rem; }}

  /* ── Section headings ── */
  .section-heading {{
      font-family:'Space Grotesk',sans-serif;
      font-size:1.35rem; font-weight:700;
      color:#fff;
      display:flex; align-items:center; gap:.5rem;
      margin-bottom:1.2rem;
      border-left:3px solid #8b5cf6;
      padding-left:.85rem;
  }}

  /* ── Camera panel ── */
  .camera-panel {{
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(139,92,246,0.2);
      border-radius: 20px;
      padding: 1.5rem;
      backdrop-filter: blur(16px);
      height: 100%;
  }}

  /* ── Button overrides ── */
  .stButton > button {{
      width:100%;
      border-radius:12px !important;
      font-weight:600 !important;
      font-size:0.9rem !important;
      padding:0.65rem 1rem !important;
      border:none !important;
      transition: all .25s !important;
      letter-spacing:.02em;
  }}
  div[data-testid="column"]:nth-child(1) .stButton > button {{
      background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
      color: #fff !important;
      box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
  }}
  div[data-testid="column"]:nth-child(1) .stButton > button:hover {{
      box-shadow: 0 8px 28px rgba(124,58,237,0.6) !important;
      transform: translateY(-2px) !important;
  }}
  div[data-testid="column"]:nth-child(2) .stButton > button {{
      background: rgba(255,255,255,0.07) !important;
      color: #e8e8f5 !important;
      border: 1px solid rgba(255,255,255,0.15) !important;
  }}
  div[data-testid="column"]:nth-child(3) .stButton > button {{
      background: linear-gradient(135deg, #059669, #047857) !important;
      color: #fff !important;
      box-shadow: 0 4px 20px rgba(5,150,105,0.35) !important;
  }}

  /* ── Detected emotion result ── */
  .emotion-result {{
      background: rgba(255,255,255,0.04);
      border-radius: 20px;
      padding: 1.5rem;
      border: 1px solid rgba(255,255,255,0.08);
      margin-top: 1rem;
      display: flex;
      align-items: center;
      gap: 1.2rem;
  }}
  .emotion-emoji-big {{ font-size: 3.5rem; line-height:1; }}
  .emotion-name {{
      font-family:'Space Grotesk',sans-serif;
      font-size:1.6rem;
      font-weight:700;
      color:#fff;
  }}
  .emotion-desc {{ font-size:.85rem; color:#8892a4; margin-top:.2rem; }}
  .confidence-bar-bg {{
      height:6px; background:rgba(255,255,255,0.1);
      border-radius:10px; margin-top:.6rem; overflow:hidden;
  }}
  .confidence-bar {{
      height:100%; border-radius:10px;
      transition: width 1s ease;
  }}

  /* ── Music recommendation panel ── */
  .music-panel {{
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(100,200,255,0.15);
      border-radius: 20px;
      padding: 1.5rem;
      backdrop-filter: blur(16px);
      height: 100%;
  }}
  .music-panel-header {{
      position: relative;
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 1.2rem;
      height: 110px;
  }}
  .music-panel-header img {{
      width:100%; height:100%;
      object-fit:cover;
      filter: brightness(0.55) saturate(1.4);
  }}
  .music-panel-header-text {{
      position:absolute;
      inset:0;
      display:flex; align-items:center; padding:1rem 1.4rem;
      gap:.8rem;
  }}
  .music-panel-mood {{
      font-family:'Space Grotesk',sans-serif;
      font-size:1.1rem; font-weight:700; color:#fff;
  }}
  .music-panel-sub {{ font-size:.8rem; color:#b0c0d8; }}

  /* ── Song card ── */
  .song-card {{
      display:flex; align-items:center; gap:1rem;
      padding:.9rem 1.1rem;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius:14px;
      margin-bottom:.65rem;
      transition: all .2s;
      cursor:default;
  }}
  .song-card:hover {{
      background: rgba(139,92,246,0.12);
      border-color: rgba(139,92,246,0.35);
      transform: translateX(4px);
  }}
  .song-num {{
      font-size:.8rem; color:#5a6580; font-weight:700;
      min-width:20px;
  }}
  .song-disc {{
      width:44px; height:44px; border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      font-size:1.3rem; flex-shrink:0;
      animation: spinDisc 4s linear infinite;
      animation-play-state: paused;
  }}
  .song-card:hover .song-disc {{ animation-play-state: running; }}
  @keyframes spinDisc {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}
  .song-info {{ flex:1; min-width:0; }}
  .song-title {{
      font-weight:600; color:#e8e8f5;
      font-size:.92rem; white-space:nowrap;
      overflow:hidden; text-overflow:ellipsis;
  }}
  .song-artist {{ font-size:.8rem; color:#7c8ba1; margin-top:.15rem; }}
  .genre-pill {{
      font-size:.7rem; font-weight:700;
      padding:3px 10px; border-radius:50px;
      letter-spacing:.04em;
      flex-shrink:0;
  }}

  /* ── Emotion gallery cards ── */
  .gallery-container {{
      display:grid;
      grid-template-columns: repeat(7, 1fr);
      gap:.7rem;
      margin:1.5rem 0;
  }}
  .gallery-card {{
      border-radius:16px;
      padding:1rem .5rem;
      text-align:center;
      transition:all .25s;
      cursor:default;
      border: 1px solid rgba(255,255,255,0.07);
      backdrop-filter: blur(8px);
  }}
  .gallery-card:hover {{ transform:translateY(-6px); box-shadow:0 16px 40px rgba(0,0,0,0.4); }}
  .gallery-emoji {{ font-size:2rem; display:block; margin-bottom:.4rem; }}
  .gallery-label {{
      font-size:.75rem; font-weight:700;
      text-transform:uppercase; letter-spacing:.06em;
      color:rgba(255,255,255,0.85);
  }}

  /* ── Stats distribution bar ── */
  .dist-bar-wrap {{ margin-bottom:.7rem; }}
  .dist-bar-label {{
      display:flex; justify-content:space-between;
      font-size:.82rem; color:#9aa5b8; margin-bottom:.25rem;
  }}
  .dist-bar-bg {{
      height:8px; background:rgba(255,255,255,0.07);
      border-radius:10px; overflow:hidden;
  }}
  .dist-bar-fill {{
      height:100%; border-radius:10px;
      background: linear-gradient(90deg, #7c3aed, #3b82f6);
      transition: width 1.2s ease;
  }}

  /* ── How it works ── */
  .steps-grid {{
      display:grid; grid-template-columns:repeat(4,1fr);
      gap:1rem; margin:1rem 0;
  }}
  .step-card {{
      background:rgba(255,255,255,0.03);
      border:1px solid rgba(255,255,255,0.08);
      border-radius:16px; padding:1.2rem;
      text-align:center;
      transition:all .2s;
  }}
  .step-card:hover {{
      background:rgba(139,92,246,0.08);
      border-color:rgba(139,92,246,0.3);
      transform:translateY(-3px);
  }}
  .step-icon {{ font-size:2rem; margin-bottom:.6rem; }}
  .step-num {{
      font-size:.7rem; color:#7c3aed; font-weight:700;
      text-transform:uppercase; letter-spacing:.08em;
      margin-bottom:.3rem;
  }}
  .step-title {{ font-size:.9rem; font-weight:600; color:#e8e8f5; margin-bottom:.3rem; }}
  .step-text  {{ font-size:.78rem; color:#6b7590; line-height:1.45; }}

  /* ── Sidebar overrides ──  */
  [data-testid="stSidebar"] {{
      background: rgba(10,10,30,0.95) !important;
      border-right: 1px solid rgba(139,92,246,0.15) !important;
  }}
  [data-testid="stSidebar"] .stMarkdown h2 {{
      font-family:'Space Grotesk',sans-serif;
      background: linear-gradient(90deg,#c084fc,#60a5fa);
      -webkit-background-clip:text; -webkit-text-fill-color:transparent;
      background-clip:text;
  }}
  .stSlider [data-baseweb="slider"] {{
      padding: 0 6px;
  }}
  .stSlider [data-testid="stThumbValue"] {{
      color: #c084fc !important;
  }}

  /* ── Alert/info override ── */
  [data-testid="stAlert"] {{
      border-radius: 12px !important;
  }}

  /* divider */
  hr {{ border-color: rgba(139,92,246,0.2) !important; margin: 2rem 0 !important; }}

  /* pandas table */
  [data-testid="stDataFrame"] {{
      background: rgba(255,255,255,0.02) !important;
      border-radius: 12px !important;
  }}

  /* Spotify Button override */
  .spotify-btn > button {{
      background: linear-gradient(135deg, #1DB954, #191414) !important;
      color: #fff !important;
      border: none !important;
      transition: opacity 0.3s;
  }}
  .spotify-btn > button:hover {{
      opacity: 0.8 !important;
  }}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if 'emotion_processor' not in st.session_state:
    st.session_state.emotion_processor = EmotionProcessor()
if 'detector' not in st.session_state:
    st.session_state.detector = EmotionDetector()
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'frames_captured' not in st.session_state:
    st.session_state.frames_captured = 0
if 'detection_complete' not in st.session_state:
    st.session_state.detection_complete = False
if 'last_emotion' not in st.session_state:
    st.session_state.last_emotion = None
if 'last_confidence' not in st.session_state:
    st.session_state.last_confidence = 0.0
if 'spotify_client' not in st.session_state:
    st.session_state.spotify_client = None
if 'spotify_auth_status' not in st.session_state:
    st.session_state.spotify_auth_status = "None"

# ── Hero Banner ───────────────────────────────────────────────────────────────
if hero_b64:
    st.markdown(f"""
    <div class="hero-section">
        <img src="data:image/png;base64,{hero_b64}" alt="MoodTunes Banner"/>
        <div class="hero-overlay">
            <div class="hero-title">🎵 MoodTunes AI</div>
            <div class="hero-subtitle">Real-time emotion detection meets personalized music curation</div>
            <div class="hero-badges">
                <span class="badge badge-ai">🤖 AI Powered</span>
                <span class="badge badge-live">⚡ Live Detection</span>
                <span class="badge badge-ml">🧠 Computer Vision</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("# 🎵 MoodTunes – Emotion-Based Music Recommendation")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    st.markdown("**📷 Detection**")
    detection_duration = st.slider("Capture Duration (sec)", 1, 10, 3)
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    st.markdown("---")
    st.markdown("**🎛️ Display**")
    show_stats = st.checkbox("Show Statistics", value=True)
    show_how = st.checkbox("Show How It Works", value=True)
    st.markdown("---")
    st.markdown("**🎧 Spotify Integration**")
    spotify_client_id = st.text_input("Client ID", type="password", help="Your Spotify API Client ID")
    spotify_client_secret = st.text_input("Client Secret", type="password", help="Your Spotify API Client Secret")
    
    st.markdown('<div class="spotify-btn">', unsafe_allow_html=True)
    if st.button("Connect to Spotify", use_container_width=True):
        if spotify_client_id and spotify_client_secret:
            client = SpotifyClient(spotify_client_id, spotify_client_secret)
            if client.authenticate():
                st.session_state.spotify_client = client
                st.session_state.spotify_auth_status = "Connected"
            else:
                st.session_state.spotify_auth_status = "Error"
                st.error(f"❌ Auth Failed: {client.auth_error}")
        else:
            st.warning("Please enter both ID and Secret.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.spotify_auth_status == "Connected":
        st.markdown("<div style='color:#1DB954;font-size:0.9rem;font-weight:bold;margin-top:0.5rem;'>✓ Connected to Spotify</div>", unsafe_allow_html=True)

    st.markdown("---")
    if emotions_b64:
        st.markdown("**🎭 Emotion Guide**")
        st.markdown(f'<img src="data:image/png;base64,{emotions_b64}" style="width:100%;border-radius:12px;margin-top:.5rem;"/>',
                    unsafe_allow_html=True)

# ── Live stat bar (session totals) ────────────────────────────────────────────
stats_live = st.session_state.emotion_processor.get_emotion_stats()
detected_count = stats_live['total_frames']
unique_count   = stats_live['unique_emotions']
top_emo        = stats_live['top_emotion'] or "—"
avg_conf       = stats_live['average_confidence']

top_meta = EMOTION_META.get(top_emo, {"emoji": "🎭"})

st.markdown(f"""
<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-icon">📸</div>
    <div class="stat-number">{detected_count}</div>
    <div class="stat-label">Frames Analyzed</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🎭</div>
    <div class="stat-number">{unique_count}</div>
    <div class="stat-label">Unique Emotions</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">{top_meta.get("emoji","🎭")}</div>
    <div class="stat-number" style="font-size:1.4rem">{top_emo.upper() if top_emo != "—" else "—"}</div>
    <div class="stat-label">Dominant Mood</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🎯</div>
    <div class="stat-number">{avg_conf:.0%}</div>
    <div class="stat-label">Avg Confidence</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main Columns ──────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

# ──── LEFT: Emotion Detection ─────────────────────────────────────────────────
with col1:
    st.markdown('<div class="section-heading">📹 Live Emotion Detection</div>', unsafe_allow_html=True)

    with st.container():
        video_placeholder  = st.empty()
        status_placeholder = st.empty()

        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            start_button = st.button("🎬 Start Camera", key="start_camera", use_container_width=True)
        with btn2:
            reset_button = st.button("🔄 Reset", key="reset", use_container_width=True)
        with btn3:
            analyze_button = st.button("📊 Analyze", key="analyze", use_container_width=True)

    # button logic
    if reset_button:
        st.session_state.emotion_processor.reset()
        st.session_state.frames_captured = 0
        st.session_state.detection_complete = False
        st.session_state.last_emotion = None
        st.session_state.last_confidence = 0.0
        st.rerun()

    if start_button:
        st.session_state.camera_active = True
        st.session_state.detection_complete = False

    # camera capture
    if st.session_state.camera_active:
        st.info("📷 Position your face clearly, then click **Take photo**.")
        picture = st.camera_input("Take a photo", label_visibility="collapsed")

        if picture is not None:
            st.session_state.emotion_processor.reset()
            st.session_state.frames_captured = 0
            try:
                image_array = np.array(Image.open(picture))
                frame = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                emotion, confidence, face_box = st.session_state.detector.detect_emotion(frame)

                if emotion is not None:
                    frame = st.session_state.detector.draw_emotion_on_frame(frame, emotion, confidence, face_box)
                    st.session_state.emotion_processor.add_emotion(emotion, confidence)
                    st.session_state.frames_captured = 1
                    st.session_state.last_emotion    = emotion
                    st.session_state.last_confidence = confidence

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(frame_rgb, use_column_width=True)
                    status_placeholder.success(f"✅ Detected: **{emotion.upper()}** — confidence {confidence:.0%}")
                else:
                    status_placeholder.warning("⚠️ No face detected. Try better lighting or move closer.")

                st.session_state.camera_active = False
                st.session_state.detection_complete = True

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # ── Detected Emotion Result Card ──
    if st.session_state.last_emotion:
        em = st.session_state.last_emotion
        meta = EMOTION_META.get(em, {"emoji":"🎭","gradient":"linear-gradient(135deg,#6b7280,#374151)","desc":"","color":"#9aa5b8"})
        conf_pct = int(st.session_state.last_confidence * 100)
        st.markdown(f"""
        <div class="emotion-result">
          <div class="emotion-emoji-big">{meta['emoji']}</div>
          <div style="flex:1">
            <div class="emotion-name" style="background:{meta['gradient']};-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">{em.upper()}</div>
            <div class="emotion-desc">{meta['desc']}</div>
            <div style="font-size:.8rem;color:#9aa5b8;margin-top:.4rem;">Confidence</div>
            <div class="confidence-bar-bg">
              <div class="confidence-bar" style="width:{conf_pct}%;background:{meta['gradient']};"></div>
            </div>
            <div style="font-size:.8rem;color:{meta['color']};font-weight:700;margin-top:.25rem;">{conf_pct}%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ──── RIGHT: Music Recommendations ───────────────────────────────────────────
with col2:
    st.markdown('<div class="section-heading">🎶 Music Recommendations</div>', unsafe_allow_html=True)

    if st.session_state.detection_complete and st.session_state.frames_captured > 0:
        top_emotion, count = st.session_state.emotion_processor.get_top_emotion()

        if top_emotion:
            recs  = get_recommendations(top_emotion)
            meta  = EMOTION_META.get(top_emotion, {"emoji":"🎭","gradient":"linear-gradient(135deg,#6b7280,#374151)","desc":""})

            # Music header with background image
            if music_b64:
                st.markdown(f"""
                <div class="music-panel-header">
                  <img src="data:image/png;base64,{music_b64}" alt="music bg"/>
                  <div class="music-panel-header-text">
                    <div style="font-size:2.8rem">{meta['emoji']}</div>
                    <div>
                      <div class="music-panel-mood">{recs['mood']}</div>
                      <div class="music-panel-sub">Detected: <strong style="color:#c084fc">{top_emotion.upper()}</strong> · {count} frame(s)</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Song cards
            spotify_used = False
            if st.session_state.spotify_client and st.session_state.spotify_client.is_authenticated:
                spotify_tracks = st.session_state.spotify_client.get_tracks_for_emotion(top_emotion)
                if spotify_tracks:
                    spotify_used = True
                    for i, song in enumerate(spotify_tracks, 1):
                        img_url = song.get("image_url", "")
                        st.markdown(f"""
                        <div class="song-card" style="padding-right:0.5rem">
                          <span class="song-num">{i:02d}</span>
                          <img src="{img_url}" style="width:50px;height:50px;border-radius:10px;object-fit:cover;margin:0 10px;" onerror="this.src='https://via.placeholder.com/50'"/>
                          <div class="song-info">
                            <div class="song-title"><a href="{song['spotify_url']}" target="_blank" style="color:#e8e8f5;text-decoration:none;">{song['title']}</a></div>
                            <div class="song-artist">🎤 {song['artist']}</div>
                          </div>
                          <a href="{song['spotify_url']}" target="_blank" style="text-decoration:none;">
                            <span class="genre-pill" style="background:rgba(29, 185, 84, 0.18);color:#1DB954;border:1px solid #1DB95433;">Open in Spotify ↑</span>
                          </a>
                        </div>
                        """, unsafe_allow_html=True)
                        if song.get("preview_url"):
                            st.audio(song["preview_url"])
            
            if not spotify_used:
                for i, song in enumerate(recs['songs'], 1):
                    genre_color = GENRE_COLORS.get(song['genre'], "#8b5cf6")
                    discs = ["🎵","🎶","🎸","🎹","🎺","🎻","🥁"]
                    disc  = discs[i % len(discs)]
                    st.markdown(f"""
                    <div class="song-card">
                      <span class="song-num">{i:02d}</span>
                      <div class="song-disc" style="background:rgba({int(genre_color[1:3],16)},{int(genre_color[3:5],16)},{int(genre_color[5:7],16)},0.15);">{disc}</div>
                      <div class="song-info">
                        <div class="song-title">{song['title']}</div>
                        <div class="song-artist">🎤 {song['artist']}</div>
                      </div>
                      <span class="genre-pill" style="background:rgba({int(genre_color[1:3],16)},{int(genre_color[3:5],16)},{int(genre_color[5:7],16)},0.18);color:{genre_color};border:1px solid {genre_color}33;">{song['genre']}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No emotion detected. Please try again.")

    else:
        if not st.session_state.detection_complete:
            if music_b64:
                st.markdown(f"""
                <div class="music-panel-header">
                  <img src="data:image/png;base64,{music_b64}" alt="music bg"/>
                  <div class="music-panel-header-text">
                    <div style="font-size:2.5rem">🎵</div>
                    <div>
                      <div class="music-panel-mood">Ready to detect your mood?</div>
                      <div class="music-panel-sub">Start the camera to get personalized music</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            st.info("📌 Click **Start Camera** to detect your emotion and receive song recommendations.")
        else:
            st.warning("⚠️ No emotion was detected above the confidence threshold.")

# ── Statistics Section ────────────────────────────────────────────────────────
if st.session_state.detection_complete and st.session_state.frames_captured > 0 and show_stats:
    st.markdown("---")
    st.markdown('<div class="section-heading">📊 Detection Statistics</div>', unsafe_allow_html=True)

    emotion_df = st.session_state.emotion_processor.get_emotion_dataframe()

    if not emotion_df.empty:
        stats_full = st.session_state.emotion_processor.get_emotion_stats()
        total = stats_full['total_frames']

        sc1, sc2 = st.columns([1, 1], gap="large")
        with sc1:
            st.markdown("**Emotion Distribution**")
            for _, row in emotion_df.iterrows():
                em_name  = row['Emotion']
                em_count = int(row['Count'])
                em_pct   = em_count / total * 100
                em_meta  = EMOTION_META.get(em_name, {"emoji":"🎭","color":"#8b5cf6"})
                st.markdown(f"""
                <div class="dist-bar-wrap">
                  <div class="dist-bar-label">
                    <span>{em_meta['emoji']} {em_name.capitalize()}</span>
                    <span style="color:{em_meta['color']};font-weight:700">{em_count} ({em_pct:.0f}%)</span>
                  </div>
                  <div class="dist-bar-bg">
                    <div class="dist-bar-fill" style="width:{em_pct}%;background:{em_meta.get('gradient','linear-gradient(90deg,#7c3aed,#3b82f6)')};"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        with sc2:
            st.markdown("**Raw Data**")
            display_df = emotion_df[['Emotion','Count','Avg_Confidence']].copy()
            display_df.columns = ['Emotion','Count','Avg Confidence']
            display_df['Avg Confidence'] = display_df['Avg Confidence'].map(lambda x: f"{x:.0%}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.bar_chart(
                emotion_df.set_index('Emotion')['Count'],
                use_container_width=True,
                color="#7c3aed",
            )

# ── Emotion Gallery ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-heading">🎭 Emotion Palette</div>', unsafe_allow_html=True)

gallery_html = '<div class="gallery-container">'
for em_name, em_meta in EMOTION_META.items():
    gallery_html += f"""
    <div class="gallery-card" style="background:{em_meta['gradient'].replace('linear-gradient','linear-gradient').replace('135deg','135deg')};opacity:0.85;">
      <span class="gallery-emoji">{em_meta['emoji']}</span>
      <span class="gallery-label">{em_name}</span>
    </div>"""
gallery_html += '</div>'
st.markdown(gallery_html, unsafe_allow_html=True)

# ── How It Works ─────────────────────────────────────────────────────────────
if show_how:
    st.markdown('<div class="section-heading">🚀 How It Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="steps-grid">
      <div class="step-card">
        <div class="step-icon">💡</div>
        <div class="step-num">Step 01</div>
        <div class="step-title">Prepare</div>
        <div class="step-text">Ensure good lighting and face the camera directly for best results.</div>
      </div>
      <div class="step-card">
        <div class="step-icon">🎬</div>
        <div class="step-num">Step 02</div>
        <div class="step-title">Capture</div>
        <div class="step-text">Click <strong>Start Camera</strong> and take a photo when ready.</div>
      </div>
      <div class="step-card">
        <div class="step-icon">🤖</div>
        <div class="step-num">Step 03</div>
        <div class="step-title">Detect</div>
        <div class="step-text">AI vision model analyzes your facial features and identifies your emotion.</div>
      </div>
      <div class="step-card">
        <div class="step-icon">🎵</div>
        <div class="step-num">Step 04</div>
        <div class="step-title">Enjoy</div>
        <div class="step-text">Receive handpicked music recommendations tailored to your current mood.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem 0 2rem;color:#4a5568;">
  <span style="font-size:1.1rem">🎵</span>
  <span style="font-size:.85rem;"> Built with <strong style="color:#7c3aed">Streamlit</strong>, <strong style="color:#3b82f6">OpenCV</strong> &amp; Computer Vision &nbsp;·&nbsp; </span>
  <span style="font-size:.85rem;color:#c084fc">MoodTunes AI</span>
</div>
""", unsafe_allow_html=True)
