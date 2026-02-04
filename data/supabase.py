from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def get_supabase_client() -> Client:
    url: str = st.secrets['supabase']['url']
    key: str = st.secrets['supabase']['key']
    supabase: Client = create_client(url, key)
    return supabase

@st.cache_data(ttl=5400)
def fetch_data_from_tablefull(table_name: str) -> list[dict]:
    supabase = get_supabase_client()
    results: list[dict] = []
    chunk_size = 1000
    start = 0

    while True:
        end = start + chunk_size - 1
        response = (
            supabase.table(table_name)
            .select('*')
            .order('id', desc=True)
            .range(start, end)
            .execute()
        )
        rows = response.data or []
        if not rows:
            break
        results.extend(rows)
        if len(rows) < chunk_size:
            break
        start += chunk_size

    return results

@st.cache_data(ttl=5400)
def fetch_data_from_table(table_name: str) -> list[dict]:
    supabase = get_supabase_client()
    data = supabase.table(table_name).select('*').order('id', desc=True).execute()
    return data.data