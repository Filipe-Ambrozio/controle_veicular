import streamlit as st
from supabase_config import supabase
import pandas as pd

st.title("⛽ Combustível")

veiculos = supabase.table("veiculos").select("*").execute().data
lista = [v["nome"] for v in veiculos]

veiculo = st.selectbox("Veículo", lista)

tipo = st.selectbox("Tipo combustível", [
    "Gasolina",
    "Diesel",
    "Etanol",
    "Gasolina aditivada"
])

litros = st.number_input("Litros")
valor = st.number_input("Valor")
data = st.date_input("Data")
km = st.number_input("Quilometragem")

if st.button("Salvar combustível"):

    id_veiculo = [v["id"] for v in veiculos if v["nome"] == veiculo][0]

    supabase.table("combustivel").insert({
        "veiculo_id": id_veiculo,
        "tipo_combustivel": tipo,
        "litros": litros,
        "valor": valor,
        "data": str(data),
        "quilometragem": km
    }).execute()

    st.success("Registro salvo")

dados = supabase.table("combustivel").select("*").execute().data

if dados:
    st.dataframe(pd.DataFrame(dados))
    
    
st.subheader("Excluir combustível")

if dados:
    ids = [d["id"] for d in dados]

    excluir = st.selectbox("ID Combustível", ids)

    if st.button("Apagar"):
        supabase.table("combustivel").delete().eq("id", excluir).execute()
        st.success("Registro apagado")