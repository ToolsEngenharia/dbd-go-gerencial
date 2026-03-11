import streamlit as st

COLUMN_CONFIG = {
    'data_atualizacao': st.column_config.TextColumn('Período'),
    'sigla': st.column_config.TextColumn('Obra (Sigla)'),
    'periodo_custo': st.column_config.TextColumn('Período Custo'),
    'custo_obra': st.column_config.NumberColumn('Custo Obra', format="R$ %.2f"),
    'change_order': st.column_config.NumberColumn('Change Order', format="R$ %.2f"),
    'custo_total': st.column_config.NumberColumn('Custo Total', format="R$ %.2f"),
    'tendencia': st.column_config.NumberColumn('Tendência', format="R$ %.2f"),
    'gasto_competencia_acumulado': st.column_config.NumberColumn('Gasto Acumulado', format="R$ %.2f"),
    'percentual_consumido': st.column_config.NumberColumn('Consumido %', format='%.2f%%'),
    'percentual_contratado': st.column_config.ProgressColumn(
        'Contratado %', format='%.2f%%',
        help="Percentual de valor contratado em relação ao custo total.",
        max_value=100
    ),
    'percentual_remunerado': st.column_config.ProgressColumn(
        'Remuneração %', format='%.2f%%',
        help="Percentual de remuneração em relação ao custo total.",
        width=100,
        max_value=100
    ),
    'percentual_economia': st.column_config.NumberColumn('Economia %', format='%.2f%%'),
    'desvio': st.column_config.NumberColumn('Desvio', format="R$ %.2f"),
    'percentual_desvio': st.column_config.NumberColumn('Desvio %', format='%.2f%%'),
    'taxa': st.column_config.NumberColumn('Taxa', format="R$ %.2f"),
    'taxa_paga_acumulada': st.column_config.NumberColumn('Taxa Paga Acumulada', format="R$ %.2f"),
    'taxa_liberada_acumulada': st.column_config.NumberColumn('Taxa Liberada Acumulada', format="R$ %.2f"),
    'curva_base': st.column_config.ProgressColumn(
        'Curva Base', format='%.2f%%',
        help="Percentual de avanço físico previsto na curva base para o período.",
        width=100,
        max_value=100
    ),
    'percentual_realizado': st.column_config.ProgressColumn(
        'Realizado %', format='%.2f%%',
        help="Percentual de avanço físico em relação à curva base.",
        max_value=100,
        width=100
    ),
    'data_termino_previsto': st.column_config.DateColumn('Término Previsto'),
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
    'HUB': st.column_config.LinkColumn('HUB', display_text="🔗", width=20),
    'VISI': st.column_config.LinkColumn('VISI', display_text="🔗", width=20),
    'PBI_RG': st.column_config.LinkColumn('Rel. Gerencial', display_text="🔗", width=50),
    'PBI_RE': st.column_config.LinkColumn('RDO + Efetivo', display_text="🔗", width=50),
    'PBI_RA': st.column_config.LinkColumn('Apontamentos', display_text="🔗", width=50),
    'PBI_RQ': st.column_config.LinkColumn('Qualidade', display_text="🔗", width=50),
}

COLS_MAP = {
    'Geral': [
        'sigla', 'tendencia', 'percentual_desvio', 'percentual_consumido',
        'percentual_contratado', 'curva_base', 'data_termino_previsto', 'percentual_realizado',
        'percentual_remunerado', 'atraso_avanco', 'contratado_total',
        'economia_total', 'saving_total', 'saldo_saving', 'HUB', 'VISI', 'PBI_RG'
    ],
    'Financeiro': [
        'sigla', 'periodo_custo', 'custo_obra', 'change_order',
        'custo_total', 'tendencia', 'desvio', 'percentual_desvio'
    ],
    'Renumeração': ['sigla', 'taxa', 'taxa_liberada_acumulada', 'taxa_paga_acumulada', 'percentual_remunerado'],
    'Físico': ['sigla', 'periodo_avanco', 'curva_base', 'data_termino_previsto', 'percentual_realizado', 'atraso_avanco'],
    'Contratações': [
        'sigla', 'contratado_direto', 'contratado_indireto',
        'contratado_total', 'percentual_contratado', 'economia_total'
    ],
    'Informações Adicionais': ['sigla', 'RCR', 'FASE', 'AREA', 'LOCAL', 'CONSTRUTORA', 'ARQUITETURA', 'CLIENTE'],
    'Relatórios': ['sigla', 'HUB', 'VISI', 'PBI_RG', 'PBI_RE', 'PBI_RA', 'PBI_RQ'],
}

def style_prediction(v):
    return 'color: #d10000; font-weight: bold;' if v > 0 else ('color: #008000; font-weight: bold;' if v < 0 else 'color: #808080;')