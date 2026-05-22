# -*- coding: utf-8 -*-import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuração da página com as cores da identidade visual (Simulação)
st.set_page_config(page_title="Pro Delphus - Tech Sales & Operations", layout="wide")

st.title("📊 Plataforma Integrada de Gestão — Pro Delphus")
st.markdown("Análise Comercial Geográfica e Gestão de Operações da Fábrica")

# --- CRIAÇÃO DAS ABAS PRINCIPAIS ---
aba_comercial, aba_fabrica = st.tabs(["📈 Análise Comercial", "👥 Equipe da Fábrica"])

# =====================================================================
# ABA 1: ANÁLISE COMERCIAL (Código anterior preservado e organizado)
# =====================================================================
with aba_comercial:
    # --- SIMULAÇÃO DE DADOS INTERNOS ---
    @st.cache_data
    def carregar_dados_comerciais():
        regioes = ['Sudeste', 'Nordeste', 'Sul', 'Centro-Oeste', 'Norte', 'América Latina (Export)', 'Europa (Export)']
        especialidades = ['Neurocirurgia (SIMONT)', 'Laparoscopia', 'Ginecologia', 'Ortopedia/Artroscopia', 'Cardiologia']
        
        np.random.seed(42)
        dados = []
        for _ in range(500):
            regiao = np.random.choice(regioes)
            especialidade = np.random.choice(especialidades)
            vendas = np.random.randint(1, 5)
            faturamento = vendas * np.random.randint(5000, 25000)
            recompra = np.random.choice([0, 1], p=[0.6, 0.4])
            custo_logistico = faturamento * np.random.uniform(0.02, 0.15) if "Export" not in regiao else faturamento * np.random.uniform(0.12, 0.30)
            
            dados.append({
                "Região": regiao,
                "Especialidade": especialidade,
                "Unidades Vendidas": vendas,
                "Faturamento (R$)": faturamento,
                "Cliente Recorrente": recompra,
                "Custo Logístico (R$)": custo_logistico
            })
        return pd.DataFrame(dados)

    df = carregar_dados_comerciais()

    # Filtros na barra lateral (afetam apenas a aba comercial)
    st.sidebar.header("Filtros Comerciais")
    regioes_selecionadas = st.sidebar.multiselect("Filtrar por Região/Mercado:", options=df["Região"].unique(), default=df["Região"].unique())
    df_filtrado = df[df["Região"].isin(regioes_selecionadas)]

    # KPIs
    total_faturamento = df_filtrado["Faturamento (R$)"].sum()
    total_unidades = df_filtrado["Unidades Vendidas"].sum()
    taxa_recompra_geral = (df_filtrado["Cliente Recorrente"].sum() / len(df_filtrado)) * 100
    custo_log_total = df_filtrado["Custo Logístico (R$)"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faturamento Filtrado", f"R$ {total_faturamento:,.2f}")
    col2.metric("Unidades Comercializadas", f"{total_unidades:,}")
    col3.metric("Taxa de Recompra Média", f"{taxa_recompra_geral:.1f}%")
    col4.metric("Custo Logístico Acumulado", f"R$ {custo_log_total:,.2f}")

    st.markdown("---")

    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("🎯 Especialidades Mais Procuradas por Região")
        fig_esp = px.bar(
            df_filtrado, x="Região", y="Faturamento (R$)", color="Especialidade",
            title="Volume Financeiro por Linha de Simulador", barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_esp, use_container_width=True)

    with col_dir:
        st.subheader("🔄 Taxa de Recompra por Especialidade")
        recompra_esp = df_filtrado.groupby("Especialidade")["Cliente Recorrente"].mean().reset_index()
        recompra_esp["Taxa de Recompra (%)"] = recompra_esp["Cliente Recorrente"] * 100
        fig_rec = px.bar(
            recompra_esp, y="Especialidade", x="Taxa de Recompra (%)", orientation='h',
            title="Índice de Fidelização (Hospitais/Universidades)", color="Taxa de Recompra (%)",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_rec, use_container_width=True)

    st.markdown("---")
    st.subheader("🚛 Otimização Logística vs. Faturamento")
    logistica_regiao = df_filtrado.groupby("Região").agg({"Faturamento (R$)": "sum", "Custo Logístico (R$)": "sum"}).reset_index()
    logistica_regiao["Percentual Custo Logístico (%)"] = (logistica_regiao["Custo Logístico (R$)"] / logistica_regiao["Faturamento (R$)"]) * 100

    fig_log = px.scatter(
        logistica_regiao, x="Faturamento (R$)", y="Percentual Custo Logístico (%)",
        size="Custo Logístico (R$)", text="Região", title="Onde a logística consome a margem?", size_max=60
    )
    fig_log.update_traces(textposition='top center')
    st.plotly_chart(fig_log, use_container_width=True)

# =====================================================================
# ABA 2: EQUIPE DA FÁBRICA (Nova funcionalidade com os seus dados)
# =====================================================================
with aba_fabrica:
    st.subheader("👥 Fichas Cadastrais e Alocação por Setor")
    st.markdown("Visualize os colaboradores ativos nos processos de manufatura de blocos anatômicos e simuladores.")

    # Base de dados dos funcionários baseada no seu envio
    dados_funcionarios = [
        {"Nome": "Mauro", "Setor": "Forma", "Função": "Técnico de Modelagem / Forma"},
        {"Nome": "Josilene", "Setor": "Forma", "Função": "Técnica de Modelagem / Forma"},
        {"Nome": "Jovem", "Setor": "Forma", "Função": "Auxiliar de Produção — Formas"},
        {"Nome": "Jose Kele", "Setor": "Neoderma", "Função": "Especialista em Síntese de Neoderma"},
        {"Nome": "Paulo", "Setor": "Neoderma", "Função": "Técnico de Produção de Polímeros"},
        {"Nome": "Igor", "Setor": "Neoderma", "Função": "Operador de Injeção de Material"},
        {"Nome": "Rogatier", "Setor": "Fibra", "Função": "Laminador / Técnico em Resinas e Fibra"},
        {"Nome": "Paulo", "Setor": "Pintura", "Função": "Artista Anatômico / Acabamento e Pintura"}
    ]
    df_func = pd.DataFrame(dados_funcionarios)

    # Filtro por setor na tela principal da aba
    setores_disponiveis = ["Todos"] + list(df_func["Setor"].unique())
    setor_selecionado = st.selectbox("Selecione o Setor para Filtrar a Equipe:", setores_disponiveis)

    if setor_selecionado != "Todos":
        df_filtrado_func = df_func[df_func["Setor"] == setor_selecionado]
    else:
        df_filtrado_func = df_func

    # Layout de exibição em cartões (cards) para cada funcionário
    st.write("")
    cols = st.columns(3)  # Exibe em até 3 colunas paralelas na tela
    
    for idx, row in df_filtrado_func.iterrows():
        # Distribui os cartões entre as colunas criadas
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### 👤 {row['Nome']}")
                st.markdown(f"**Setor:** `{row['Setor']}`")
                st.markdown(f"**Cargo/Função Ocupada:** {row['Função']}")
                
                # Exemplo de como adicionar pequenas interações para cada um no futuro
                status = st.toggle("Presente hoje", value=True, key=f"status_{row['Nome']}_{idx}")
                if status:
                    st.caption("🟢 Disponível em linha de produção")
                else:
                    st.caption("🔴 Ausente ou em outra atividade")

    # Métrica de Resumo do Chão de Fábrica
    st.markdown("---")
    st.markdown("#### 📊 Indicadores Rápidos da Fábrica")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Operadores Ativos", len(df_func))
    c2.metric("Setor mais Populoso", "Forma (3 colaboradores)")
    c3.metric("Especialidades Cobertas", f"{df_func['Setor'].nunique()} setores críticos")
