import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análisis de Peliculas")

df = pd.read_csv("peliculas.csv")

st.title("Analisis de peliculas")
st.write("Información basica de un conjunto de peliculas")

st.sidebar.header("Filtros")

generos = ["Todos"] + sorted(df["genero"].unique().tolist())
genero = st.sidebar.selectbox("Selecciona un genero", generos)

texto = st.sidebar.text_input("Buscar pelicula")

df_filtrado = df.copy()

if genero != "Todos":
    df_filtrado = df_filtrado[df_filtrado["genero"] == genero]

if texto:
    df_filtrado = df_filtrado[df_filtrado["titulo"].str.contains(texto, case=False, na=False)]

col1, col2, col3 = st.columns(3)
col1.metric("Películas", len(df_filtrado))
col2.metric("Calificación promedio", round(df_filtrado["calificacion"].mean(), 2) if len(df_filtrado) else 0)
col3.metric("Año más reciente", int(df_filtrado["año"].max()) if len(df_filtrado) else "-")

st.subheader("Datos")
st.dataframe(df_filtrado, use_container_width=True)

if len(df_filtrado) > 0:
    st.subheader("Película con mayor calificación")
    mejor = df_filtrado.loc[df_filtrado["calificacion"].idxmax()]
    st.write("**" + mejor["titulo"] + "** tiene una calificación de **" + str(mejor["calificacion"]) + "**.")

    st.subheader("Películas por genero")
    conteo = df_filtrado["genero"].value_counts()

    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_xlabel("Genero")
    ax.set_ylabel("Cantidad")
    ax.set_title("Cantidad de películas por genero")
    st.pyplot(fig)
else:
    st.warning("No se encontraron películas con los filtros seleccionados")
