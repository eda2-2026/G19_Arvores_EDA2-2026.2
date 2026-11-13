import streamlit as st

def exibir_informacoes():
    st.markdown("### 📋 Retorno da interface")
    tipo = st.session_state.get("feedback_tipo", "info")
    msg = st.session_state.get("feedback", "")

    if tipo == "success":
        st.success(msg, icon="✅")
    elif tipo == "warning":
        st.warning(msg, icon="⚠️")
    elif tipo == "error":
        st.error(msg, icon="❌")
    else:
        st.info(msg, icon="ℹ️")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Legenda**")
        st.markdown('<span style="color:#ff6575">●</span> Nó vermelho &nbsp;&nbsp; <span style="color:#aab8ca">●</span> Nó preto', unsafe_allow_html=True)
    with c2:
        with st.expander("Regras da Árvore Rubro-Negra"):
            st.markdown("""
            1. Todo nó é **vermelho** ou **preto**.
            2. A raiz é sempre **preta**.
            3. Nós vermelhos não podem ter filhos vermelhos.
            4. Todos os caminhos de um nó até as folhas possuem a mesma quantidade de nós pretos.
            """)
