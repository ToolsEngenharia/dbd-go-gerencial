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
        novo_item = {
			"SIGLA": item.get('name', '').split('-')[0].strip(),
            "OBRA": item.get('name', ''),
            "FASE": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'status6'), ''),
            "RCR": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'dup__of_equipe'), ''),
            "PRODUTO": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'produto'), ''),
            "LOCAL": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'location'), ''),
            "CIDADE": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'local'), ''),
            "AREA": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'numeric_mksm5mps'), ''),
            "CONSTRUTORA": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'texto1'), ''),
            "ARQUITETURA": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'texto4'), ''),
            "CLIENTE": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'dup__of_produto'), ''),
            "HUB": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'link1'), ''),
            "VISI": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'link2'), ''),
            "PBI_RG": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'link_mkskfawa'), ''),
            "PBI_RE": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'link_mkmw87fc'), ''),
            "PBI_RA": next((c['text'] for c in item.get('column_values', []) if c['id'] == 'link_mkmw93z2'), ''),
        }
        resultado.append(novo_item)
    resultado = [item for item in resultado if item['PRODUTO'] and 'PROJETO' not in item['PRODUTO'].upper() and 'GESTÃO' not in item['PRODUTO'].upper()]
    return resultado

    #selecionar apenas os itens que possuem o produto GERENCIAMENTO RESIDENCIAL e que esta na fase de Fase Obra
    # resultado = [item for item in resultado if item['PRODUTO'] == 'GERENCIAMENTO DE OBRA RESIDENCIAL' and item['FASE'] == 'Fase Obra']