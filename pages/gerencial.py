import pathlib
import pandas as pd
import streamlit as st
import streamlit.components.v2 as stc

from data.monday import get_dataModay
from data.supabase import fetch_data_from_tablefull

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

def style_prediction(v):
    return 'color: #d10000; font-weight: bold;' if v > 0 else ('color: #008000; font-weight: bold;' if v < 0 else 'color: #808080;')

data_rdo = pd.DataFrame(fetch_data_from_tablefull("Bot_Atividade"))
data_pbi = pd.DataFrame(fetch_data_from_tablefull("Powerbi_reports"))
data_gerencial = pd.DataFrame(fetch_data_from_tablefull("Map_PBI"))
data_monday = pd.DataFrame(get_dataModay(926240878))

data_monday['PRODUTO'] = data_monday['PRODUTO'].str.replace('GERENCIAMENTO DE OBRA ', '', regex=False)
data_monday = data_monday[~data_monday['RCR'].isin(['', 'DELETED MEMBER', 'MEMBRO EXCLUÍDO'])]

obras = data_monday['SIGLA'].dropna().unique().tolist()
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
data_gerencial[['desvio_porcentual', 'curva_base', 'realizado_porcentual']] = data_gerencial[['desvio_porcentual', 'curva_base', 'realizado_porcentual']].apply(pd.to_numeric, errors='coerce') * 100
data_gerencial['data_atualizacao'] = pd.to_datetime(data_gerencial['data_atualizacao'], errors='coerce').dt.strftime('%Y-%m')
data_gerencial['periodo_custo'] = pd.to_datetime(data_gerencial['periodo_custo'], errors='coerce').dt.strftime('%Y-%m')
data_gerencial['periodo_avanco'] = pd.to_datetime(data_gerencial['periodo_avanco'], errors='coerce').dt.strftime('%Y-%m')

config = {
    'data_atualizacao': st.column_config.TextColumn('Período'),
    'sigla': st.column_config.TextColumn('Obra (Sigla)'),
    'periodo_custo': st.column_config.TextColumn('Período Custo'),
    'custo_obra': st.column_config.NumberColumn('Custo Obra', format="R$ %.2f"),
    'change_order': st.column_config.NumberColumn('Change Order', format="R$ %.2f"),
    'custo_total': st.column_config.NumberColumn('Custo Total', format="R$ %.2f"),
    'tendencia': st.column_config.NumberColumn('Tendência', format="R$ %.2f"),
    'gasto_competencia_acumulado': st.column_config.NumberColumn('Gasto Acumulado', format="R$ %.2f"),
    'porcentual_consumido': st.column_config.NumberColumn('Consumido %', format='%.2f%%'),

    'desvio_porcentual': st.column_config.NumberColumn('Desvio %', format='%.2f%%'),
    'taxa_paga_acumulada': st.column_config.NumberColumn('Taxa Paga Acumulada', format="R$ %.2f"),
    'taxa_liberada_acumulada': st.column_config.NumberColumn('Taxa Liberada Acumulada', format="R$ %.2f"),
    'curva_base': st.column_config.NumberColumn('Curva Base', format='%.2f%%'),
    'realizado_porcentual': st.column_config.NumberColumn('Realizado %', format='%.2f%%'),
    'atraso_avanco': st.column_config.TextColumn('Atraso Avanço'),
    'contratado_direto': st.column_config.NumberColumn('Contratado Direto', format="R$ %.2f"),
    'contratado_indireto': st.column_config.NumberColumn('Contratado Indireto', format="R$ %.2f"),
    'contratado_total': st.column_config.NumberColumn('Contratado Total', format="R$ %.2f"),
    'economia_total_direto': st.column_config.NumberColumn('Economia Total Direto', format="R$ %.2f"),
    'economia_total_indireto': st.column_config.NumberColumn('Economia Total Indireto', format="R$ %.2f"),
    'economia_total': st.column_config.NumberColumn('Economia Total', format="R$ %.2f"),
    'saving_direto': st.column_config.NumberColumn('Saving Direto', format="R$ %.2f"),
    'saving_indireto': st.column_config.NumberColumn('Saving Indireto', format="R$ %.2f"),
    'saving_total': st.column_config.NumberColumn('Saving Total', format="R$ %.2f"),
    'saving_pago_direto': st.column_config.NumberColumn('Saving Pago Direto', format="R$ %.2f"),
    'saving_pago_indireto': st.column_config.NumberColumn('Saving Pago Indireto', format="R$ %.2f"),
    'saving_pago_total': st.column_config.NumberColumn('Saving Pago Total', format="R$ %.2f"),
    'saldo_saving': st.column_config.NumberColumn('Saldo Saving', format="R$ %.2f"),
    'periodo_avanco': st.column_config.TextColumn('Período Avanço'),
    'HUB': st.column_config.LinkColumn('HUB', display_text="🔗", width=10),
    'VISI': st.column_config.LinkColumn('VISI', display_text="🔗", width=10),
    'PBI_RG': st.column_config.LinkColumn('Rel. Gerencial', display_text="🔗", width=50),
    'PBI_RE': st.column_config.LinkColumn('RDO + Efetivo', display_text="🔗", width=50),
    'PBI_RA': st.column_config.LinkColumn('Apontamentos', display_text="🔗", width=50),
    'PBI_RQ': st.column_config.LinkColumn('Qualidade', display_text="🔗", width=50),
}

with st.expander(label='CENTRO DE GERENCIAMENTO', expanded=True, icon="📊"):
    layout = st.container(horizontal=True, horizontal_alignment='center')
    layout.segmented_control(
        label="Selecione a visualização",
        label_visibility='hidden',
        options=['Geral', 'Financeiro', 'Físico', 'Contratações', 'Economias e Savings', 'Relatórios'],
        key='option_view',
        default='Geral'
    )

    option = st.session_state.get('option_view', 'Geral')
    data_gerencial = data_gerencial.merge(data_monday[['SIGLA', 'HUB', 'VISI', 'PBI_RG', 'PBI_RE', 'PBI_RA', 'PBI_RQ']].drop_duplicates(), how='left', left_on='sigla', right_on='SIGLA').drop(columns=['SIGLA'], errors='ignore')
    
    cols_map = {
        'Geral': ['sigla', 'periodo_custo', 'custo_total', 'desvio_porcentual', 'curva_base', 'realizado_porcentual', 'atraso_avanco', 'contratado_total', 'economia_total', 'saving_total', 'saldo_saving', 'HUB', 'VISI', 'PBI_RG'],
        'Financeiro': ['sigla', 'periodo_custo', 'custo_obra', 'change_order', 'custo_total', 'tendencia', 'desvio_porcentual'],
        'Físico': ['sigla', 'periodo_avanco', 'curva_base', 'realizado_porcentual', 'atraso_avanco'],
        'Contratações': ['sigla', 'contratado_direto', 'contratado_indireto', 'contratado_total'],
        'Economias e Savings': ['sigla', 'economia_total_direto', 'economia_total_indireto', 'economia_total', 'saving_indireto', 'saving_pago_indireto', 'saldo_saving'],
        'Relatórios': ['sigla', 'HUB', 'VISI', 'PBI_RG', 'PBI_RE', 'PBI_RA', 'PBI_RQ']
    }
    
    cols_to_show = cols_map.get(option, data_gerencial.columns.tolist())
    df_display = data_gerencial[cols_to_show].copy()
    colunas_para_estilizar = [c for c in ['desvio_porcentual', 'atraso_avanco', 'saldo_saving'] if c in cols_to_show]

    df_styled = (
        df_display.style.applymap(style_prediction, subset=colunas_para_estilizar)
        if colunas_para_estilizar
        else df_display
    )

    st.dataframe(df_styled, column_config=config, use_container_width=True, hide_index=True)

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