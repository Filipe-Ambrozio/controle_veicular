import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Controle Veicular",
    layout="centered"
)

st.title("🚗 Controle Veicular Profissional")

st.markdown("""
### Sistema desenvolvido para:

✅ Controle de veículos  
✅ Histórico de manutenção  
✅ Controle de combustível  
✅ Alertas de troca por KM e tempo  
✅ Organização financeira automotiva  

Permite acompanhar custos, prevenir atrasos de manutenção e manter o veículo em dia.
""")

st.divider()

hoje = datetime.now().strftime("%d/%m/%Y")

st.info(f"📅 Hoje: {hoje}")

st.warning("""
### 💰 Lembrete IPVA
Verifique o calendário do IPVA do seu estado para evitar juros e atraso.
""")