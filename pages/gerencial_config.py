import streamlit as st

COLUMN_CONFIG = {
    'data_atualizacao': st.column_config.TextColumn('Período'),
    'sigla': st.column_config.TextColumn('Obra (Sigla)'),
    'periodo_custo': st.column_config.TextColumn('Período Custo'),
    'custo_obra': st.column_config.TextColumn('Custo Obra'),
    'change_order': st.column_config.TextColumn('Change Order'),
    'custo_total': st.column_config.TextColumn('Custo Total'),
    'tendencia': st.column_config.TextColumn('Tendência'),
    'gasto_competencia_acumulado': st.column_config.TextColumn('Gasto Acumulado'),
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
    'desvio': st.column_config.TextColumn('Desvio'),
    'percentual_desvio': st.column_config.NumberColumn('Desvio %', format='%.2f%%'),
    'taxa': st.column_config.TextColumn('Taxa'),
    'taxa_paga_acumulada': st.column_config.TextColumn('Taxa Paga Acumulada'),
    'taxa_liberada_acumulada': st.column_config.TextColumn('Taxa Liberada Acumulada'),
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
    'contratado_direto': st.column_config.TextColumn('Contratado Direto'),
    'contratado_indireto': st.column_config.TextColumn('Contratado Indireto'),
    'contratado_total': st.column_config.TextColumn('Contratado Total'),
    'economia_total_direto': st.column_config.TextColumn('Economia Total Direto'),
    'economia_total_indireto': st.column_config.TextColumn('Economia Total Indireto'),
    'economia_total': st.column_config.TextColumn('Economia Total'),
    'saving_direto': st.column_config.TextColumn('Saving Direto'),
    'saving_indireto': st.column_config.TextColumn('Saving Indireto'),
    'saving_total': st.column_config.TextColumn('Saving Total'),
    'saving_pago_direto': st.column_config.TextColumn('Saving Pago Direto'),
    'saving_pago_indireto': st.column_config.TextColumn('Saving Pago Indireto'),
    'saving_pago_total': st.column_config.TextColumn('Saving Pago Total'),
    'saldo_saving': st.column_config.TextColumn('Saldo Saving'),
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

COLUNAS_MONETARIAS = [
    'custo_obra', 'change_order', 'custo_total', 'tendencia',
    'gasto_competencia_acumulado', 'desvio', 'taxa', 'taxa_paga_acumulada',
    'taxa_liberada_acumulada', 'contratado_direto', 'contratado_indireto',
    'contratado_total', 'economia_total_direto', 'economia_total_indireto',
    'economia_total', 'saving_direto', 'saving_indireto', 'saving_total',
    'saving_pago_direto', 'saving_pago_indireto', 'saving_pago_total', 'saldo_saving',
]

def fmt_brl(v):
    try:
        return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (TypeError, ValueError):
        return v

def style_prediction(v):
    return 'color: #d10000; font-weight: bold;' if v > 0 else ('color: #008000; font-weight: bold;' if v < 0 else 'color: #808080;')