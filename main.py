import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

pg = st.navigation([
    st.Page('pages/gerencial.py', title='Gerencial'),
    # st.Page('pages/parametrico.py', title='Parâmetrico'),
    # st.Page('pages/suprimento.py', title='Suprimento'),
], position='top')

pg.run()
