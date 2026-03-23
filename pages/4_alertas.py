import streamlit as st
from supabase_config import supabase
from datetime import datetime
import pandas as pd

st.title("⚠️ Alertas")

dados = supabase.table("manutencoes").select("*").execute().data

if dados:

    for item in dados:

        intervalo = item["intervalo_km"] if item["intervalo_km"] else 10000
        km_faltando = (item["km_inicial"] + intervalo) - item["km_atual"]

        st.subheader(item["tipo_manutencao"])

        if km_faltando <= 0:
            st.error("Manutenção vencida")
        else:
            st.warning(f"Faltam {km_faltando:.0f} km")

        st.write(f"KM Atual: {item['km_atual']}")