import streamlit as st
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from supabase_config import supabase

st.title("⚠️ Alertas")

manutencoes = supabase.table("manutencoes").select("*").execute().data
veiculos = supabase.table("veiculos").select("*").execute().data

veiculos_dict = {v["id"]: v for v in veiculos}

hoje = datetime.today().date()

for item in manutencoes:

    veiculo = veiculos_dict.get(item["veiculo_id"])

    km_atual = veiculo["km_atual"]

    km_inicial = item["km_inicial"]
    intervalo = item["intervalo_km"]

    proxima_troca = km_inicial + intervalo
    km_faltando = proxima_troca - km_atual

    data_inicial = datetime.strptime(item["data_inicial"], "%Y-%m-%d").date()
    periodo = item["periodo_meses"]

    data_limite = data_inicial + timedelta(days=periodo*30)
    dias_faltando = (data_limite - hoje).days

    st.subheader(item["tipo_manutencao"])

    st.write(f"🚗 Veículo: {veiculo['nome']}")
    st.write(f"KM Atual: {km_atual}")
    st.write(f"Faltam: {km_faltando:.0f} km")
    st.write(f"Faltam: {dias_faltando} dias")

    if km_faltando <= 0 or dias_faltando <= 0:
        st.error("Manutenção vencida")

    st.divider()
