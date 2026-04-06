# app_dashboard.py
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Tapí RH | Visão Estratégica", layout="wide")

# Estilo visual limpo e moderno (premium)
st.markdown("""
    <style>
    .main {background-color: #FAFAFA;}
    h1 {color: #8B0000;} /* Vermelho Tapí */
    </style>
""", unsafe_allow_html=True)

st.title("📊 Tapí RH Case: Processos e Soluções")
st.markdown("Monitoramento de Atração & Seleção - Nova Loja")

# Função para consumir a API
@st.cache_data
def carregar_dados(endpoint):
    try:
        response = requests.get(f"http://localhost:8000/api/{endpoint}")
        return response.json()["dados"]
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
        return []

# --- CARREGANDO DADOS DA API ---
dados_funil = carregar_dados("funil")
dados_fontes = carregar_dados("fontes")

# --- CONSTRUÇÃO DOS INDICADORES (KPIs) ---
col1, col2, col3 = st.columns(3)
col1.metric("Vagas Abertas", "2", "Atendentes")
col2.metric("SLA Atual (Time to Fill)", "8 dias", "-2 dias da meta", delta_color="inverse")
col3.metric("Custo por Contratação", "R$ 0,00", "Foco em tráfego orgânico/social")

st.divider()

# --- GRÁFICOS ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("🎯 Funil de Contratação em Tempo Real")
    if dados_funil:
        df_funil = pd.DataFrame(dados_funil)
        fig_funil = px.funnel(df_funil, x='valor', y='etapa', 
                              color_discrete_sequence=['#8B0000'])
        st.plotly_chart(fig_funil, use_container_width=True)

with col_graf2:
    st.subheader("📈 Fonte de Candidatos Eficaz")
    if dados_fontes:
        df_fontes = pd.DataFrame(dados_fontes)
        fig_fontes = px.pie(df_fontes, values='candidatos', names='fonte', hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_fontes, use_container_width=True)

# --- INSIGHTS ---
st.subheader("💡 Insights Estratégicos")
st.info("**Análise de Conversão:** O recrutamento via WhatsApp e Instagram trouxe volume e agilidade, validando a tese de que o público da nova loja já consome a marca localmente. O LinkedIn trouxe candidatos com perfil mais administrativo, fora do escopo 'mão na massa' exigido para o salão.")