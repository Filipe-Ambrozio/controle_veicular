import streamlit as st
from supabase_config import supabase
from datetime import date
import pandas as pd

if "logado" not in st.session_state or not st.session_state.logado:
    st.warning("Faça login primeiro")
    st.stop()

st.title("🔧 Manutenção")

tipos = [
    "Manutenção periódica",
    "Mudança de pneus",
    "Óleo com Filtro",
    "Filtro de ar do motor",
    "Filtro de cabine",
    "Pastilha de freio",
    "Disco e pastilha de freio",
    "Fluido de freio",
    "Velas de ignição",
    "Limpadores",
    "Rodas",
    "Motor",
    "Suspensão",
    "Caixa de cambio",
    "Caixa de velocidade",
    "Fluido",
    "Filtro de combustivel",
    "Correia dentada",
    "Correia de acessórios",
    "Anticongelante",
    "Lava-jato",
    "Conserto de pneus",
    "Elétrica",
    "Reparação de corpo",
    "Evacuação",
    "Atualização de quilometragem",
    "Lampadas Dianteira",
    "Lampada traseira",
    "Bateria",
    "Outro serviço"
]

veiculos = supabase.table("veiculos").select("*").execute().data

lista = [v["nome"] for v in veiculos]

veiculo_id = st.session_state["veiculo_id"]
tipo = st.selectbox("Tipo de manutenção", tipos)


km_inicial = st.number_input("Quilometragem inicial")
data_inicial = st.date_input("Data inicial")
periodo = st.number_input("Periodo em meses", value=6)
valor = st.number_input("Valor")
intervalo_km = st.number_input("intervalo_km", value=60079.00)
km_atual = st.number_input("KM Atual", value=60079.0)

if st.button("Salvar manutenção"):

    id_veiculo = st.session_state.veiculo_id

    supabase.table("manutencoes").insert({
        "veiculo_id": veiculo_id,
        "tipo_manutencao": tipo,
        "km_atual": km_atual,
        "km_inicial": km_inicial,
        "data_inicial": str(data_inicial),
        "periodo_meses": periodo,
        "valor": valor,
        "intervalo_km": intervalo_km
    }).execute()

    st.success("Manutenção salva")

dados = supabase.table("manutencoes").select("*").execute().data

if dados:
    st.dataframe(pd.DataFrame(dados))
    
intervalo_km = st.number_input(
    "Próxima troca em quantos KM?",
    value=8000
)

st.subheader("Excluir manutenção")

if dados:
    ids = [d["id"] for d in dados]

    excluir = st.selectbox("Selecione ID", ids)

    if st.button("Apagar Registro"):
        supabase.table("manutencoes").delete().eq("id", excluir).execute()
        st.success("Registro apagado")
