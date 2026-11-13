import streamlit as st
from arvore.arvore_rubronegra import ArvoreRubroNegra

def criar_arvore_exemplo():
    arv = ArvoreRubroNegra()
    for val in (20, 10, 30, 5, 15, 25, 40):
        arv.inserir(val)
    return arv

def exibir_controles():
    st.markdown("### ⚙️ Operações")
    arvore = st.session_state.arvore

    with st.container(border=True):
        st.markdown("**Inserir elemento**")
        value_in = st.number_input("Valor para inserir", value=50, step=1, key="insert_value")
        if st.button("＋ Inserir na árvore", type="primary", use_container_width=True):
            sucesso, msg = arvore.inserir(int(value_in))
            st.session_state.feedback = msg
            st.session_state.feedback_tipo = "success" if sucesso else "warning"
            st.rerun()

    with st.container(border=True):
        st.markdown("**Remover elemento**")
        value_out = st.number_input("Valor para remover", value=10, step=1, key="remove_value")
        if st.button("－ Remover da árvore", use_container_width=True):
            sucesso, msg = arvore.remover(int(value_out))
            st.session_state.feedback = msg
            st.session_state.feedback_tipo = "success" if sucesso else "error"
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("↻ Exemplo", use_container_width=True):
            st.session_state.arvore = criar_arvore_exemplo()
            st.session_state.feedback = "Árvore de exemplo restaurada."
            st.session_state.feedback_tipo = "info"
            st.rerun()
    with col2:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.arvore = ArvoreRubroNegra()
            st.session_state.feedback = "Árvore limpa. Pronta para novas inserções."
            st.session_state.feedback_tipo = "info"
            st.rerun()
