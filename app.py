"""
=============================================================================
  GALPÃO LOGÍSTICO DIDÁTICO - PoC v3.5 — MEGA BRAIN GIGA CHAD EDITION
  Arquivo único: app.py
  Executar com: streamlit run app.py
=============================================================================
  • Login seguro via session_state (sem arquivos externos)
  • Tema ULTRA PREMIUM: partículas, neon glow, glassmorphism, gradientes
  • Imagens ilustrativas por setor + vídeos educativos embutidos
  • Dashboard analítico com gráficos e KPIs
=============================================================================
"""

import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🏭 Galpão Logístico Didático",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CAMINHOS DOS ASSETS
# ─────────────────────────────────────────────
ASSETS_DIR = Path(__file__).parent / "assets"

# ─────────────────────────────────────────────
# BANCO DE USUÁRIOS (simulação em memória)
# ─────────────────────────────────────────────
USUARIOS = {
    "recebimento": {"senha": "123", "cargo": "Operador de Recebimento", "icone": "📦", "cor": "#00F5D4"},
    "estoque":     {"senha": "123", "cargo": "Estoquista",              "icone": "🗄️", "cor": "#4361EE"},
    "picking":     {"senha": "123", "cargo": "Separador (Picker)",      "icone": "🛒", "cor": "#F72585"},
    "expedicao":   {"senha": "123", "cargo": "Expedidor",               "icone": "🚚", "cor": "#FFC300"},
}

# ─────────────────────────────────────────────
# CSS ULTRA PREMIUM
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ══════════════════════════════════════════════
   IMPORTAÇÕES & VARIÁVEIS
   ══════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg-primary: #07070F;
    --bg-secondary: #0D0D1A;
    --neon-cyan: #00F5D4;
    --neon-blue: #00BBF9;
    --neon-purple: #9B5DE5;
    --neon-pink: #F72585;
    --neon-magenta: #B5179E;
    --neon-orange: #FF6B35;
    --neon-yellow: #FFC300;
    --neon-green: #06D6A0;
    --text-primary: #E8EDF3;
    --text-secondary: #8892A0;
}

/* ── Animações ── */
@keyframes cosmicDrift {
    0%   { background-position: 0% 0%; }
    50%  { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(25px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes shimmerWave {
    0%   { background-position: -300% center; }
    100% { background-position: 300% center; }
}
@keyframes floatSmooth {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-8px); }
}
@keyframes glowBreath {
    0%, 100% { box-shadow: 0 0 20px rgba(155, 93, 229, 0.2); }
    50%      { box-shadow: 0 0 35px rgba(247, 37, 133, 0.35); }
}
@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
    50%      { opacity: 1; transform: scale(1) rotate(180deg); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes textGlow {
    0%, 100% { text-shadow: 0 0 10px rgba(0, 245, 212, 0.3); }
    50%      { text-shadow: 0 0 25px rgba(0, 245, 212, 0.6), 0 0 50px rgba(0, 187, 249, 0.3); }
}
@keyframes particleFloat1 {
    0%   { transform: translate(0, 0); opacity: 0; }
    10%  { opacity: 0.5; }
    90%  { opacity: 0.5; }
    100% { transform: translate(80px, -800px); opacity: 0; }
}
@keyframes particleFloat2 {
    0%   { transform: translate(0, 0); opacity: 0; }
    10%  { opacity: 0.4; }
    90%  { opacity: 0.4; }
    100% { transform: translate(-60px, -900px); opacity: 0; }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(155, 93, 229, 0.2); }
    50%      { border-color: rgba(247, 37, 133, 0.4); }
}

/* ══════════════════════════════════════════════
   FUNDO CÓSMICO
   ══════════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background:
        radial-gradient(ellipse at 15% 85%, rgba(114, 9, 183, 0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 15%, rgba(0, 187, 249, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(247, 37, 133, 0.05) 0%, transparent 60%),
        linear-gradient(180deg, #05050D 0%, #0A0A1A 30%, #0D0D25 60%, #07070F 100%) !important;
    background-size: 200% 200%, 200% 200%, 100% 100%, 100% 100% !important;
    animation: cosmicDrift 20s ease infinite !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stAppViewContainer"]::before {
    content: '✦'; position: fixed; bottom: -10px; left: 20%;
    font-size: 6px; color: rgba(155, 93, 229, 0.5);
    pointer-events: none; z-index: 0;
    animation: particleFloat1 12s linear infinite;
}
[data-testid="stAppViewContainer"]::after {
    content: '✦'; position: fixed; bottom: -10px; right: 30%;
    font-size: 4px; color: rgba(0, 245, 212, 0.4);
    pointer-events: none; z-index: 0;
    animation: particleFloat2 15s linear 3s infinite;
}
.block-container {
    background: transparent !important;
    position: relative; z-index: 1;
}

/* ── Header ── */
[data-testid="stHeader"] {
    background: linear-gradient(90deg, rgba(5,5,13,0.95), rgba(13,13,30,0.9), rgba(5,5,13,0.95)) !important;
    border-bottom: 1px solid rgba(155, 93, 229, 0.15) !important;
    backdrop-filter: blur(20px) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, rgba(8,8,20,0.97), rgba(13,13,35,0.95), rgba(10,10,25,0.97)) !important;
    border-right: 1px solid rgba(155, 93, 229, 0.12) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span,
[data-testid="stSidebar"] .stRadio label {
    color: #C8D6E5 !important;
}

/* ══════════════════════════════════════════════
   TIPOGRAFIA NEON
   ══════════════════════════════════════════════ */
h1 {
    background: linear-gradient(135deg, #00F5D4, #00BBF9, #9B5DE5, #F72585) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 900 !important;
    font-size: 2.3rem !important;
    animation: textGlow 3s ease-in-out infinite !important;
}
h2 {
    background: linear-gradient(135deg, #F72585, #FF6B35, #FFC300) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 700 !important;
}
h3 {
    background: linear-gradient(135deg, #4CC9F0, #4361EE, #9B5DE5) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════════
   BOTÕES NEON
   ══════════════════════════════════════════════ */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #7209B7, #B5179E, #F72585, #FF6B35, #FFC300) !important;
    background-size: 400% 400% !important;
    animation: cosmicDrift 5s ease infinite !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 800 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1.5px;
    text-transform: uppercase !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    box-shadow: 0 4px 20px rgba(183, 23, 158, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before, [data-testid="stFormSubmitButton"] > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: -100%; width: 100%; height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent) !important;
    transition: left 0.6s ease !important;
}
.stButton > button:hover::before, [data-testid="stFormSubmitButton"] > button:hover::before {
    left: 100% !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-4px) scale(1.03) !important;
    box-shadow: 0 10px 40px rgba(247, 37, 133, 0.4), 0 0 60px rgba(114, 9, 183, 0.15) !important;
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(-1px) scale(0.98) !important;
}

/* ══════════════════════════════════════════════
   CARDS DE MÉTRICA
   ══════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(13,13,35,0.9), rgba(7,7,20,0.95)) !important;
    border: 1px solid rgba(155, 93, 229, 0.12) !important;
    border-radius: 18px !important;
    padding: 1.3rem 1.5rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    animation: fadeInUp 0.6s ease forwards !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.03) inset !important;
}
[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: 0; right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #F72585, #B5179E, #7209B7, #4361EE, #4CC9F0, #00F5D4, #FFC300, #FF6B35, #F72585) !important;
    background-size: 300% auto !important;
    animation: shimmerWave 4s linear infinite !important;
    border-radius: 18px 18px 0 0 !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.02) !important;
    border-color: rgba(155, 93, 229, 0.35) !important;
    box-shadow: 0 15px 50px rgba(114, 9, 183, 0.2), 0 0 80px rgba(114, 9, 183, 0.06) inset !important;
}
[data-testid="stMetric"] label {
    color: #4CC9F0 !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #00F5D4, #00BBF9, #9B5DE5) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 900 !important;
    font-size: 2.1rem !important;
    font-family: 'Orbitron', sans-serif !important;
}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-weight: 700 !important;
}

/* ══════════════════════════════════════════════
   INPUTS
   ══════════════════════════════════════════════ */
input, textarea, select,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextArea"] textarea {
    background: rgba(10, 10, 25, 0.8) !important;
    color: #E8EDF3 !important;
    border: 1px solid rgba(75, 75, 140, 0.25) !important;
    border-radius: 12px !important;
    transition: all 0.35s ease !important;
    backdrop-filter: blur(15px) !important;
}
input:focus, textarea:focus {
    border-color: #9B5DE5 !important;
    box-shadow: 0 0 0 3px rgba(155,93,229,0.15), 0 0 25px rgba(155,93,229,0.1) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stTextArea label,
.stDateInput label, .stTimeInput label, .stSlider label {
    background: linear-gradient(135deg, #4CC9F0, #4361EE, #9B5DE5) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 600 !important;
}

/* ── Alertas, dividers, expanders ── */
[data-testid="stAlert"] { border-radius: 14px !important; font-weight: 500 !important; }
hr {
    border: none !important; height: 1px !important;
    background: linear-gradient(90deg, transparent, #F72585, #7209B7, #4361EE, #4CC9F0, #00F5D4, #FFC300, transparent) !important;
    margin: 2rem 0 !important; opacity: 0.7;
}
[data-testid="stExpander"] {
    background: rgba(13,13,35,0.5) !important;
    border: 1px solid rgba(75,75,140,0.2) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    transition: all 0.35s ease !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(155,93,229,0.3) !important;
    box-shadow: 0 4px 25px rgba(114,9,183,0.1) !important;
}

/* ── Forms ── */
[data-testid="stForm"] {
    background: rgba(10,10,28,0.6) !important;
    border: 1px solid rgba(75,75,140,0.18) !important;
    border-radius: 20px !important;
    padding: 1.8rem !important;
    backdrop-filter: blur(25px) !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.35) !important;
    animation: fadeInUp 0.7s ease !important;
}

/* ── Radio sidebar ── */
[data-testid="stSidebar"] .stRadio > div { gap: 5px !important; }
[data-testid="stSidebar"] .stRadio > div > label {
    background: rgba(13,13,35,0.5) !important;
    border-radius: 12px !important;
    padding: 11px 16px !important;
    transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    border: 1px solid rgba(75,75,140,0.12) !important;
    animation: slideInRight 0.4s ease forwards !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: linear-gradient(135deg, rgba(114,9,183,0.2), rgba(247,37,133,0.12)) !important;
    border-color: #B5179E !important;
    transform: translateX(6px) !important;
    box-shadow: 0 2px 20px rgba(181,23,158,0.2), -3px 0 0 #B5179E !important;
}

/* ══════════════════════════════════════════════
   IMAGENS ESTILIZADAS
   ══════════════════════════════════════════════ */
[data-testid="stImage"] {
    border-radius: 18px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 35px rgba(0,0,0,0.5), 0 0 0 1px rgba(155,93,229,0.1) !important;
    transition: all 0.4s ease !important;
}
[data-testid="stImage"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 15px 50px rgba(114,9,183,0.2), 0 0 0 1px rgba(155,93,229,0.25) !important;
}
[data-testid="stImage"] img {
    border-radius: 18px !important;
}

/* ══════════════════════════════════════════════
   CLASSES CUSTOMIZADAS
   ══════════════════════════════════════════════ */
.section-header-mega {
    background: linear-gradient(135deg, rgba(13,13,35,0.85), rgba(7,7,20,0.7));
    border-left: 4px solid;
    border-image: linear-gradient(180deg, #F72585, #7209B7, #4361EE, #00F5D4) 1;
    padding: 1.4rem 2rem;
    border-radius: 0 20px 20px 0;
    margin-bottom: 2rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.3);
    animation: fadeInUp 0.5s ease;
}
.section-header-mega p { color: #8892A0 !important; margin: 0 !important; margin-top: 6px !important; }
.glow-line-mega {
    height: 2px;
    background: linear-gradient(90deg, transparent, #F72585, #B5179E, #7209B7, #4361EE, #4CC9F0, #00F5D4, #FFC300, transparent);
    background-size: 300% auto;
    border-radius: 2px;
    margin: 2rem 0;
    animation: shimmerWave 4s linear infinite;
    box-shadow: 0 0 15px rgba(155,93,229,0.15);
}
.user-badge-mega {
    background: linear-gradient(135deg, #7209B7, #B5179E, #F72585);
    color: white; padding: 14px 20px; border-radius: 16px;
    font-weight: 800; text-align: center; margin-bottom: 10px;
    letter-spacing: 1.5px; font-size: 0.95rem;
    position: relative; overflow: hidden;
    box-shadow: 0 6px 25px rgba(114,9,183,0.4);
    animation: glowBreath 4s ease-in-out infinite;
}
.user-badge-mega::before {
    content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    animation: shimmerWave 3s ease-in-out infinite;
}
.cargo-badge-mega {
    background: rgba(0,245,212,0.08);
    border: 1px solid rgba(0,245,212,0.25);
    color: #00F5D4; padding: 10px 16px; border-radius: 12px;
    font-size: 0.82rem; text-align: center;
    font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase;
    animation: fadeInUp 0.5s ease;
}
.footer-mega {
    text-align: center; font-size: 0.7rem; color: #555B6E;
    margin-top: 1.5rem; padding: 14px;
    border-top: 1px solid rgba(75,75,140,0.15);
}
.footer-mega .brand {
    background: linear-gradient(135deg, #4CC9F0, #9B5DE5, #F72585);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-weight: 800;
    font-family: 'Orbitron', sans-serif; letter-spacing: 1px;
}
.dash-card {
    background: rgba(13,13,35,0.8);
    border: 1px solid rgba(75,75,140,0.15);
    border-radius: 18px; padding: 1.5rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 6px 30px rgba(0,0,0,0.3);
    transition: all 0.35s ease;
    animation: fadeInUp 0.6s ease;
    position: relative; overflow: hidden;
}
.dash-card:hover {
    border-color: rgba(155,93,229,0.3);
    transform: translateY(-4px);
    box-shadow: 0 12px 45px rgba(114,9,183,0.15);
}
.dash-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 18px 18px 0 0;
}
.dash-card.teal::before    { background: linear-gradient(90deg, #00F5D4, #00BBF9); }
.dash-card.purple::before  { background: linear-gradient(90deg, #7209B7, #B5179E); }
.dash-card.pink::before    { background: linear-gradient(90deg, #F72585, #FF6B35); }
.dash-card.gold::before    { background: linear-gradient(90deg, #FFC300, #FF6B35); }
.dash-card .card-icon {
    font-size: 2.8rem; margin-bottom: 10px;
    filter: drop-shadow(0 0 10px rgba(155,93,229,0.3));
    animation: floatSmooth 3s ease-in-out infinite;
}
.dash-card .card-title {
    font-family: 'Orbitron', sans-serif; font-size: 0.8rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;
}
.dash-card.teal .card-title   { color: #00F5D4; }
.dash-card.purple .card-title { color: #9B5DE5; }
.dash-card.pink .card-title   { color: #F72585; }
.dash-card.gold .card-title   { color: #FFC300; }
.dash-card .card-value {
    font-family: 'Orbitron', sans-serif; font-size: 2rem; font-weight: 900; margin: 4px 0;
}
.dash-card.teal .card-value   { color: #00F5D4; text-shadow: 0 0 20px rgba(0,245,212,0.3); }
.dash-card.purple .card-value { color: #9B5DE5; text-shadow: 0 0 20px rgba(155,93,229,0.3); }
.dash-card.pink .card-value   { color: #F72585; text-shadow: 0 0 20px rgba(247,37,133,0.3); }
.dash-card.gold .card-value   { color: #FFC300; text-shadow: 0 0 20px rgba(255,195,0,0.3); }
.dash-card .card-delta { font-size: 0.85rem; font-weight: 600; color: #06D6A0; }
.status-pill {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;
}
.status-pill.online {
    background: rgba(6,214,160,0.15); color: #06D6A0; border: 1px solid rgba(6,214,160,0.3);
}

/* ── Cores por setor nas métricas ── */
.setor-recebimento [data-testid="stMetric"]::before { background: linear-gradient(90deg, #00F5D4, #06D6A0, #00BBF9, #00F5D4) !important; }
.setor-recebimento [data-testid="stMetric"]:hover { border-color: rgba(0,245,212,0.3) !important; }
.setor-estoque [data-testid="stMetric"]::before { background: linear-gradient(90deg, #4361EE, #7209B7, #9B5DE5, #4361EE) !important; }
.setor-estoque [data-testid="stMetric"]:hover { border-color: rgba(67,97,238,0.3) !important; }
.setor-picking [data-testid="stMetric"]::before { background: linear-gradient(90deg, #F72585, #B5179E, #FF6B35, #F72585) !important; }
.setor-picking [data-testid="stMetric"]:hover { border-color: rgba(247,37,133,0.3) !important; }
.setor-expedicao [data-testid="stMetric"]::before { background: linear-gradient(90deg, #FFC300, #FF6B35, #F72585, #FFC300) !important; }
.setor-expedicao [data-testid="stMetric"]:hover { border-color: rgba(255,195,0,0.3) !important; }

/* ── Seção de mídia ── */
.media-section {
    background: rgba(13,13,35,0.6);
    border: 1px solid rgba(75,75,140,0.15);
    border-radius: 20px;
    padding: 1.5rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 6px 30px rgba(0,0,0,0.3);
    animation: fadeInUp 0.7s ease;
    margin-bottom: 1rem;
}
.media-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(75,75,140,0.15);
}
.media-title.teal   { color: #00F5D4; }
.media-title.purple { color: #9B5DE5; }
.media-title.pink   { color: #F72585; }
.media-title.gold   { color: #FFC300; }
.media-title.blue   { color: #00BBF9; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# INICIALIZAÇÃO DO SESSION STATE
# ─────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "cargo" not in st.session_state:
    st.session_state.cargo = ""
if "icone" not in st.session_state:
    st.session_state.icone = ""


# ─────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────
def autenticar(usuario: str, senha: str) -> bool:
    """Verifica credenciais contra o dicionário USUARIOS."""
    if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
        st.session_state.logado = True
        st.session_state.usuario = usuario
        st.session_state.cargo = USUARIOS[usuario]["cargo"]
        st.session_state.icone = USUARIOS[usuario]["icone"]
        return True
    return False


def logout():
    """Reseta o session state para deslogar o usuário."""
    for key in ["logado", "usuario", "cargo", "icone"]:
        st.session_state[key] = False if key == "logado" else ""


def hora_atual():
    return datetime.now().strftime("%H:%M:%S")


def data_atual():
    return datetime.now().strftime("%d/%m/%Y")


def gerar_dados_grafico(dias=7):
    """Gera dados simulados para gráficos do dashboard."""
    datas = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(dias-1, -1, -1)]
    return pd.DataFrame({
        "Dia": datas,
        "Recebimento": [random.randint(30, 90) for _ in range(dias)],
        "Estoque": [random.randint(40, 100) for _ in range(dias)],
        "Picking": [random.randint(50, 120) for _ in range(dias)],
        "Expedição": [random.randint(35, 95) for _ in range(dias)],
    })


def carregar_imagem(nome):
    """Carrega imagem da pasta assets se existir."""
    caminho = ASSETS_DIR / nome
    if caminho.exists():
        return str(caminho)
    return None


# ─────────────────────────────────────────────
# TELA DE LOGIN — CENTRALIZADA
# ─────────────────────────────────────────────
def tela_login():
    """Tela de login limpa e centralizada."""

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Layout centralizado em 3 colunas
    col_esq, col_centro, col_dir = st.columns([1, 1.3, 1])

    with col_centro:
        # Ícone animado
        st.markdown("""
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span style="font-size:4.5rem;
                         filter:drop-shadow(0 0 30px rgba(114,9,183,0.5))
                                drop-shadow(0 0 60px rgba(247,37,133,0.2));
                         animation:floatSmooth 4s ease-in-out infinite;
                         display:inline-block;">🏭</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("# Galpão Logístico")

        st.markdown("""
        <p style="text-align:center; color:#8892A0; margin-bottom:1.8rem; font-size:0.95rem;">
            ✦ Sistema Didático — Insira suas credenciais para acessar ✦
        </p>
        """, unsafe_allow_html=True)

        # Formulário de login
        with st.form("form_login", clear_on_submit=False):
            usuario = st.text_input(
                "👤 Usuário",
                placeholder="recebimento · estoque · picking · expedicao",
            )
            senha = st.text_input(
                "🔒 Senha",
                type="password",
                placeholder="Digite sua senha",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            enviar = st.form_submit_button("⚡ ENTRAR NO SISTEMA", use_container_width=True)

            if enviar:
                if usuario.strip() == "" or senha.strip() == "":
                    st.warning("⚠️ Preencha usuário e senha.")
                elif autenticar(usuario.strip().lower(), senha):
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos.")

        # Credenciais de teste
        with st.expander("💡 Credenciais de teste"):
            st.markdown("""
            | Usuário | Senha | Cargo |
            |:--------|:------|:------|
            | `recebimento` | `123` | Operador de Recebimento |
            | `estoque` | `123` | Estoquista |
            | `picking` | `123` | Separador (Picker) |
            | `expedicao` | `123` | Expedidor |
            """)


# ─────────────────────────────────────────────
# PÁGINA: INÍCIO — DASHBOARD COM IMAGEM HERO
# ─────────────────────────────────────────────
def pagina_inicio():
    """Dashboard premium com hero image, gráficos e vídeo."""
    st.markdown("""
    <div class="section-header-mega">
        <h1 style="margin:0;">🎓 Central de Aprendizagem</h1>
        <p>Painel geral do galpão — Monitoramento em tempo real dos setores</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Banner ──
    img_hero = carregar_imagem("warehouse_hero.jpg")
    if img_hero:
        st.image(img_hero, use_container_width=True,
                 caption="📸 Vista panorâmica do Galpão Logístico Didático")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Dashboard Cards ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="dash-card teal">
            <div class="card-icon">📦</div>
            <div class="card-title">Recebimento</div>
            <div class="card-value">{random.randint(45, 95)}</div>
            <div class="card-delta">▲ +{random.randint(3,12)}% vs ontem</div>
            <div style="margin-top:8px;"><span class="status-pill online">Ativo</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="dash-card purple">
            <div class="card-icon">🗄️</div>
            <div class="card-title">Estoque</div>
            <div class="card-value">{random.randint(700, 850)}</div>
            <div class="card-delta">▲ {random.randint(85,99)}% ocupação</div>
            <div style="margin-top:8px;"><span class="status-pill online">Ativo</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="dash-card pink">
            <div class="card-icon">🛒</div>
            <div class="card-title">Picking</div>
            <div class="card-value">{random.randint(100, 200)}</div>
            <div class="card-delta">▲ +{random.randint(5,18)} ped/h</div>
            <div style="margin-top:8px;"><span class="status-pill online">Ativo</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="dash-card gold">
            <div class="card-icon">🚚</div>
            <div class="card-title">Expedição</div>
            <div class="card-value">{random.randint(60, 180)}</div>
            <div class="card-delta">▲ +{random.randint(2,8)} veículos</div>
            <div style="margin-top:8px;"><span class="status-pill online">Ativo</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Gráfico + Texto ──
    col_chart, col_info = st.columns([1.3, 1])
    with col_chart:
        st.markdown("## 📈 Atividade — Últimos 7 Dias")
        df = gerar_dados_grafico(7)
        st.area_chart(df, x="Dia", y=["Recebimento", "Estoque", "Picking", "Expedição"],
                       color=["#00F5D4", "#9B5DE5", "#F72585", "#FFC300"])
    with col_info:
        st.markdown("## 📚 O que é Logística de Armazém?")
        st.markdown("""
        A **logística de armazém** é o coração da cadeia de suprimentos.

        - 🟢 **Conferência e recebimento** de mercadorias
        - 🔵 **Endereçamento e armazenagem** estratégica
        - 🟣 **Separação (picking)** precisa de pedidos
        - 🔴 **Embalagem e expedição** eficiente

        > *"Um armazém bem gerido reduz custos, acelera entregas
        > e aumenta a satisfação do cliente."*
        """)

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Vídeo + KPIs ──
    col_video, col_kpi = st.columns([1.2, 1])
    with col_video:
        st.markdown("""
        <div class="media-section">
            <div class="media-title blue">🎬 Vídeo Educativo</div>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=NMqsdKAaaaw")
        st.caption("📺 Como funciona a operação logística de um armazém moderno")
    with col_kpi:
        st.markdown("## 🏆 KPIs Globais do Turno")
        st.metric("📊 Eficiência Geral", f"{random.randint(90, 99)}%", delta=f"+{random.randint(1,5)}%")
        st.metric("⏱️ Tempo Médio de Ciclo", f"{random.randint(8, 18)} min", delta=f"-{random.randint(1,4)} min")
        st.metric("✅ Concluídos Hoje", random.randint(200, 500), delta=f"+{random.randint(10,50)}")
        st.metric("⚠️ Incidentes", random.randint(0, 3), delta=f"-{random.randint(0,2)}")

    with st.expander("📋 Sobre esta PoC"):
        st.markdown("""
        **Prova de Conceito** didática — Python 3 · Streamlit · CSS Premium

        **Features:** Login seguro · Dashboard analítico · Formulários por setor · Imagens e vídeos · Glassmorphism + Neon
        """)


# ─────────────────────────────────────────────
# PÁGINA: RECEBIMENTO
# ─────────────────────────────────────────────
def pagina_recebimento():
    st.markdown('<div class="setor-recebimento">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header-mega">
        <h1 style="margin:0;">📦 Setor de Recebimento</h1>
        <p>Registro e conferência de mercadorias na entrada do galpão</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Imagem + Vídeo do setor ──
    col_img, col_vid = st.columns(2)
    with col_img:
        st.markdown('<div class="media-section"><div class="media-title teal">📸 Área de Recebimento</div></div>', unsafe_allow_html=True)
        img = carregar_imagem("setor_recebimento.jpg")
        if img:
            st.image(img, use_container_width=True, caption="Doca de recebimento — descarga e conferência")
    with col_vid:
        st.markdown('<div class="media-section"><div class="media-title teal">🎬 Vídeo — Processo de Recebimento</div></div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=Vu8M7PtM5I8")
        st.caption("📺 Como funciona o processo de recebimento logístico")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Métricas ──
    st.markdown("### 📊 Indicadores do Turno")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("⚡ Eficiência", f"{random.randint(85, 99)}%", delta=f"+{random.randint(1,5)}%")
    with m2:
        st.metric("📄 NFs Processadas", random.randint(30, 75), delta=f"+{random.randint(2,10)}")
    with m3:
        st.metric("⚠️ Divergências", random.randint(0, 5), delta=f"-{random.randint(0,2)}")
    with m4:
        st.metric("📋 Pendentes", random.randint(2, 12), delta=f"-{random.randint(1,3)}")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Formulário ──
    st.markdown("### 📝 Registrar Recebimento de Mercadoria")
    with st.form("form_recebimento", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            nf = st.text_input("📄 Número da Nota Fiscal", placeholder="Ex: NF-2026-001234")
            sku = st.text_input("🏷️ Código SKU do Produto", placeholder="Ex: SKU-00451")
            quantidade = st.number_input("📦 Quantidade Recebida", min_value=1, max_value=9999, value=1)
        with col_b:
            fornecedor = st.text_input("🏢 Fornecedor", placeholder="Ex: Distribuidora ABC Ltda")
            condicao = st.selectbox("🔍 Condição da Carga", [
                "✅ Perfeita — Sem avarias",
                "⚠️ Avaria parcial — Alguns itens danificados",
                "❌ Carga recusada — Avaria total",
            ])
            obs = st.text_area("📋 Observações", placeholder="Detalhes adicionais...")
        enviado = st.form_submit_button("⚡ REGISTRAR RECEBIMENTO", use_container_width=True)
        if enviado:
            st.success(
                f"✅ **Simulação:** Dados enviados com sucesso para o banco de dados do Google Sheets!\n\n"
                f"- **NF:** {nf} | **SKU:** {sku} | **Qtd:** {quantidade}\n"
                f"- **Fornecedor:** {fornecedor} | **Condição:** {condicao}\n"
                f"- **Registro:** {data_atual()} às {hora_atual()}"
            )
            st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PÁGINA: ESTOQUE
# ─────────────────────────────────────────────
def pagina_estoque():
    st.markdown('<div class="setor-estoque">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header-mega">
        <h1 style="margin:0;">🗄️ Setor de Estoque</h1>
        <p>Armazenagem, endereçamento e controle de inventário</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Imagem + Vídeo ──
    col_img, col_vid = st.columns(2)
    with col_img:
        st.markdown('<div class="media-section"><div class="media-title purple">📸 Área de Estoque</div></div>', unsafe_allow_html=True)
        img = carregar_imagem("setor_estoque.jpg")
        if img:
            st.image(img, use_container_width=True, caption="Corredores de armazenagem — prateleiras organizadas")
    with col_vid:
        st.markdown('<div class="media-section"><div class="media-title purple">🎬 Vídeo — Gestão de Estoque</div></div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=RFg_JhcIB7g")
        st.caption("📺 Boas práticas de gestão de estoque em armazéns")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Métricas ──
    st.markdown("### 📊 Indicadores do Turno")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🎯 Acuracidade", f"{random.uniform(96, 99.9):.1f}%", delta=f"+{random.uniform(0.1, 1.5):.1f}%")
    with m2:
        st.metric("📍 Posições", f"{random.randint(650, 820)}/1000", delta=f"+{random.randint(5,20)}")
    with m3:
        st.metric("🔄 Movimentações", random.randint(40, 130), delta=f"+{random.randint(5,15)}")
    with m4:
        st.metric("📋 Pendentes", random.randint(3, 15), delta=f"-{random.randint(1,4)}")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Mapa de Ocupação ──
    st.markdown("### 🗺️ Mapa de Ocupação por Rua")
    mapa_data = pd.DataFrame({
        "Rua": [f"Rua {chr(65+i)}" for i in range(8)],
        "Ocupação (%)": [random.randint(55, 98) for _ in range(8)],
    })
    st.bar_chart(mapa_data, x="Rua", y="Ocupação (%)", color="#9B5DE5")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Formulário ──
    st.markdown("### 📝 Registrar Movimentação de Estoque")
    with st.form("form_estoque", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            sku_est = st.text_input("🏷️ Código SKU", placeholder="Ex: SKU-00451")
            tipo_mov = st.selectbox("🔄 Tipo de Movimentação", [
                "📥 Entrada (Armazenagem)", "📤 Saída (Separação)",
                "🔁 Transferência Interna", "📋 Inventário / Contagem",
            ])
            quantidade_est = st.number_input("📦 Quantidade", min_value=1, max_value=9999, value=1)
        with col_b:
            rua = st.selectbox("🏗️ Rua", [f"Rua {chr(65+i)}" for i in range(8)])
            prateleira = st.selectbox("📚 Prateleira", [f"Prateleira {i+1}" for i in range(6)])
            nivel = st.selectbox("📐 Nível", ["Nível 1 (Chão)", "Nível 2", "Nível 3", "Nível 4 (Topo)"])
            posicao = f"{rua} → {prateleira} → {nivel}"
        st.info(f"📍 **Endereço completo:** {posicao}")
        enviado = st.form_submit_button("⚡ REGISTRAR MOVIMENTAÇÃO", use_container_width=True)
        if enviado:
            st.success(
                f"✅ **Simulação:** Dados enviados com sucesso para o banco de dados do Google Sheets!\n\n"
                f"- **SKU:** {sku_est} | **Tipo:** {tipo_mov} | **Qtd:** {quantidade_est}\n"
                f"- **Posição:** {posicao}\n"
                f"- **Registro:** {data_atual()} às {hora_atual()}"
            )
            st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PÁGINA: PICKING
# ─────────────────────────────────────────────
def pagina_picking():
    st.markdown('<div class="setor-picking">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header-mega">
        <h1 style="margin:0;">🛒 Setor de Picking</h1>
        <p>Separação e conferência de pedidos para expedição</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Imagem + Vídeo ──
    col_img, col_vid = st.columns(2)
    with col_img:
        st.markdown('<div class="media-section"><div class="media-title pink">📸 Área de Picking</div></div>', unsafe_allow_html=True)
        img = carregar_imagem("setor_picking.jpg")
        if img:
            st.image(img, use_container_width=True, caption="Separadores em ação — picking por zona")
    with col_vid:
        st.markdown('<div class="media-section"><div class="media-title pink">🎬 Vídeo — Processos de Picking</div></div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=KGSuf5xKpOc")
        st.caption("📺 Tipos de picking: discreto, por lote, por zona e wave picking")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Métricas ──
    st.markdown("### 📊 Indicadores do Turno")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🚀 Pedidos/Hora", random.randint(18, 42), delta=f"+{random.randint(1,6)}")
    with m2:
        st.metric("❌ Taxa de Erro", f"{random.uniform(0.1, 2.5):.1f}%", delta=f"-{random.uniform(0.1, 0.8):.1f}%")
    with m3:
        st.metric("⏳ Na Fila", random.randint(5, 35), delta=f"-{random.randint(2,8)}")
    with m4:
        st.metric("⚡ Eficiência", f"{random.randint(88, 99)}%", delta=f"+{random.randint(1,4)}%")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Ranking ──
    st.markdown("### 🏆 Ranking de Separadores")
    ranking = pd.DataFrame({
        "Picker": ["Ana S.", "Carlos M.", "Juliana R.", "Pedro L.", "Maria F."],
        "Pedidos": sorted([random.randint(20, 65) for _ in range(5)], reverse=True),
        "Acertos (%)": [round(random.uniform(96, 100), 1) for _ in range(5)],
    })
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Formulário ──
    st.markdown("### 📝 Registrar Separação de Pedido")
    with st.form("form_picking", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            num_pedido = st.text_input("🧾 Número do Pedido", placeholder="Ex: PED-2026-005678")
            sku_pick = st.text_input("🏷️ SKU do Item", placeholder="Ex: SKU-00451")
            qtd_pick = st.number_input("📦 Quantidade Separada", min_value=1, max_value=999, value=1)
        with col_b:
            origem = st.text_input("📍 Posição de Origem", placeholder="Ex: Rua B → Prat. 3 → Nível 2")
            metodo = st.selectbox("⚙️ Método de Picking", [
                "🔵 Discreto (Pedido a pedido)", "🟢 Por Lote (Batch picking)",
                "🟡 Por Zona (Zone picking)", "🔴 Wave Picking (Por onda)",
            ])
            conferencia = st.selectbox("✅ Conferência", [
                "✅ Confere — SKU e quantidade OK",
                "⚠️ Divergência — Quantidade diferente",
                "❌ Erro — SKU incorreto",
            ])
        enviado = st.form_submit_button("⚡ CONFIRMAR SEPARAÇÃO", use_container_width=True)
        if enviado:
            st.success(
                f"✅ **Simulação:** Dados enviados com sucesso para o banco de dados do Google Sheets!\n\n"
                f"- **Pedido:** {num_pedido} | **SKU:** {sku_pick} | **Qtd:** {qtd_pick}\n"
                f"- **Origem:** {origem} | **Método:** {metodo}\n"
                f"- **Conferência:** {conferencia}\n"
                f"- **Registro:** {data_atual()} às {hora_atual()}"
            )
            st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PÁGINA: EXPEDIÇÃO
# ─────────────────────────────────────────────
def pagina_expedicao():
    st.markdown('<div class="setor-expedicao">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header-mega">
        <h1 style="margin:0;">🚚 Setor de Expedição</h1>
        <p>Embalagem, conferência final e despacho de pedidos</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Imagem + Vídeo ──
    col_img, col_vid = st.columns(2)
    with col_img:
        st.markdown('<div class="media-section"><div class="media-title gold">📸 Área de Expedição</div></div>', unsafe_allow_html=True)
        img = carregar_imagem("setor_expedicao.jpg")
        if img:
            st.image(img, use_container_width=True, caption="Docas de expedição — carregamento e despacho")
    with col_vid:
        st.markdown('<div class="media-section"><div class="media-title gold">🎬 Vídeo — Processo de Expedição</div></div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=pHlY09s1cAs")
        st.caption("📺 Como funciona o processo de expedição e distribuição")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Métricas ──
    st.markdown("### 📊 Indicadores do Turno")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("📬 Expedidos Hoje", random.randint(80, 220), delta=f"+{random.randint(5,25)}")
    with m2:
        st.metric("⏱️ Tempo Médio", f"{random.randint(4, 12)} min", delta=f"-{random.randint(1,3)} min")
    with m3:
        st.metric("🚛 Veículos", f"{random.randint(3, 8)}/10", delta=f"+{random.randint(1,2)}")
    with m4:
        st.metric("📋 Pendentes", random.randint(4, 18), delta=f"-{random.randint(1,5)}")

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Status das Docas ──
    st.markdown("### 🏗️ Status das Docas em Tempo Real")
    docas_cols = st.columns(6)
    status_opcoes = ["🟢 Livre", "🟡 Carregando", "🔴 Ocupada"]
    for i, c in enumerate(docas_cols):
        with c:
            status = random.choice(status_opcoes)
            cor = "#06D6A0" if "Livre" in status else "#FFC300" if "Carregando" in status else "#F72585"
            st.markdown(f"""
            <div style="background:rgba(13,13,35,0.8); border:1px solid {cor}40;
                        border-radius:14px; padding:14px; text-align:center;
                        backdrop-filter:blur(15px); box-shadow:0 4px 20px rgba(0,0,0,0.3);
                        transition:all 0.3s ease;">
                <div style="font-size:1.8rem; margin-bottom:6px;">🏗️</div>
                <div style="color:{cor}; font-weight:800; font-family:'Orbitron',sans-serif;
                            font-size:0.85rem;">DOCA {i+1}</div>
                <div style="color:{cor}; font-size:0.75rem; margin-top:4px; font-weight:600;">
                    {status}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="glow-line-mega"></div>', unsafe_allow_html=True)

    # ── Formulário ──
    st.markdown("### 📝 Registrar Expedição de Pedido")
    with st.form("form_expedicao", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            num_pedido_exp = st.text_input("🧾 Número do Pedido", placeholder="Ex: PED-2026-005678")
            num_volumes = st.number_input("📦 Número de Volumes", min_value=1, max_value=200, value=1)
            peso_total = st.number_input("⚖️ Peso Total (kg)", min_value=0.1, max_value=5000.0, value=1.0, step=0.5)
        with col_b:
            transportadora = st.selectbox("🚛 Transportadora", [
                "🟢 LogExpress Transportes", "🔵 RápidoLog Entregas",
                "🟡 TransBR Logística", "🔴 Flash Cargo Nacional",
                "⚪ Retirada pelo Cliente",
            ])
            doca = st.selectbox("🏗️ Doca de Saída", [f"Doca {i+1}" for i in range(6)])
            prioridade = st.selectbox("🔥 Prioridade", [
                "🟢 Normal", "🟡 Urgente", "🔴 Crítica (Same-Day)",
            ])
        enviado = st.form_submit_button("⚡ CONFIRMAR DESPACHO", use_container_width=True)
        if enviado:
            st.success(
                f"✅ **Simulação:** Dados enviados com sucesso para o banco de dados do Google Sheets!\n\n"
                f"- **Pedido:** {num_pedido_exp} | **Volumes:** {num_volumes} | **Peso:** {peso_total} kg\n"
                f"- **Transportadora:** {transportadora}\n"
                f"- **Doca:** {doca} | **Prioridade:** {prioridade}\n"
                f"- **Registro:** {data_atual()} às {hora_atual()}"
            )
            st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FLUXO PRINCIPAL
# ─────────────────────────────────────────────
def main():
    """Controle principal: login → sidebar → páginas."""

    if not st.session_state.logado:
        tela_login()
        return

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom:14px;">
            <span style="font-size:3rem; filter:drop-shadow(0 0 20px rgba(114,9,183,0.5));
                         animation:floatSmooth 4s ease-in-out infinite; display:inline-block;">
                🏭
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="user-badge-mega">
            {st.session_state.icone} {st.session_state.usuario.upper()}
        </div>
        <div class="cargo-badge-mega">
            ✦ {st.session_state.cargo} ✦
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        pagina = st.radio(
            "✦ NAVEGAÇÃO",
            options=[
                "🏠 Início (Central de Aprendizagem)",
                "📦 Recebimento",
                "🗄️ Estoque",
                "🛒 Picking",
                "🚚 Expedição",
            ],
            index=0,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 SAIR DO SISTEMA", use_container_width=True):
            logout()
            st.rerun()

        st.markdown(f"""
        <div class="footer-mega">
            🕐 {hora_atual()} · {data_atual()}<br>
            <span class="brand">GALPÃO LOGÍSTICO</span> v3.5
        </div>
        """, unsafe_allow_html=True)

    # ── ROTEAMENTO ──
    if "Início" in pagina:
        pagina_inicio()
    elif "Recebimento" in pagina:
        pagina_recebimento()
    elif "Estoque" in pagina:
        pagina_estoque()
    elif "Picking" in pagina:
        pagina_picking()
    elif "Expedição" in pagina:
        pagina_expedicao()


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
