import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# =====================================================================
# 1. DATA GENERATOR
# =====================================================================
def generate_mock_data(num_records=150):
    np.random.seed(42)
    random.seed(42)

    processos = [
        "Onboarding de Usuários", "Deploy de Aplicação", "Resolução de Incidentes N1",
        "Gestão de Mudanças", "Backup e Restore", "Provisionamento de Infra", 
        "Auditoria de Acessos", "Fechamento Financeiro", "Processamento de Folha"
    ]
    areas = ["TI - Infraestrutura", "TI - Suporte", "Operações", "Segurança da Informação", "Desenvolvimento", "RH"]
    gargalos = ["Aprovação manual", "Sistema legado lento", "Falta de automação", "Dependência de terceiros", "Dados incompletos", "Retrabalho"]
    tipos_melhoria = ["Automação RPA", "Refatoração de Código", "Novo Sistema", "Treinamento", "Revisão de Processo"]
    status_melhoria = ["Concluído", "Em Andamento", "Backlog", "Cancelado"]
    status_processo = ["Normal", "Em análise", "Em melhoria", "Crítico"]
    responsaveis = ["Ana Silva", "Carlos Souza", "Mariana Santos", "João Pedro", "Fernanda Lima"]

    data = []
    base_date = datetime.now() - timedelta(days=180)

    for i in range(1, num_records + 1):
        start_date = base_date + timedelta(days=random.randint(0, 150))
        end_date = start_date + timedelta(days=random.randint(5, 45)) if random.choice([True, False]) else pd.NaT

        status_m = random.choice(status_melhoria)
        if status_m == "Concluído" and pd.isna(end_date):
            end_date = start_date + timedelta(days=random.randint(5, 30))
        elif status_m in ["Em Andamento", "Backlog"]:
            end_date = pd.NaT

        data.append({
            "ID da Melhoria": f"IMP-{str(i).zfill(3)}",
            "Processo": random.choice(processos),
            "Área responsável": random.choice(areas),
            "Tempo de Execução (h)": round(random.uniform(2.0, 48.0), 1),
            "Gargalo identificado": random.choice(gargalos),
            "Tipo de melhoria": random.choice(tipos_melhoria),
            "Status da melhoria": status_m,
            "Status do Processo": random.choice(status_processo),
            "Responsável": random.choice(responsaveis),
            "Data de início": start_date,
            "Data de conclusão": end_date,
            "Impacto estimado (%)": round(random.uniform(5.0, 45.0), 1)
        })

    df = pd.DataFrame(data)
    df['Mês de Conclusão'] = df['Data de conclusão'].dt.strftime('%Y-%m')
    return df

df_main = generate_mock_data()

# =====================================================================
# 2. CHARTS
# =====================================================================
COLORS = {
    "Normal": "#2ecc71",
    "Em análise": "#f1c40f",
    "Em melhoria": "#3498db",
    "Crítico": "#e74c3c",
    "Concluído": "#2ecc71",
    "Em Andamento": "#f39c12",
    "Backlog": "#95a5a6",
    "Cancelado": "#c0392b"
}

def create_status_pie(df):
    if df.empty: return go.Figure()
    status_counts = df['Status do Processo'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Contagem']
    fig = px.pie(status_counts, names='Status', values='Contagem', hole=0.4,
                 color='Status', color_discrete_map=COLORS,
                 title="Processos por Status")
    return fig

def create_time_bar(df):
    if df.empty: return go.Figure()
    time_df = df.groupby('Processo')['Tempo de Execução (h)'].mean().reset_index().sort_values(by='Tempo de Execução (h)', ascending=True)
    fig = px.bar(time_df, x='Tempo de Execução (h)', y='Processo', orientation='h',
                 title="Tempo Médio de Execução (Horas)", color_discrete_sequence=['#2c3e50'])
    return fig

def create_bottleneck_dist(df):
    if df.empty: return go.Figure()
    gargalos_counts = df['Gargalo identificado'].value_counts().reset_index()
    gargalos_counts.columns = ['Gargalo', 'Contagem']
    fig = px.bar(gargalos_counts, x='Gargalo', y='Contagem',
                 title="Distribuição de Gargalos", color='Contagem', color_continuous_scale='Reds')
    return fig

def create_improvements_timeline(df):
    df_concluido = df.dropna(subset=['Mês de Conclusão'])
    if df_concluido.empty: return go.Figure()
    timeline_df = df_concluido.groupby('Mês de Conclusão').size().reset_index(name='Melhorias Implementadas')
    timeline_df = timeline_df.sort_values('Mês de Conclusão')
    fig = px.line(timeline_df, x='Mês de Conclusão', y='Melhorias Implementadas', markers=True,
                  title="Melhorias Implementadas por Mês", line_shape='spline')
    return fig

def create_impact_scatter(df):
    if df.empty: return go.Figure()
    fig = px.scatter(df, x='Tempo de Execução (h)', y='Impacto estimado (%)', 
                     color='Status da melhoria', color_discrete_map=COLORS,
                     hover_data=['Processo', 'Gargalo identificado'],
                     title="Impacto das Melhorias vs Tempo Atual", size_max=15)
    return fig

# =====================================================================
# 3. STREAMLIT APP
# =====================================================================
st.title("Process Improvement & Operations Dashboard")

# Filtros
area = st.multiselect("Área Responsável", df_main['Área responsável'].unique())
processo = st.multiselect("Processo", df_main['Processo'].unique())
status = st.multiselect("Status da Melhoria", df_main['Status da melhoria'].unique())

# Filtragem
dff = df_main.copy()
if area: dff = dff[dff['Área responsável'].isin(area)]
if processo: dff = dff[dff['Processo'].isin(processo)]
if status: dff = dff[dff['Status da melhoria'].isin(status)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Processos Monitorados", dff['Processo'].nunique())
col2.metric("Gargalos Críticos", len(dff[dff['Status do Processo']=="Crítico"]))
col3.metric("Melhorias Concluídas", len(dff[dff['Status da melhoria']=="Concluído"]))

col4, col5, col6 = st.columns(3)
col4.metric("Melhorias em Andamento", len(dff[dff['Status da melhoria']=="Em Andamento"]))
media_reducao = dff['Impacto estimado (%)'].mean()
col5.metric("Redução Média de Tempo", f"{media_reducao:.1f}%" if pd.notna(media_reducao) else "0%")
total_valid = len(dff)
if total_valid > 0:
    eff = (len(dff[dff['Status do Processo'].isin(['Normal','Em melhoria'])]) / total_valid) * 100
    col6.metric("Eficiência Operacional", f"{eff:.1f}%")
else:
    col6.metric("Eficiência Operacional", "N/A")

# Gráficos
st.plotly_chart(create_status_pie(dff), use_container_width=True)
st.plotly_chart(create_time_bar(dff), use_container_width=True)
st.plotly_chart(create_bottleneck_dist(dff), use_container_width=True)
st.plotly_chart(create_improvements_timeline(dff), use_container_width=True)
st.plotly_chart(create_impact_scatter(dff), use_container_width=True)

# Tabela
st.subheader("Backlog e Histórico de Melhorias")
st.dataframe(dff[['ID da Melhoria','Processo','Área responsável','Gargalo identificado',
                  'Tipo de melhoria','Status da melhoria','Responsável','Impacto estimado (%)']])
