import streamlit as st
import sys
import os
from datetime import datetime, timedelta

if "logado" not in st.session_state or not st.session_state.logado:
    st.warning("Faça login primeiro")
    st.stop()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from supabase_config import supabase

st.title("⚠️ Alertas Inteligentes")

# manutencoes = supabase.table("manutencoes").select("*").execute().data
# veiculos = supabase.table("veiculos").select("*").execute().data

veiculo_id = st.session_state["veiculo_id"]

manutencoes = supabase.table("manutencoes").select("*").eq("veiculo_id", veiculo_id).execute().data

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
            dias_total = periodo * 30
        else:
            dias_faltando = 0
            dias_total = 1

        # progresso km
        km_usado = km_atual - km_inicial
        progresso_km = min(max(km_usado / intervalo, 0), 1)

        # progresso dias
        dias_usados = dias_total - dias_faltando
        progresso_dias = min(max(dias_usados / dias_total, 0), 1)

        st.subheader(item["tipo_manutencao"])

        st.write(f"🚗 Veículo: {veiculo['nome']}")

        st.metric("KM Atual", f"{km_atual:.0f} km")
        st.metric("Próxima troca", f"{proxima_troca:.0f} km")
        st.metric("Faltam KM", f"{km_faltando:.0f} km")

        st.progress(progresso_km)

        st.metric("Dias restantes", f"{dias_faltando} dias")

        st.progress(progresso_dias)

        # Qual vence primeiro
        percentual_km = km_faltando / intervalo if intervalo > 0 else 0
        percentual_dias = dias_faltando / dias_total if dias_total > 0 else 0

        if percentual_km < percentual_dias:
            st.warning("⚠️ Vence por quilometragem primeiro")
        else:
            st.warning("⚠️ Vence por tempo primeiro")

        # Status geral
        if km_faltando <= 0 or dias_faltando <= 0:
            st.error("❌ Manutenção vencida")
        elif km_faltando < 1000 or dias_faltando < 30:
            st.warning("⚠️ Próximo da troca")
        else:
            st.success("✅ Em dia")

        st.divider()
