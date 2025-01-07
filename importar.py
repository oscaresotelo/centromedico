import sqlite3
import pandas as pd
import streamlit as st

# Crear la base de datos SQLite y la tabla si no existe
def create_db():
    # Conectar a la base de datos (se creará si no existe)
    conn = sqlite3.connect('sistema_pedidos.db')
    cursor = conn.cursor()

    # Crear la tabla 'pedidos'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudios (
            Id INTEGER PRIMARY KEY,
            Des TEXT,
            Referencia TEXT,
            Precio INTEGER,
            Generales TEXT,
            Basico INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Función para cargar los datos desde un archivo CSV subido
def cargar_datos_csv(file):
    # Intentar leer el CSV con encoding='latin1'
    df = pd.read_csv(file, sep=";", encoding='latin1')
    return df

# Función para insertar los datos en la base de datos
def insertar_datos(df):
    conn = sqlite3.connect('sistema_pedidos.db')
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO estudios (Id, Des, Referencia, Precio, Generales, Basico)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['Id'], row['Des'], row['Referencia'], row['Precio'], row['Generales'], row['Basico']))
    
    conn.commit()
    conn.close()

# Aplicación Streamlit
def app():
    st.title("Gestión de Estudios")

    # Crear la base de datos y la tabla si no existen
    create_db()

    # Subir archivo CSV
    st.subheader("Subir archivo CSV")
    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Cargar y mostrar los datos del archivo CSV
        try:
            datos_df = cargar_datos_csv(uploaded_file)
            st.write("Datos cargados desde el archivo CSV:")
            st.write(datos_df)

            # Insertar los datos en la base de datos
            if st.button('Insertar Datos'):
                insertar_datos(datos_df)
                st.success("Datos insertados correctamente en la base de datos.")
        except Exception as e:
            st.error(f"Ocurrió un error al cargar el archivo CSV: {e}")

    # Mostrar la base de datos
    if st.button('Mostrar Pedidos'):
        conn = sqlite3.connect('sistema_pedidos.db')
        df_pedidos = pd.read_sql('SELECT * FROM estudios', conn)
        conn.close()
        st.write(df_pedidos)

if __name__ == '__main__':
    app()
