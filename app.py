
import streamlit as st
import streamlit.components.v1 as components
from html import escape

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

NODES = [
    {"value":20,"color":"black","x":500,"y":75,"parent":None},
    {"value":10,"color":"red","x":290,"y":190,"parent":20},
    {"value":30,"color":"black","x":710,"y":190,"parent":20},
    {"value":5,"color":"black","x":185,"y":305,"parent":10},
    {"value":15,"color":"black","x":395,"y":305,"parent":10},
    {"value":25,"color":"red","x":605,"y":305,"parent":30},
    {"value":40,"color":"red","x":815,"y":305,"parent":30},
]

def render_svg(nodes):
    lookup = {n["value"]: n for n in nodes}
    edges = []
    for n in nodes:
        if n["parent"] in lookup:
            p = lookup[n["parent"]]
            edges.append(f'<line x1="{p["x"]}" y1="{p["y"]+25}" x2="{n["x"]}" y2="{n["y"]-25}" stroke="#52647d" stroke-width="3" stroke-linecap="round"/>')
    circles = []
    for n in nodes:
        fill = "#dc3545" if n["color"] == "red" else "#080d16"
        stroke = "#ff7b87" if n["color"] == "red" else "#718096"
        circles.append(f'<circle cx="{n["x"]}" cy="{n["y"]}" r="25" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/><text x="{n["x"]}" y="{n["y"]+6}" text-anchor="middle" font-family="monospace" font-size="16" font-weight="600" fill="white">{escape(str(n["value"]))}</text>')
    return f"""
    <svg viewBox="0 0 1000 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">
      <defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#34445b" opacity=".45"/></pattern></defs>
      <rect width="1000" height="380" rx="16" fill="#0c1626"/>
      <rect width="1000" height="380" rx="16" fill="url(#dots)"/>
      {''.join(edges)}
      {''.join(circles)}
      <text x="500" y="365" text-anchor="middle" fill="#71839b" font-family="Inter,sans-serif" font-size="12">Árvore de exemplo — valores e cores ilustrativos</text>
    </svg>"""

if "feedback" not in st.session_state:
    st.session_state.feedback = "A árvore exibida é demonstrativa. A lógica de inserção e remoção será conectada na próxima etapa."

st.markdown("""
<div class="hero">
  <div class="eyebrow">ESTRUTURAS DE DADOS · LABORATÓRIO INTERATIVO</div>
  <h1>Árvore Rubro-Negra</h1>
  <p>Explore a estrutura, acompanhe as operações e visualize o balanceamento da árvore.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([0.78, 2.22], gap="large")
with left:
    st.markdown("### ⚙️ Operações")
    with st.container(border=True):
        st.markdown("**Inserir elemento**")
        value_in = st.number_input("Valor para inserir", value=50, step=1, key="insert_value")
        if st.button("＋ Inserir na árvore", type="primary", use_container_width=True):
            st.session_state.feedback = f"Solicitação de inserção do valor {value_in} recebida. O algoritmo será conectado na próxima etapa."
            st.rerun()
    with st.container(border=True):
        st.markdown("**Remover elemento**")
        value_out = st.number_input("Valor para remover", value=10, step=1, key="remove_value")
        if st.button("－ Remover da árvore", use_container_width=True):
            st.session_state.feedback = f"Solicitação de remoção do valor {value_out} recebida. O algoritmo será conectado na próxima etapa."
            st.rerun()
    if st.button("↻ Restaurar exemplo", use_container_width=True):
        st.session_state.feedback = "Exemplo demonstrativo restaurado. Nenhuma operação real foi executada."
        st.rerun()
    st.markdown('<p class="muted">Nesta versão, os botões são apenas a interface. A árvore ainda não é modificada.</p>', unsafe_allow_html=True)

with right:
    st.markdown("### 🌳 Visualização da árvore")
    st.markdown('<p class="muted">Nós circulares conectados por arestas; vermelho e preto representam as cores dos nós.</p>', unsafe_allow_html=True)
    components.html(render_svg(NODES), height=400, scrolling=False)
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Nós","Altura","Raiz","Estado"], ["7","3","20","Exemplo"]):
        with col:
            st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.markdown("### 📋 Retorno da interface")
st.info(st.session_state.feedback, icon="ℹ️")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Legenda**")
    st.markdown('<span style="color:#ff6575">●</span> Nó vermelho &nbsp;&nbsp; <span style="color:#aab8ca">●</span> Nó preto', unsafe_allow_html=True)
with c2:
    with st.expander("Próximas etapas"):
        st.markdown("""
        1. Criar a classe `No` e a estrutura da árvore.
        2. Implementar inserção, recoloração e rotações.
        3. Implementar remoção e os casos de correção.
        4. Atualizar o SVG após cada operação.
        5. Criar um modo passo a passo para explicar cada caso.
        """)
