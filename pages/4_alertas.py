import streamlit as st
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from supabase_config import supabase

st.title("⚠️ Alertas Inteligentes")

manutencoes = supabase.table("manutencoes").select("*").execute().data
veiculos = supabase.table("veiculos").select("*").execute().data

veiculos_dict = {v["id"]: v for v in veiculos}

hoje = datetime.today().date()

if manutencoes:

    for item in manutencoes:

        veiculo = veiculos_dict.get(item["veiculo_id"])

        if not veiculo:
            continue

        km_atual = float(veiculo["km_atual"] or 0)
        km_inicial = float(item["km_inicial"] or 0)
        intervalo = float(item["intervalo_km"] or 10000)

        proxima_troca = km_inicial + intervalo
        km_faltando = proxima_troca - km_atual

        periodo = int(item["periodo_meses"] or 6)

        data_str = item["data_inicial"]

        if data_str:
            data_inicial = datetime.strptime(data_str, "%Y-%m-%d").date()
            data_limite = data_inicial + timedelta(days=periodo * 30)
            dias_faltando = (data_limite - hoje).days
        else:
            dias_faltando = 0

        st.subheader(item["tipo_manutencao"])

        st.write(f"🚗 Veículo: {veiculo['nome']}")
        st.write(f"KM Atual: {km_atual:.0f} km")
        st.write(f"Próxima troca: {proxima_troca:.0f} km")
        st.write(f"Faltam: {km_faltando:.0f} km")
        st.write(f"Faltam: {dias_faltando} dias")

        if km_faltando <= 0 or dias_faltando <= 0:
            st.error("❌ Manutenção vencida")
        elif km_faltando < 1000:
            st.warning("⚠️ Próximo da troca")
        else:
            st.success("✅ Em dia")

        st.divider()
