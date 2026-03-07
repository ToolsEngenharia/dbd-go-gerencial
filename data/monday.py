from urllib import response
import streamlit as st
import requests as req

@st.cache_data
def get_dataModay(board):
	api = st.secrets['monday']['apikey']
	url = 'https://api.monday.com/v2'
	query = 'query { boards(ids: '+str(board)+') { items_page (limit:500) { cursor items { id name column_values(ids: [\"status6\", \"dup__of_equipe\", \"produto\", \"location\", \"dup__of_produto\", \"local\", \"numeric_mksm5mps\", \"texto1\", \"texto4\", \"link1\", \"link2\", \"link_mkskfawa\", \"link_mkmw87fc\", \"link_mkmw93z2\"]) { id text  } } } } }'

	headers = {
		'Authorization': api
	}
	response = req.post(url, json={'query': query}, headers=headers)
	return transformar_dados(response.json())

def transformar_dados(input_data):
    try:
        items = input_data['data']['boards'][0]['items_page']['items']
    except (KeyError, IndexError):
        raise ValueError("Formato de dados de entrada inválido.")

    resultado = []

    for item in items:
        def get_column_value(column_id):
            return next((c['text'] for c in item.get('column_values', []) if c['id'] == column_id), '')
        
        def extract_hub(column_id):
            text = get_column_value(column_id)
            return text.split(' - ')[-1] if ' - ' in text else text
        
        novo_item = {
            "SIGLA": item.get('name', '').split('-')[0].strip(),
            "OBRA": item.get('name', ''),
            "FASE": get_column_value('status6'),
            "RCR": ', '.join(
                e.split('@', 1)[0].strip().replace('.', ' ').title()
                    for e in get_column_value('dup__of_equipe').split(',')
                    if e.strip() and e.strip().upper() not in ['DELETED MEMBER', 'MEMBRO EXCLUÍDO']
                ) or None,
            "PRODUTO": get_column_value('produto'),
            "LOCAL": get_column_value('location'),
            "CIDADE": get_column_value('local'),
            "AREA": get_column_value('numeric_mksm5mps'),
            "CONSTRUTORA": get_column_value('texto1'),
            "ARQUITETURA": get_column_value('texto4'),
            "CLIENTE": get_column_value('dup__of_produto'),
            "HUB": extract_hub('link1'),
            "VISI": extract_hub('link2'),
            "PBI_RG": extract_hub('link_mkskfawa'),
            "PBI_RE": extract_hub('link_mkmw87fc'),
            "PBI_RA": extract_hub('link_mkmw93z2'),
            "PBI_RQ": extract_hub('link_mkmw93z2'),
        }
        resultado.append(novo_item)
    resultado = [item for item in resultado if item['PRODUTO'] and 'PROJETO' not in item['PRODUTO'].upper() and 'GESTÃO' not in item['PRODUTO'].upper() and 'Finalizado' not in item['FASE'] and 'Paralisado' not in item['FASE']]
    return resultado

    #selecionar apenas os itens que possuem o produto GERENCIAMENTO RESIDENCIAL e que esta na fase de Fase Obra
    # resultado = [item for item in resultado if item['PRODUTO'] == 'GERENCIAMENTO DE OBRA RESIDENCIAL' and item['FASE'] == 'Fase Obra']