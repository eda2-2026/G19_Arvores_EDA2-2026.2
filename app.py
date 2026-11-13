import streamlit as st
from components.controles import exibir_controles, criar_arvore_exemplo
from components.visualizacao import exibir_visualizacao
from components.informacoes import exibir_informacoes

st.set_page_config(page_title="Simulador de Árvore Rubro-Negra", page_icon="🌳", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background:#0b1120; color:#e5e7eb; }
.block-container { max-width:1250px; padding-top:2rem; }
header, footer { visibility:hidden; }
.hero { padding:1.5rem 1.7rem; border:1px solid #263449; border-radius:18px; background:linear-gradient(120deg,#131f33,#101827 70%,#1b1728); margin-bottom:1.2rem; }
.eyebrow { color:#93a4bd; font-size:.72rem; font-weight:700; letter-spacing:.15em; }
.hero h1 { color:#f8fafc; font-size:2rem; margin:.35rem 0; font-weight:800; }
.hero p,.muted { color:#aab8ca; font-size:.88rem; }
.metric { background:#111c2d; border:1px solid #263449; border-radius:14px; padding:.85rem 1rem; }
.metric-label { color:#93a4b8; font-size:.75rem; }
.metric-value { color:#f8fafc; font-size:1.4rem; font-weight:800; margin-top:.15rem; }
.stButton button { border-radius:10px; min-height:2.6rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)

if "arvore" not in st.session_state:
    st.session_state.arvore = criar_arvore_exemplo()
if "feedback" not in st.session_state:
    st.session_state.feedback = "Simulador conectado! Insira ou remova valores para visualizar o balanceamento."
    st.session_state.feedback_tipo = "info"

st.markdown("""
<div class="hero">
  <div class="eyebrow">ESTRUTURAS DE DADOS · LABORATÓRIO INTERATIVO</div>
  <h1>Árvore Rubro-Negra</h1>
  <p>Explore a estrutura, acompanhe as operações e visualize o balanceamento da árvore.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns((0.78, 2.22), gap="large")
with left:
    exibir_controles()

with right:
    exibir_visualizacao(st.session_state.arvore)

exibir_informacoes()
