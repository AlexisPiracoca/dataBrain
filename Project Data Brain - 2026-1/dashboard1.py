import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
)

# ------------------------------------------------
# TÍTULO
# ------------------------------------------------

st.title("Data Brain Analytics Dashboard")


# ------------------------------------------------
# CARGAR DATASET
# ------------------------------------------------

archivo = st.file_uploader(
    "Cargar archivo CSV",
    type=["csv"]
)

# ------------------------------------------------
# VALIDAR CARGA
# ------------------------------------------------

if archivo is not None:

    # Leer dataset
    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    # ------------------------------------------------
    # MOSTRAR DATASET
    # ------------------------------------------------

    st.subheader("Vista General del Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ------------------------------------------------
    # INFORMACIÓN GENERAL
    # ------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Filas",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columnas",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Valores Nulos",
            df.isnull().sum().sum()
        )

    st.divider()

    # ------------------------------------------------
    # SELECCIÓN DE VARIABLES
    # ------------------------------------------------

    st.sidebar.header("Configuración de Gráfica")

    columnas = df.columns.tolist()

    eje_x = st.sidebar.selectbox(
        "Seleccione eje X",
        columnas
    )

    eje_y = st.sidebar.selectbox(
        "Seleccione eje Y",
        columnas
    )

    tipo_grafica = st.sidebar.selectbox(
        "Seleccione tipo de gráfica",
        [
            "Barra",
            "Línea",
            "Dispersión",
            "Histograma",
            "Caja"
        ]
    )

    # ------------------------------------------------
    # SELECCIÓN DE COLOR
    # ------------------------------------------------

    color_tema = st.sidebar.selectbox(
        "Seleccione paleta de colores",
        [
            "Vivid",
            "Bold",
            "Pastel",
            "Dark2",
            "Set2",
            "Teal",
            "Viridis"
        ]
    )

    # ------------------------------------------------
    # PALETAS
    # ------------------------------------------------

    paletas = {
        "Vivid": px.colors.qualitative.Vivid,
        "Bold": px.colors.qualitative.Bold,
        "Pastel": px.colors.qualitative.Pastel,
        "Dark2": px.colors.qualitative.Dark2,
        "Set2": px.colors.qualitative.Set2,
        "Teal": px.colors.sequential.Teal,
        "Viridis": px.colors.sequential.Viridis
    }

    colores = paletas[color_tema]

    # ------------------------------------------------
    # CREAR GRÁFICA
    # ------------------------------------------------

    st.subheader("Visualización de Datos")

    if tipo_grafica == "Barra":

        fig = px.bar(
            df,
            x=eje_x,
            y=eje_y,
            color=eje_x,
            template="plotly_dark",
            color_discrete_sequence=colores,
            title="Gráfico de Barras"
        )

    elif tipo_grafica == "Línea":

        fig = px.line(
            df,
            x=eje_x,
            y=eje_y,
            color=eje_x,
            template="plotly_dark",
            color_discrete_sequence=colores,
            title="Gráfico de Línea"
        )

    elif tipo_grafica == "Dispersión":

        fig = px.scatter(
            df,
            x=eje_x,
            y=eje_y,
            color=eje_x,
            size=eje_y,
            template="plotly_dark",
            color_discrete_sequence=colores,
            title="Gráfico de Dispersión"
        )

    elif tipo_grafica == "Histograma":

        fig = px.histogram(
            df,
            x=eje_x,
            color=eje_x,
            template="plotly_dark",
            color_discrete_sequence=colores,
            title="Histograma"
        )

    elif tipo_grafica == "Caja":

        fig = px.box(
            df,
            x=eje_x,
            y=eje_y,
            color=eje_x,
            template="plotly_dark",
            color_discrete_sequence=colores,
            title="Diagrama de Caja"
        )

    # ------------------------------------------------
    # MOSTRAR GRÁFICA
    # ------------------------------------------------

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------
    # ESTADÍSTICAS
    # ------------------------------------------------

    st.subheader("Estadísticas Descriptivas")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

else:

    st.info("Por favor cargue un archivo CSV para comenzar.")