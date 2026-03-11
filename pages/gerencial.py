import pathlib
import pandas as pd
import streamlit as st
import streamlit.components.v2 as stc

from data.monday import get_dataModay
from pages.components.header import _render_header
from data.supabase import fetch_data_from_tablefull
from pages.gerencial_config import COLUMN_CONFIG, COLS_MAP, style_prediction

frontend_dir = pathlib.Path(__file__).parent.resolve().parent / "components" / "calendarTabular"
frontend_dir_pbi = pathlib.Path(__file__).parent.resolve().parent / "components" / "calendarTabular_PBI"
calen = stc.component(
    "calend",
    html=pathlib.Path(frontend_dir / "index.html").read_text(encoding="utf-8"),
    js=pathlib.Path(frontend_dir / "script.js").read_text(encoding="utf-8"),
    css=pathlib.Path(frontend_dir / "style.css").read_text(encoding="utf-8")
)
calenPBI = stc.component(
    "calend_pbi",
    html=pathlib.Path(frontend_dir_pbi / "index.html").read_text(encoding="utf-8"),
    js=pathlib.Path(frontend_dir_pbi / "script.js").read_text(encoding="utf-8"),
    css=pathlib.Path(frontend_dir / "style.css").read_text(encoding="utf-8")
)

data_rdo = pd.DataFrame(fetch_data_from_tablefull("Bot_Atividade"))
data_pbi = pd.DataFrame(fetch_data_from_tablefull("Powerbi_reports"))
data_gerencial = pd.DataFrame(fetch_data_from_tablefull("Map_PBI"))
data_monday = pd.DataFrame(get_dataModay(926240878))

data_monday['PRODUTO'] = data_monday['PRODUTO'].str.replace('GERENCIAMENTO DE OBRA ', '', regex=False)
data_monday = data_monday[~data_monday['RCR'].isin(['', 'DELETED MEMBER', 'MEMBRO EXCLUÍDO'])]
data_gerencial = data_gerencial.drop_duplicates(subset=['tendencia'])

obras = data_monday['SIGLA'].dropna().unique().tolist()
prod = data_monday['PRODUTO'].dropna().unique().tolist()

option_view = {
     0: ':material/view_agenda:',
     1: ':material/table:'
}

_render_header()

with st.expander("Filtros", expanded=True, icon="⚙️"):
    df_filtered = data_monday[['SIGLA', 'PRODUTO', 'RCR', 'CIDADE']].copy()
    df_filtered = df_filtered.assign(RCR=df_filtered['RCR'].str.split(',')).explode('RCR')
    df_filtered['RCR'].fillna('SEM RCR', inplace=True)
    col01, col02, col03, col04 = st.columns(4)

    prod_opts = sorted(df_filtered['PRODUTO'].dropna().unique().tolist())
    default_prod = ['RESIDENCIAL'] if 'RESIDENCIAL' in prod_opts else (prod_opts if prod_opts else None)
    sel_prod = col01.pills(
        'Selecione a Produto',
        options=prod_opts,
        selection_mode='multi',
        key="sel_fase",
        default=default_prod,
        help="Selecione os produtos para filtrar. Por padrão, 'RESIDENCIAL' está selecionado se disponível.",
    )
    if sel_prod:
        df_filtered = df_filtered[df_filtered['PRODUTO'].isin(sel_prod)]

    sel_rcr = col03.multiselect(
        'Selecione o RCR',
        placeholder="Selecione os RCRs para filtrar",
        options=sorted(df_filtered['RCR'].str.strip().dropna().unique().tolist()),
        key='sel_rcr',
        help="Selecione os RCRs para filtrar. Como padrão, nenhum RCR está selecionado para permitir a visualização de todas as obras, incluindo aquelas sem RCR atribuído."
    )
    if sel_rcr:
        df_filtered = df_filtered[df_filtered['RCR'].isin(sel_rcr)]

    sel_obra = col02.multiselect(
        "Filtrar por Obra (Sigla)",
        placeholder="Selecione as obras para filtrar",
        options=(
            sorted(
                [
                    o for o in df_filtered['SIGLA'].dropna().unique().tolist()
                    if o in set(data_rdo['obra'].dropna().unique()).union(set(data_pbi['sigla'].dropna().unique()))
                ]
            )
            if any(
                o in set(data_rdo['obra'].dropna().unique()).union(set(data_pbi['sigla'].dropna().unique()))
                for o in df_filtered['SIGLA'].dropna().unique().tolist()
            )
            else sorted(df_filtered['SIGLA'].dropna().unique().tolist())
        ),
        key='sel_obra',
        help="Selecione as obras para filtrar. A lista de obras é filtrada para incluir apenas aquelas que possuem dados relacionados"
    )
    if sel_obra:
        df_filtered = df_filtered[df_filtered['SIGLA'].isin(sel_obra)]

    sel_cid = col04.multiselect(
        'Selecione a Cidade',
        options=sorted(df_filtered['CIDADE'].dropna().unique().tolist()),
        key='sel_cid',
        placeholder="Selecione as cidades para filtrar",
        help="Selecione as cidades para filtrar. A lista de cidades é baseada nos dados disponíveis no conjunto de dados filtrado."
    )
    if sel_cid:
        df_filtered = df_filtered[df_filtered['CIDADE'].isin(sel_cid)]

data_rdo = data_rdo[data_rdo['obra'].isin(df_filtered['SIGLA'].unique())]
dados = data_rdo[['obra', 'date_in']].to_dict(orient='records')

dataset_pbi = data_pbi[data_pbi['sigla'].isin(df_filtered['SIGLA'].unique())]
dados_pbi = dataset_pbi[['sigla', 'data_relatorio']].to_dict(orient='records')

data_gerencial = data_gerencial[data_gerencial['sigla'].isin(df_filtered['SIGLA'].unique())]
# data_gerencial = data_gerencial.drop(columns=['id'], errors='ignore')
data_gerencial[['percentual_desvio', 'curva_base', 'percentual_realizado']] = data_gerencial[['percentual_desvio', 'curva_base', 'percentual_realizado']].apply(pd.to_numeric, errors='coerce') * 100
data_gerencial['data_atualizacao'] = pd.to_datetime(data_gerencial['data_atualizacao'], errors='coerce').dt.strftime('%Y-%m')
data_gerencial['periodo_custo'] = pd.to_datetime(data_gerencial['periodo_custo'], errors='coerce').dt.strftime('%Y-%m')
data_gerencial['periodo_avanco'] = pd.to_datetime(data_gerencial['periodo_avanco'], errors='coerce').dt.strftime('%Y-%m')

with st.expander(label='CENTRO DE GERENCIAMENTO', expanded=True, icon="📊"):
    layout = st.container(horizontal=True, horizontal_alignment='center')
    layout.segmented_control(
        label="Selecione a visualização",
        label_visibility='hidden',
        options=list(COLS_MAP.keys()),
        key='option_view',
        default='Geral'
    )

    option = st.session_state.get('option_view', 'Geral')
    data_gerencial = data_gerencial.merge(data_monday[['SIGLA','FASE', 'RCR', 'AREA','LOCAL','CONSTRUTORA','ARQUITETURA','CLIENTE', 'HUB', 'VISI', 'PBI_RG', 'PBI_RE', 'PBI_RA', 'PBI_RQ']].drop_duplicates(), how='left', left_on='sigla', right_on='SIGLA').drop(columns=['SIGLA'], errors='ignore')
    
    cols_to_show = COLS_MAP.get(option, data_gerencial.columns.tolist())
    df_display = data_gerencial[cols_to_show].copy()
    colunas_para_estilizar = [c for c in ['percentual_desvio', 'atraso_avanco', 'saldo_saving'] if c in cols_to_show]

    df_styled = (
        df_display.style.applymap(style_prediction, subset=colunas_para_estilizar)
        if colunas_para_estilizar
        else df_display
    )
    st.dataframe(df_styled, column_config=COLUMN_CONFIG, use_container_width=True, hide_index=True)

    if option == 'Geral' or option == 'Economias e Savings':
        col01, col02, col03 = st.columns([1, 1, 1])
        col01.metric('ECONOMIA TOTAL', value=f"R$ {data_gerencial['economia_total'].sum():,.2f}", border=True)
        col02.metric('SAVING PAGO', value=f"R$ {data_gerencial['saving_pago_total'].sum():,.2f}", border=True)
        col03.metric('SALDO SAVING', value=f"R$ {data_gerencial['saldo_saving'].sum():,.2f}", border=True)

with st.expander(label='STATUS DAS ATIVIDADES - RDO', expanded=True, icon="📊"):
    with st.container(border=True):
        mes = calen(data=dados, on_clicked_change=lambda: None)

    clicked = (mes.get('clicked') if isinstance(mes, dict) else None) or pd.to_datetime('today').strftime('%m-%Y')
    data_selecionada = pd.to_datetime(clicked, format='%m-%Y')
    col01, col02, col03 = st.columns(3)

    with col01:
        col01.metric('TOTAL OBRAS', value=len(df_filtered['SIGLA'].unique()), border=True)

    with col02:
        mes_period = pd.to_datetime(clicked, format='%m-%Y').to_period('M')
        total_obras_com_atividades = data_rdo[
            pd.to_datetime(data_rdo['date_in']).dt.to_period('M') == mes_period
        ]['obra'].nunique()
        col02.metric('TOTAL ATIVIDADES (MÊS ATUAL)', value=total_obras_com_atividades, border=True)

    with col03:
        col03.metric(
            'PERCENTUAL DE OBRAS COM ATIVIDADES (MÊS ATUAL)',value=f"{(total_obras_com_atividades / len(df_filtered['SIGLA'].unique()) * 100):.2f} %", border=True
        )
with st.expander(label='RELATÓRIO DE GERENCIAL DE OBRAS - POWER BI', expanded=True, icon="📊"):
    with st.container(border=True):
        ano_pbi = calenPBI(data=dados_pbi, on_clicked_change=lambda: None)
    clicked_pbi = (ano_pbi.get('clicked') if isinstance(ano_pbi, dict) else None) or pd.to_datetime('today').strftime('%Y')
    data_selecionada_pbi = pd.to_datetime(clicked_pbi, format='%Y')
    col01, col02, col03 = st.columns(3)
    with col01:
        col01.metric('TOTAL OBRAS', value=len(df_filtered['SIGLA'].unique()), border=True)
    with col02:
        ano_period = pd.to_datetime(clicked_pbi, format='%Y').to_period('Y')
        total_obras_com_relatorio = dataset_pbi[
            pd.to_datetime(dataset_pbi['data_relatorio']).dt.to_period('Y') == ano_period
        ]['sigla'].nunique()
        col02.metric('TOTAL OBRAS COM RELATÓRIO (ANO ATUAL)', value=total_obras_com_relatorio, border=True)
    with col03:
        col03.metric(
            'PERCENTUAL DE OBRAS COM RELATÓRIO (ANO ATUAL)',value=f"{(total_obras_com_relatorio / len(df_filtered['SIGLA'].unique()) * 100):.2f} %", border=True
        )