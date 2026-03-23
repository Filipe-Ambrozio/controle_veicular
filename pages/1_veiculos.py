import streamlit as st
from supabase_config import supabase
import pandas as pd

st.title("🚗 Cadastro de Veículos")

dados = supabase.table("veiculos").select("*").execute().data

if len(dados) >= 5:
    st.warning("Máximo de 5 veículos permitido")

nome = st.text_input("Nome")
marca = st.text_input("Marca")
modelo = st.text_input("Modelo")
placa = st.text_input("Placa")
cor = st.text_input("Cor")

if st.button("Salvar Veículo"):
    if len(dados) < 5:
        supabase.table("veiculos").insert({
            "nome": nome,
            "marca": marca,
            "modelo": modelo,
            "placa": placa,
            "cor": cor
        }).execute()
        st.success("Veículo salvo")

if dados:
    st.dataframe(pd.DataFrame(dados))
    
    
st.subheader("Excluir Veículo")

if dados:
    ids = [v["id"] for v in dados]

    excluir = st.selectbox("ID veículo", ids)

    if st.button("Excluir veículo"):
        supabase.table("veiculos").delete().eq("id", excluir).execute()
        st.success("Veículo removido")