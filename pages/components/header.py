import streamlit as st

def _render_header(titleAdicional: str = ''):
    col1, col2, col3 = st.columns([2, 4, 1])
    with col1:
        st.image('./images/Logo Verde.png', width=200)
    with col2:
        st.header('GERENCIAMENTO DE OBRAS' + (' - ' + titleAdicional.upper() if titleAdicional else ''))
    with col3:
        if st.button('Atualizar Dados'):
            st.cache_data.clear()
            st.rerun()
    st.write('####')
