import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

conn = sqlite3.connect('db.sqlite3')

def extraer(tabla):
    query = f'SELECT * FROM {tabla}'
    df = pd.read_sql_query(query, conn)
    return df

consultas = extraer('main_consulta')
users = extraer('auth_user')
users = users[['id', 'username', 'email', 'date_joined']]
df = pd.merge(consultas, users.rename(columns={'id':'user_id'}), how='left', on='user_id')
df['fecha'] = pd.to_datetime(df['fecha'])
df['user_id'] = df['user_id'].astype('object')

st.title('Mi Aplicación en Streamlit')
st.write('¡Hola, mundo!')