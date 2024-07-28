import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO
import tempfile

# Función para extraer datos de una tabla
def extraer(tabla, conn):
    query = f'SELECT * FROM {tabla}'
    df = pd.read_sql_query(query, conn)
    return df

# Función para convertir la intensidad del dolor a valores numéricos
def convertir_intensidad(intensidad):
    mapping = {
        'Sin Dolor': 0,
        'Dolor Leve': 1,
        'Dolor Moderado': 2,
        'Dolor Intenso': 3,
        'Dolor Muy Intenso': 4,
        'Dolor Insoportable': 5
    }
    return mapping.get(intensidad, np.nan)

# Función para generar gráficos
def generar_graficos(df):
    st.subheader('Distribución de las Patologías Consultadas')
    plt.figure(figsize=(10, 6))
    sns.countplot(y='patologia', data=df, order=df['patologia'].value_counts().index)
    plt.title('Distribución de las Patologías Consultadas')
    plt.xlabel('Número de Consultas')
    plt.ylabel('Patología')
    st.pyplot(plt)
    plt.clf()

    st.subheader('Distribución de la Intensidad del Dolor')
    plt.figure(figsize=(10, 6))
    sns.countplot(y='intensidad', data=df, order=df['intensidad'].value_counts().index)
    plt.title('Distribución de la Intensidad del Dolor')
    plt.xlabel('Número de Consultas')
    plt.ylabel('Intensidad del Dolor')
    st.pyplot(plt)
    plt.clf()

    st.subheader('Relación entre la Intensidad del Dolor y la Duración')
    df['intensidad_numerica'] = df['intensidad'].apply(convertir_intensidad)
    df['duracion_numerica'] = df['duracion'].map({'Muy Corta': 1, 'Corta': 2, 'Media': 3, 'Larga': 4, 'Muy Larga': 5})
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='duracion_numerica', y='intensidad_numerica', data=df)
    plt.title('Relación entre la Intensidad del Dolor y la Duración')
    plt.xlabel('Duración (numérica)')
    plt.ylabel('Intensidad del Dolor (numérica)')
    plt.xticks(ticks=[1, 2, 3, 4, 5], labels=['Muy Corta', 'Corta', 'Media', 'Larga', 'Muy Larga'])
    st.pyplot(plt)
    plt.clf()

    st.subheader('Número de Consultas por Usuario')
    plt.figure(figsize=(10, 6))
    sns.countplot(y='username', data=df, order=df['username'].value_counts().index)
    plt.title('Número de Consultas por Usuario')
    plt.xlabel('Número de Consultas')
    plt.ylabel('Usuario')
    st.pyplot(plt)
    plt.clf()

    st.subheader('Distribución de Consultas por Fecha')
    df['fecha_solo'] = df['fecha'].dt.date
    consultas_por_fecha = df.groupby('fecha_solo').size()
    plt.figure(figsize=(10, 6))
    consultas_por_fecha.plot(kind='bar')
    plt.title('Distribución de Consultas por Fecha')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Consultas')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.clf()

# Título de la aplicación
st.title('DolorFarma')

# Cargar archivo SQLite
uploaded_file = st.file_uploader("Sube tu base de datos SQLite", type="sqlite3")

if uploaded_file is not None:
    if uploaded_file.size > 200 * 1024 * 1024:
        st.error("El archivo es demasiado grande. El tamaño máximo permitido es de 200 MB.")
    else:
        # Guardar el archivo subido en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Conectar a la base de datos SQLite usando el archivo temporal
        conn = sqlite3.connect(tmp_file_path)
        consultas = extraer('main_consulta', conn)
        users = extraer('auth_user', conn)
        users = users[['id', 'username', 'email', 'date_joined']]
        df = pd.merge(consultas, users.rename(columns={'id':'user_id'}), how='left', on='user_id')
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['user_id'] = df['user_id'].astype('object')
        generar_graficos(df)
else:
    st.write("Por favor, sube una base de datos SQLite para continuar.")
