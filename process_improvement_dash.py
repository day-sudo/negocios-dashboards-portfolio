import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go

# =====================================================================
# 1. DATA GENERATOR (Equivalente ao data_generator.py)
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

# Inicializa o dataset
df_main = generate_mock_data()

# =====================================================================
# 2. CHARTS (Equivalente ao charts.py)
# =====================================================================
# Paleta de cores corporativa
COLORS = {
    "Normal": "#2ecc71",       # Verde
    "Em análise": "#f1c40f",   # Amarelo
    "Em melhoria": "#3498db",  # Azul
    "Crítico": "#e74c3c",      # Vermelho
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
                 title="1. Processos por Status")
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def create_time_bar(df):
    if df.empty: return go.Figure()
    time_df = df.groupby('Processo')['Tempo de Execução (h)'].mean().reset_index().sort_values(by='Tempo de Execução (h)', ascending=True)
    fig = px.bar(time_df, x='Tempo de Execução (h)', y='Processo', orientation='h',
                 title="2. Tempo Médio de Execução (Horas)", color_discrete_sequence=['#2c3e50'])
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def create_bottleneck_dist(df):
    if df.empty: return go.Figure()
    gargalos_counts = df['Gargalo identificado'].value_counts().reset_index()
    gargalos_counts.columns = ['Gargalo', 'Contagem']
    fig = px.bar(gargalos_counts, x='Gargalo', y='Contagem',
                 title="3. Distribuição de Gargalos", color='Contagem', color_continuous_scale='Reds')
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    return fig

def create_improvements_timeline(df):
    df_concluido = df.dropna(subset=['Mês de Conclusão'])
    if df_concluido.empty: return go.Figure()
    timeline_df = df_concluido.groupby('Mês de Conclusão').size().reset_index(name='Melhorias Implementadas')
    timeline_df = timeline_df.sort_values('Mês de Conclusão')
    fig = px.line(timeline_df, x='Mês de Conclusão', y='Melhorias Implementadas', markers=True,
                  title="4. Melhorias Implementadas por Mês", line_shape='spline')
    fig.update_traces(line=dict(color='#27ae60', width=3), marker=dict(size=8, color='#2c3e50'))
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def create_impact_scatter(df):
    if df.empty: return go.Figure()
    fig = px.scatter(df, x='Tempo de Execução (h)', y='Impacto estimado (%)', 
                     color='Status da melhoria', color_discrete_map=COLORS,
                     hover_data=['Processo', 'Gargalo identificado'],
                     title="5. Impacto das Melhorias vs Tempo Atual", size_max=15)
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# =====================================================================
# 3. TABLES (Equivalente ao tables.py)
# =====================================================================
def create_data_table(df):
    display_cols = ['ID da Melhoria', 'Processo', 'Área responsável', 'Gargalo identificado', 
                    'Tipo de melhoria', 'Status da melhoria', 'Responsável', 'Impacto estimado (%)']
    return dash_table.DataTable(
        id='improvements-table',
        columns=[{"name": i, "id": i} for i in display_cols],
        data=df.to_dict('records'),
        page_size=10,
        sort_action="native",
        filter_action="native",
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Segoe UI, Helvetica, Arial, sans-serif'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'},
            {'if': {'filter_query': '{Status da melhoria} = "Concluído"', 'column_id': 'Status da melhoria'}, 'color': '#27ae60', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{Status da melhoria} = "Em Andamento"', 'column_id': 'Status da melhoria'}, 'color': '#f39c12', 'fontWeight': 'bold'},
            {'if': {'filter_query': '{Status da melhoria} = "Cancelado"', 'column_id': 'Status da melhoria'}, 'color': '#c0392b', 'fontWeight': 'bold'}
        ],
        style_table={'overflowX': 'auto'}
    )

# =====================================================================
# 4. LAYOUT (Equivalente ao layout.py)
# =====================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

# Estilos CSS embutidos para garantir a renderização no ambiente
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "16rem",
    "padding": "2rem 1rem", "backgroundColor": "#2c3e50", "color": "white"
}

CONTENT_STYLE = {
    "marginLeft": "18rem", "marginRight": "2rem", "padding": "2rem 1rem", "backgroundColor": "#f4f6f9", "minHeight": "100vh"
}

sidebar = html.Div([
    html.H4("Ops & TI Dashboard", className="display-6", style={"fontSize": "1.5rem", "fontWeight": "bold", "color": "#ecf0f1"}),
    html.Hr(style={"borderColor": "#7f8c8d"}),
    html.P("Gestão de Melhoria Contínua", className="lead", style={"fontSize": "0.9rem", "color": "#bdc3c7"}),
    dbc.Nav([
        dbc.NavLink("Visão Geral", href="#", active="exact", style={"color": "white"}),
        dbc.NavLink("Processos", href="#", active="exact", style={"color": "#bdc3c7"}),
        dbc.NavLink("Indicadores", href="#", active="exact", style={"color": "#bdc3c7"}),
        dbc.NavLink("Gargalos", href="#", active="exact", style={"color": "#bdc3c7"}),
        dbc.NavLink("Melhorias", href="#", active="exact", style={"color": "#bdc3c7"}),
    ], vertical=True, pills=True, className="mt-4"),
], style=SIDEBAR_STYLE)

header = dbc.Row([
    dbc.Col(html.H2("Process Improvement & Operations Dashboard", style={"color": "#2c3e50", "fontWeight": "bold"}), width=8),
], className="mb-4")

filters = dbc.Card(dbc.CardBody([
    dbc.Row([
        dbc.Col([
            html.Label("Área Responsável:"),
            dcc.Dropdown(id='filter-area', options=[{'label': i, 'value': i} for i in df_main['Área responsável'].unique()], multi=True, placeholder="Todas as Áreas")
        ], width=4),
        dbc.Col([
            html.Label("Processo:"),
            dcc.Dropdown(id='filter-process', options=[{'label': i, 'value': i} for i in df_main['Processo'].unique()], multi=True, placeholder="Todos os Processos")
        ], width=4),
        dbc.Col([
            html.Label("Status da Melhoria:"),
            dcc.Dropdown(id='filter-status', options=[{'label': i, 'value': i} for i in df_main['Status da melhoria'].unique()], multi=True, placeholder="Todos os Status")
        ], width=4),
    ])
]), className="mb-4 shadow-sm")

def create_kpi_card(title, id_value, color_class, icon=""):
    return dbc.Card(dbc.CardBody([
        html.H6(title, className="card-subtitle text-muted mb-2", style={"fontSize": "0.85rem", "textTransform": "uppercase"}),
        html.H3(id=id_value, className=f"card-title {color_class}", style={"fontWeight": "bold"}),
    ]), className="shadow-sm border-0 h-100")

kpi_cards = dbc.Row([
    dbc.Col(create_kpi_card("Processos Monitorados", "kpi-process", "text-dark"), width=2),
    dbc.Col(create_kpi_card("Gargalos Identificados", "kpi-bottlenecks", "text-danger"), width=2),
    dbc.Col(create_kpi_card("Melhorias Concluídas", "kpi-done", "text-success"), width=2),
    dbc.Col(create_kpi_card("Melhorias em Andamento", "kpi-wip", "text-warning"), width=2),
    dbc.Col(create_kpi_card("Redução Média de Tempo", "kpi-time", "text-primary"), width=2),
    dbc.Col(create_kpi_card("Eficiência Operacional", "kpi-eff", "text-info"), width=2),
], className="mb-4 g-3")

charts_row_1 = dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='chart-1')), className="shadow-sm border-0"), width=4),
    dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='chart-2')), className="shadow-sm border-0"), width=8),
], className="mb-4 g-3")

charts_row_2 = dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='chart-3')), className="shadow-sm border-0"), width=4),
    dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='chart-4')), className="shadow-sm border-0"), width=4),
    dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='chart-5')), className="shadow-sm border-0"), width=4),
], className="mb-4 g-3")

table_section = dbc.Card(dbc.CardBody([
    html.H5("Backlog e Histórico de Melhorias", className="mb-3 text-secondary"),
    html.Div(id='table-container')
]), className="shadow-sm border-0 mb-4")

content = html.Div([header, filters, kpi_cards, charts_row_1, charts_row_2, table_section], style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content])

# =====================================================================
# 5. APP CALLBACKS (Equivalente ao app.py de inicialização)
# =====================================================================
@app.callback(
    [Output('kpi-process', 'children'),
     Output('kpi-bottlenecks', 'children'),
     Output('kpi-done', 'children'),
     Output('kpi-wip', 'children'),
     Output('kpi-time', 'children'),
     Output('kpi-eff', 'children'),
     Output('chart-1', 'figure'),
     Output('chart-2', 'figure'),
     Output('chart-3', 'figure'),
     Output('chart-4', 'figure'),
     Output('chart-5', 'figure'),
     Output('table-container', 'children')],
    [Input('filter-area', 'value'),
     Input('filter-process', 'value'),
     Input('filter-status', 'value')]
)
def update_dashboard(areas, processos, status):
    # Filtragem dos dados
    dff = df_main.copy()
    if areas: dff = dff[dff['Área responsável'].isin(areas)]
    if processos: dff = dff[dff['Processo'].isin(processos)]
    if status: dff = dff[dff['Status da melhoria'].isin(status)]
    
    # 1. Atualizar KPIs
    kpi_proc = dff['Processo'].nunique()
    kpi_garg = len(dff[dff['Status do Processo'] == 'Crítico'])
    kpi_conc = len(dff[dff['Status da melhoria'] == 'Concluído'])
    kpi_anda = len(dff[dff['Status da melhoria'] == 'Em Andamento'])
    
    media_reducao = dff['Impacto estimado (%)'].mean()
    kpi_red_tempo = f"{media_reducao:.1f}%" if pd.notna(media_reducao) else "0%"
    
    # Simulação de taxa de eficiência baseada em processos normais x críticos
    total_valid = len(dff)
    if total_valid > 0:
        eff = (len(dff[dff['Status do Processo'].isin(['Normal', 'Em melhoria'])]) / total_valid) * 100
        kpi_efic = f"{eff:.1f}%"
    else:
        kpi_efic = "N/A"
        
    # 2. Atualizar Gráficos
    fig1 = create_status_pie(dff)
    fig2 = create_time_bar(dff)
    fig3 = create_bottleneck_dist(dff)
    fig4 = create_improvements_timeline(dff)
    fig5 = create_impact_scatter(dff)
    
    # 3. Atualizar Tabela
    table = create_data_table(dff)
    
    return str(kpi_proc), str(kpi_garg), str(kpi_conc), str(kpi_anda), kpi_red_tempo, kpi_efic, fig1, fig2, fig3, fig4, fig5, table

if __name__ == '__main__':
    # Inicializando o servidor
    app.run(debug=True, port=8050, host='0.0.0.0')