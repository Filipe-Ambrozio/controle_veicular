import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from supabase_config import supabase

st.title("⚠️ Alertas Inteligentes")

dados = supabase.table("manutencoes").select("*").execute().data

if dados:

    hoje = datetime.today().date()

    for item in dados:

        km_inicial = item["km_inicial"] if item["km_inicial"] else 0
        km_atual = item["km_atual"] if item["km_atual"] else 0
        intervalo = item["intervalo_km"] if item["intervalo_km"] else 10000

        proxima_troca = km_inicial + intervalo
        km_faltando = proxima_troca - km_atual

        data_inicial = datetime.strptime(item["data_inicial"], "%Y-%m-%d").date()
        periodo = item["periodo_meses"] if item["periodo_meses"] else 6

        dias_total = periodo * 30
        data_limite = data_inicial + timedelta(days=dias_total)

        dias_faltando = (data_limite - hoje).days

        st.subheader(item["tipo_manutencao"])

        st.metric("KM Atual", f"{km_atual:.0f} km")
        st.metric("Próxima troca", f"{proxima_troca:.0f} km")
        st.metric("Faltam KM", f"{km_faltando:.0f} km")

        st.metric("Dias restantes", f"{dias_faltando} dias")

        if km_faltando <= 0 or dias_faltando <= 0:
            st.error("❌ Manutenção vencida")
        else:
            if km_faltando < 1000:
                st.warning("⚠️ Próximo da troca")

        st.divider()
