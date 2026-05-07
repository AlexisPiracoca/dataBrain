import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------

st.set_page_config(
    page_title="Museo",
    layout="wide",
)

# ------------------------------------------------
# CARGAR DATOS
# ------------------------------------------------

museum_df = pd.read_csv("museum_data.csv")

# ------------------------------------------------
# TÍTULO
# ------------------------------------------------

st.title("Dashboard del Museo")

st.markdown("""Análisis de visitantes y rutas inteligentes""")

# ------------------------------------------------
# MÉTRICAS
# ------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Visitantes",
        value=len(museum_df)
    )

with col2:
    st.metric(
        label="Tiempo Promedio",
        value=round(
            museum_df['tiempo_minutos'].mean(),
            2
        )
    )

with col3:
    st.metric(
        label="Obra Más Visitada",
        value=museum_df['obra_visitada'].mode()[0]
    )

st.divider()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.header("Filtros")

interes = st.sidebar.selectbox(
    "Seleccione interés",
    museum_df["interes"].unique()
)

df_filtrado = museum_df[
    museum_df["interes"] == interes
]

# ------------------------------------------------
# GRÁFICAS EN HORIZONTAL
# ------------------------------------------------

col4, col5 = st.columns(2)

# ------------------------------------------------
# GRÁFICA 1
# ------------------------------------------------

with col4:

    st.subheader("Obras Más Visitadas")

    obras_chart = (
        df_filtrado["obra_visitada"]
        .value_counts()
        .reset_index()
    )

    obras_chart.columns = [
        "Obra",
        "Cantidad"
    ]

    fig1 = px.bar(
        obras_chart,
        x="Obra",
        y="Cantidad",
        color="Obra",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        title="Cantidad de Visitas"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ------------------------------------------------
# GRÁFICA 2
# ------------------------------------------------

with col5:

    st.subheader("Tiempo Promedio por Obra")

    promedio = (
        df_filtrado
        .groupby("obra_visitada")[
            "tiempo_minutos"
        ]
        .mean()
        .reset_index()
    )

    promedio.columns = [
        "Obra",
        "Tiempo Promedio"
    ]

    fig2 = px.bar(
        promedio,
        x="Obra",
        y="Tiempo Promedio",
        color="Obra",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Teal,
        title="Tiempo Promedio"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ------------------------------------------------
# GRÁFICA 3
# ------------------------------------------------

st.subheader("Distribución de Edades")

fig3 = px.histogram(
    df_filtrado,
    x="edad",
    nbins=30,
    color_discrete_sequence=["#00C2FF"],
    template="plotly_dark",
    title="Edades de los Visitantes",
    opacity=0.8,
)

fig3.update_layout(
    bargap=0.1,
    xaxis_title="Edad",
    yaxis_title="Cantidad de Personas",
    height=500
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ------------------------------------------------
# TABLA INTERACTIVA
# ------------------------------------------------

st.subheader("Datos Filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# ------------------------------------------------
# RECOMENDACIÓN
# ------------------------------------------------

st.subheader("Recomendación de Obras")

recomendadas = (
    df_filtrado["obra_visitada"]
    .value_counts()
    .reset_index()
)

recomendadas.columns = [
    "Obra",
    "Cantidad"
]

st.table(recomendadas)

# ------------------------------------------------
# MENSAJE FINAL
# ------------------------------------------------

st.success(
    f"""
    Recomendación principal:
    {recomendadas.iloc[0]['Obra']}
    """
)