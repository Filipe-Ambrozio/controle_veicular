import streamlit as st
from supabase_config import supabase
from datetime import datetime

st.set_page_config(
    page_title="Controle Veicular",
    layout="centered"
)

# Inicializar sessão
if "logado" not in st.session_state:
    st.session_state.logado = False

if "veiculo_id" not in st.session_state:
    st.session_state.veiculo_id = None

if "veiculo_nome" not in st.session_state:
    st.session_state.veiculo_nome = None


# LOGIN
if not st.session_state.logado:

    st.title("🔐 Login Veicular")

    veiculos = supabase.table("veiculos").select("*").execute().data

    lista = [v["nome"] for v in veiculos]

    veiculo = st.selectbox("Veículo", lista)
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        usuario = [
            v for v in veiculos
            if v["nome"] == veiculo and str(v["senha"]) == str(senha)
        ]

        if usuario:
            st.session_state.logado = True
            st.session_state.veiculo_id = usuario[0]["id"]
            st.session_state.veiculo_nome = usuario[0]["nome"]
            st.rerun()
        else:
            st.error("Senha incorreta")


# SISTEMA
else:

    st.title("🚗 Controle Veicular")
    
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

    # hoje = datetime.now().strftime("%d/%m/%Y")

    st.success(f"Veículo: {st.session_state.veiculo_nome}")
    # st.write(f"📅 Data: {hoje}")
    # st.warning("💰 Lembrete IPVA")

    if st.button("Sair"):
        st.session_state.logado = False
        st.session_state.veiculo_id = None
        st.session_state.veiculo_nome = None
        st.rerun()
