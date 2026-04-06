import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Tapí RH | Visão Estratégica", layout="wide")

# 2. Estilo visual (Vermelho Tapí e fundo limpo)
st.markdown("""
    <style>
    .main {background-color: #FAFAFA;}
    h1 {color: #8B0000;} 
    </style>
""", unsafe_allow_html=True)

st.title("📊 Gestão de Recrutamento com Dados e Eficiência Operacional")
st.markdown("Monitoramento de Atração & Seleção - Nova Loja")

# 3. DADOS INTEGRADOS (Substituindo a API para funcionar no link externo)
dados_funil = [
    {"etapa": "1. Inscritos", "valor": 150},
    {"etapa": "2. Triagem", "valor": 45},
    {"etapa": "3. Entrevista (Loja)", "valor": 12},
    {"etapa": "4. Aprovados", "valor": 2}
]

dados_fontes = [
    {"fonte": "WhatsApp Local", "candidatos": 80},
    {"fonte": "Instagram Tapí", "candidatos": 45},
    {"fonte": "LinkedIn", "candidatos": 15},
    {"fonte": "Indicação", "candidatos": 10}
]

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
    df_funil = pd.DataFrame(dados_funil)
    fig_funil = px.funnel(df_funil, x='valor', y='etapa', 
                          color_discrete_sequence=['#8B0000'])
    st.plotly_chart(fig_funil, use_container_width=True)

with col_graf2:
    st.subheader("📈 Fonte de Candidatos Eficaz")
    df_fontes = pd.DataFrame(dados_fontes)
    fig_fontes = px.pie(df_fontes, values='candidatos', names='fonte', hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Reds_r)
    st.plotly_chart(fig_fontes, use_container_width=True)

# --- INSIGHTS ---
st.subheader("💡 Insights Estratégicos")
st.info("**O uso de WhatsApp e Instagram gerou maior volume e agilidade no processo seletivo, mostrando aderência ao perfil operacional da vaga e ao público local.
Já o LinkedIn apresentou baixa efetividade, indicando desalinhamento com o perfil buscado.
Estratégia recomendada: priorizar canais orgânicos e locais para otimizar tempo e custo de contratação.")
