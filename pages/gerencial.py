import pathlib
import pandas as pd
import streamlit as st
import streamlit.components.v2 as stc
import streamlit.components.v1 as components

from data.monday import get_dataModay
from data.supabase import fetch_data_from_tablefull

data_rdo = pd.DataFrame(fetch_data_from_tablefull("Bot_Atividade"))
data_monday = pd.DataFrame(get_dataModay(926240878))
data_monday['PRODUTO'] = data_monday['PRODUTO'].str.replace('GERENCIAMENTO DE OBRA ', '', regex=False)

obras = data_monday['SIGLA'].dropna().unique().tolist()
rcrs = data_monday['RCR'].dropna().unique().tolist()
cidades = data_monday['CIDADE'].dropna().unique().tolist()
prod = data_monday['PRODUTO'].dropna().unique().tolist()

option_view = {
     0: ':material/view_agenda:',
     1: ':material/table:'
}

col1, col2, col3 = st.columns([2, 4, 1])
with col1:
	st.image('./images/Logo Verde.png', width=200)
with col2:
	st.header('GERENCIAMENTO DE OBRAS')
with col3:
    if st.button('Atualizar Dados'):
        st.cache_data.clear()
        st.rerun()

st.write('####')
with st.expander("Filtros", expanded=True, icon="⚙️"):
    col01, col02, col03, col04 = st.columns(4)
    sel_prod = col01.pills('Selecione a Produto', options=prod, selection_mode='multi', key="sel_fase", default=prod[0])
    if sel_prod:
        data_monday = data_monday[data_monday['PRODUTO'].isin(sel_prod)]
        rcrs = data_monday['RCR'].dropna().unique().tolist()
        cidades = data_monday['CIDADE'].dropna().unique().tolist()
        obras = data_monday['SIGLA'].dropna().unique().tolist()
    # sel_rcr = col03.multiselect('Selecione o RCR', options=rcrs, key='sel_rcr')
    # sel_cid = col04.multiselect('Selecione a Cidade', options=cidades, key='sel_cid')
    sel_obra = col02.multiselect("Filtrar por Obra (Sigla)", options=obras, key='sel_obra')

# st.dataframe(data_monday)

# with st.container(border=True):
#     flex = st.container(horizontal=True, horizontal_alignment="right")
#     modo_view = flex.segmented_control(
#         "Modo de Visualização",
#         label_visibility="hidden",
#         options=option_view.keys(),
#         format_func=lambda x: option_view[x],
#         selection_mode="single",
#         default=0,
#     )

#     if modo_view == 0:
#         with st.container(border=True):
#             st.header('Modo de visualização selecionado: Agenda')
#             components.iframe("https://app.constructin.com.br/#/v?t=rzb63r95tmsd0n2awfbme&p=3534", height=500)
#     else:
#         st.header('Modo de visualização selecionado:')
    

frontend_dir = pathlib.Path(__file__).parent.resolve().parent / "components" / "calendar"
calen = stc.component(
    "calend",
    html=pathlib.Path(frontend_dir / "index.html").read_text(encoding="utf-8"),
    js=pathlib.Path(frontend_dir / "script.js").read_text(encoding="utf-8"),
    css=pathlib.Path(frontend_dir / "styles.css").read_text(encoding="utf-8")
)

if sel_obra:
    obras = sel_obra

for obra in obras:
    monday_obra = data_monday[data_monday['SIGLA'] == obra]
    datas = data_rdo[data_rdo['obra'] == obra]['date_in'].tolist()
    if datas:
        with st.expander(obra, expanded=True):
            tabStatus, tabPBI, tabVISI, tabRDO = st.tabs(['Status RDO', 'Relatório Gerencial', 'VISI', 'RDO + Efetivo'])
            with tabStatus:
                datas_dict = {str(data): "check" for data in datas}
                mes = calen(data=datas_dict, on_clicked_change=lambda: None)
            with tabPBI:
                components.iframe(monday_obra['PBI_RG'].iloc[0], height=500)
            with tabVISI:
                components.iframe(monday_obra['VISI'].iloc[0], height=500)
            with tabRDO:
                components.iframe(monday_obra['PBI_RE'].iloc[0], height=500)
        
# with st.container(border=True):
#     mes = calen(data=datas, on_clicked_change=lambda: None)

# st.write(f"Month selected: {mes}")