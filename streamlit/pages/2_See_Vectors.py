import requests
import os
import pandas as pd
import streamlit as st


def del_vectors(vectors_to_delete_list):
    """Delete vectors from the API."""
    url = "http://fastapi:8080/embeddings/delete_vectors/"
    response = requests.delete(
        url,
        headers={"x-access-token": os.environ.get('FAST_API_ACCESS_SECRET_TOKEN')},
        json={'vectors_to_delete': vectors_to_delete_list}
    )
    response.raise_for_status()
    st.write(f'{vectors_to_delete_list} are deleted')


def get_vectors_df():
    """Fetch vectors from API and return as DataFrame."""
    url = "http://fastapi:8080/embeddings/list_vectors/"
    response = requests.get(
        url,
        headers={"x-access-token": os.environ.get('FAST_API_ACCESS_SECRET_TOKEN')}
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())


# Initialize dataframe in session state
if "df" not in st.session_state:
    st.session_state['df'] = get_vectors_df()

# Display dataframe with selection
vectors_to_delete = st.dataframe(
    st.session_state['df'],
    on_select="rerun",
    key="key",
    selection_mode=["multi-row"],
    hide_index=True
)

# Only show buttons if there are vectors
if len(st.session_state['df']) > 0:
    selected_rows = vectors_to_delete.selection['rows']
    
    # Get selected vector keys
    vectors_to_delete_list = list(st.session_state['df'].iloc[selected_rows]['key'])
    
    # Delete selected vectors button
    if st.button(f'Vectors to delete: {vectors_to_delete_list}'):
        del_vectors(vectors_to_delete_list)
    
    # Get unique source names from selected rows
    sources_to_delete = list(set(st.session_state['df'].iloc[selected_rows]['source_name']))
    
    # Delete by source button
    if st.button(f'Sources to delete: {sources_to_delete}'):
        vectors_by_source = list(
            st.session_state['df'][st.session_state['df']['source_name'].isin(sources_to_delete)]['key']
        )
        del_vectors(vectors_by_source)

    if st.button('Delete all the vectors'):
        vectors_by_source = list(
            st.session_state['df']['key']
        )
        del_vectors(vectors_by_source)
