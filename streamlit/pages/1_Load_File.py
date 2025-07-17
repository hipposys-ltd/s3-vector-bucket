import streamlit as st
import requests

with st.form("user_form"):
    files = st.file_uploader("Upload File",
                            accept_multiple_files=True,
                            type=['pdf'])
    submitted = st.form_submit_button("Upload the file")

if submitted:
    if files:
        for file in files:
            url = 'http://fastapi:8080/embeddings/upload_file/'
            response = requests.post(
                    url,
                    files={'file': file}
                    )
            if response.status_code == 200:
                st.write(f'The file has been successfully uploaded. {file.name}')
    else:
        st.warning("Please upload file before submitting.")
