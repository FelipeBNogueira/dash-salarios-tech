import re
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ── Config da página ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# ── Carregamento com cache ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    df_ = pd.read_csv(url)
    df_["ano"] = df_["ano"].astype(int)
    df_["usd"] = pd.to_numeric(df_["usd"], errors="coerce")
    for c in ["cargo", "senioridade", "contrato", "tamanho_empresa", "remoto"]:
        df_[c] = df_[c].astype(str)
    return df_.dropna(subset=["usd"])

URL = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/main/dados-imersao-final.csv"
df = load_data(URL)

# ── Barra lateral (filtros) ────────────────────────────────────────────────────
st.sidebar.header("🔍 Filtros")

# Moeda e conversão
st.sidebar.subheader("💲 Moeda")
moeda = st.sidebar.radio("Exibir valores em:", ["USD", "BRL"], horizontal=True)
taxa_brl = st.sidebar.number_input(
    "Taxa USD → BRL", value=5.50, step=0.05,
    help="Usada apenas se BRL estiver selecionado."
)
fator = 1.0 if moeda == "USD" else float(taxa_brl)

# Filtros básicos
anos = sorted(df["ano"].unique())
anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)

senioridades = sorted(df["senioridade"].unique())
senior_sel = st.sidebar.multiselect("Senioridade", senioridades, default=senioridades)

contratos = sorted(df["contrato"].unique())
contratos_sel = st.sidebar.multiselect("Tipo de Contrato", contratos, default=contratos)

tamanhos = sorted(df["tamanho_empresa"].unique())
tamanhos_sel = st.sidebar.multiselect("Tamanho da Empresa", tamanhos, default=tamanhos)

# Filtro de cargo por digitação
st.sidebar.subheader("🧠 Cargo (digite)")
cargo_query = st.sidebar.text_input(
    "Digite parte(s) do cargo (use ; para várias)",
    placeholder="ex.: data scientist; engineer; analytics"
)
tokens = [t.strip() for t in cargo_query.split(";") if t.strip()]
if tokens:
    pattern = "|".join([re.escape(t) for t in tokens])  # OU entre termos
    mask_cargo = df["cargo"].str.contains(pattern, case=False, na=False)
else:
    mask_cargo = True

# Faixa salarial (em USD para filtro)
st.sidebar.subheader("💵 Faixa salarial (USD base)")
min_usd = int(df["usd"].min())
max_usd = int(df["usd"].max())
faixa = st.sidebar.slider("Selecione a faixa", min_value=min_usd, max_value=max_usd,
                          value=(min_usd, max_usd), step=5000)

# Aplica filtros
df_filtrado = df[
    (df["ano"].isin(anos_sel)) &
    (df["senioridade"].isin(senior_sel)) &
    (df["contrato"].isin(contratos_sel)) &
    (df["tamanho_empresa"].isin(tamanhos_sel)) &
    mask_cargo &
    (df["usd"].between(faixa[0], faixa[1]))
].copy()

# Coluna convertida para exibição
df_filtrado["valor"] = df_filtrado["usd"] * fator
sufixo_moeda = moeda

# ── Título ─────────────────────────────────────────────────────────────────────
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais nos últimos anos. Use os filtros ao lado para refinar.")

# ── KPIs (apenas 4 cards) ──────────────────────────────────────────────────────
st.subheader(f"Métricas gerais (salário anual em {sufixo_moeda})")
if df_filtrado.empty:
    st.warning("Nenhum dado com os filtros atuais.")
    st.stop()

salario_medio   = df_filtrado["valor"].mean()
salario_maximo  = df_filtrado["valor"].max()
total_registros = int(df_filtrado.shape[0])
cargo_mais_freq = df_filtrado["cargo"].mode().iat[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Salário médio", f"{salario_medio:,.0f} {sufixo_moeda}")
c2.metric("Salário máximo", f"{salario_maximo:,.0f} {sufixo_moeda}")
c3.metric("Total de registros", f"{total_registros:,}")
c4.metric("Cargo mais frequente", cargo_mais_freq)

st.markdown("---")

# ── Abas ───────────────────────────────────────────────────────────────────────
aba1, aba2, aba3, aba4 = st.tabs(["📈 Visão Geral", "📊 Distribuições", "🗺️ Geografia", "🧾 Detalhes"])

with aba1:
    col1, col2 = st.columns(2)

    # Top 10 cargos por média salarial (valores DENTRO, preto)
    top_cargos = (
        df_filtrado.groupby("cargo", as_index=False)["valor"].mean()
        .nlargest(10, "valor")
        .sort_values("valor", ascending=True)
    )
    fig1 = px.bar(
        top_cargos, x="valor", y="cargo",
        orientation="h",
        title=f"Top 10 cargos por salário médio ({sufixo_moeda})",
        labels={"valor": f"Média anual ({sufixo_moeda})", "cargo": ""}
    )
    fig1.update_traces(
        texttemplate='%{x:,.0f}',
        textposition='inside',
        insidetextfont_color='black',
        textfont_size=12
    )
    fig1.update_layout(
        title_x=0.1,
        yaxis={"categoryorder": "total ascending"},
        xaxis=dict(showticklabels=False)
    )
    col1.plotly_chart(fig1, use_container_width=True)

    # Mediana por ano e senioridade (mantida, pois é gráfico analítico)
    mediana_ano_senior = (
        df_filtrado.groupby(["ano", "senioridade"], as_index=False)["valor"].median()
    )
    fig2 = px.line(
        mediana_ano_senior, x="ano", y="valor", color="senioridade",
        markers=True, title=f"Mediana salarial por ano e senioridade ({sufixo_moeda})",
        labels={"valor": f"Mediana ({sufixo_moeda})", "ano": "Ano", "senioridade": "Senioridade"}
    )
    fig2.update_traces(mode="lines+markers+text",
                       texttemplate='%{y:,.0f}',
                       textposition="top center")
    fig2.update_layout(title_x=0.1, yaxis=dict(showticklabels=False))
    col2.plotly_chart(fig2, use_container_width=True)

with aba2:
    col3, col4 = st.columns(2)

    # Histograma com espaço entre barras + valores FORA (branco)
    nb = st.slider("Nº de bins do histograma", 10, 80, 30, 5)
    fig3 = px.histogram(
        df_filtrado, x="valor", nbins=nb,
        title=f"Distribuição de salários anuais ({sufixo_moeda})",
        labels={"valor": f"Faixa salarial ({sufixo_moeda})"}
    )
    fig3.update_traces(
        texttemplate='%{y:,}',
        textposition='outside',
        textfont_color='white',
        marker_line_width=1,
        marker_line_color="white",
        cliponaxis=False
    )
    fig3.update_layout(
        title_x=0.1,
        bargap=0.2,
        yaxis=dict(showticklabels=False),
        uniformtext_minsize=10,
        uniformtext_mode='show',
        margin=dict(t=90)
    )
    col3.plotly_chart(fig3, use_container_width=True)

    # Boxplot por senioridade
    fig4 = px.box(
        df_filtrado, x="senioridade", y="valor", points="outliers",
        title=f"Distribuição por senioridade ({sufixo_moeda})",
        labels={"valor": f"Salário ({sufixo_moeda})", "senioridade": "Senioridade"}
    )
    fig4.update_layout(title_x=0.1, yaxis=dict(showticklabels=False))
    col4.plotly_chart(fig4, use_container_width=True)

with aba3:
    col5, col6 = st.columns(2)

    # Tipos de trabalho (donut)
    remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
    remoto_contagem.columns = ["tipo_trabalho", "quantidade"]
    fig5 = px.pie(
        remoto_contagem, names="tipo_trabalho", values="quantidade",
        title="Proporção dos tipos de trabalho", hole=0.5
    )
    fig5.update_traces(textinfo="percent+label")
    fig5.update_layout(title_x=0.1)
    col5.plotly_chart(fig5, use_container_width=True)

    # Mapa: Cientista de Dados (média por país)
    df_ds = df_filtrado[df_filtrado["cargo"].str.lower() == "data scientist"]
    if not df_ds.empty and "residencia_iso3" in df_ds.columns:
        media_ds_pais = df_ds.groupby("residencia_iso3", as_index=False)["valor"].mean()
        fig6 = px.choropleth(
            media_ds_pais,
            locations="residencia_iso3",
            color="valor",
            color_continuous_scale="RdYlGn",
            title=f"Salário médio de Cientista de Dados por país ({sufixo_moeda})",
            labels={"valor": f"Média ({sufixo_moeda})", "residencia_iso3": "País"},
        )
        fig6.update_layout(title_x=0.1)
        col6.plotly_chart(fig6, use_container_width=True)
    else:
        col6.info("Sem dados suficientes de **Data Scientist** para o mapa com os filtros atuais.")

with aba4:
    st.subheader("Dados Detalhados (filtrados)")
    st.dataframe(
        df_filtrado.sort_values("valor", ascending=False),
        use_container_width=True, height=520
    )

    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar CSV filtrado",
        data=csv,
        file_name="salarios_filtrado.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Valores em USD ou BRL (conversão definida no painel). Rótulos: barras (dentro) e histograma (fora).")
