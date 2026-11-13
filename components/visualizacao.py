import streamlit as st
import streamlit.components.v1 as components
from html import escape

def render_svg(nodes, altura_arvore):
    altura_svg = max(380, altura_arvore * 100 + 80)
    if not nodes:
        return f"""
        <svg viewBox="0 0 1000 {altura_svg}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">
          <rect width="1000" height="{altura_svg}" rx="16" fill="#0c1626"/>
          <text x="500" y="{altura_svg/2}" text-anchor="middle" fill="#71839b" font-family="Inter,sans-serif" font-size="16">A árvore está vazia. Insira um elemento para começar.</text>
        </svg>"""

    lookup = {n["value"]: n for n in nodes}
    edges = list()
    for n in nodes:
        if n["parent"] in lookup:
            p = lookup[n["parent"]]
            edges.append(
                f'<line x1="{p["x"]}" y1="{p["y"]+24}" x2="{n["x"]}" y2="{n["y"]-24}" '
                f'stroke="#52647d" stroke-width="3" stroke-linecap="round"/>'
            )

    circles = list()
    for n in nodes:
        fill = "#dc3545" if n["color"] == "red" else "#080d16"
        stroke = "#ff7b87" if n["color"] == "red" else "#718096"
        circles.append(
            f'<circle cx="{n["x"]}" cy="{n["y"]}" r="24" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
            f'<text x="{n["x"]}" y="{n["y"]+6}" text-anchor="middle" font-family="monospace" font-size="15" font-weight="600" fill="white">{escape(str(n["value"]))}</text>'
        )

    return f"""
    <svg viewBox="0 0 1000 {altura_svg}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">
      <defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#34445b" opacity=".45"/></pattern></defs>
      <rect width="1000" height="{altura_svg}" rx="16" fill="#0c1626"/>
      <rect width="1000" height="{altura_svg}" rx="16" fill="url(#dots)"/>
      {''.join(edges)}
      {''.join(circles)}
    </svg>"""

def exibir_visualizacao(arvore):
    st.markdown("### 🌳 Visualização da árvore")
    st.markdown('<p class="muted">Nós circulares conectados por arestas; vermelho e preto representam as cores dos nós.</p>', unsafe_allow_html=True)
    
    nodes = arvore.obter_dados_svg()
    altura = arvore.altura()
    qtd_nos = arvore.contar_nos()
    raiz_val = str(arvore.raiz.chave) if arvore.raiz != arvore.NIL else "—"
    estado = "Vazia" if qtd_nos == 0 else "Balanceada"

    svg_html = render_svg(nodes, altura)
    components.html(svg_html, height=max(400, altura * 100 + 100), scrolling=False)

    cols = st.columns(4)
    for col, label, value in zip(cols, ["Nós", "Altura", "Raiz", "Estado"], [str(qtd_nos), str(altura), raiz_val, estado]):
        with col:
            st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
