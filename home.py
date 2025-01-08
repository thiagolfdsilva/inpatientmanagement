import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# API endpoint for requests
load_dotenv()
API_ENDPOINT = os.getenv("API_ENDPOINT")  # Replace with your backend URL

# Page title
st.title("Painel de Gerenciamento de Solicitações")

# Function to fetch all requests from the backend
def fetch_requests():
    try:
        response = requests.get(API_ENDPOINT)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro ao buscar solicitações: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Erro ao se conectar à API: {e}")
        return []

# Function to mark a request as completed
def complete_request(index):
    try:
        response = requests.put(f"{API_ENDPOINT}/{index}")
        if response.status_code == 200:
            st.success(f"Solicitação marcada como concluída.")
        else:
            st.error(f"Erro ao atualizar a solicitação: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Erro ao se conectar à API: {e}")

# Fetch and display requests
requests_data = fetch_requests()

if not requests_data:
    st.write("Nenhuma solicitação disponível no momento.")
else:
    # Convert the requests to a DataFrame for display
    df = pd.DataFrame(requests_data)

    # Add an index column to use for actions
    df["Índice"] = df.index

    # Display the DataFrame
    st.write("Solicitações em Aberto:")
    df = df[df["status"] == "Open"]

    st.dataframe(df)


    # Add buttons for each request to mark it as completed
    for idx, request in df.iterrows():
        if st.button(f"Marcar como Concluído - {request['request_id']} (Leito {request['bed_id']})", key=idx):
            complete_request(request["Índice"])
