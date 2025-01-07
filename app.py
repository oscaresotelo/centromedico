import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import os
import json

# Obtener las credenciales desde el secreto en GitHub Actions
google_credentials = os.getenv('GOOGLE_CREDENTIALS_JSON')

# Si las credenciales no se encuentran, mostrar un error
if google_credentials is None:
    st.error("Las credenciales de Google no están configuradas.")
else:
    # Convertir las credenciales JSON desde la variable de entorno en un diccionario
    credentials_dict = json.loads(google_credentials)

    # Crear un archivo temporal con las credenciales
    with open('google.json', 'w') as f:
        json.dump(credentials_dict, f)

    # Configuración de Google Sheets
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE_ACCOUNT_FILE = 'google.json'

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    client = gspread.authorize(credentials)

    # Abrir el libro y las hojas
    spreadsheet = client.open_by_key("1o-gOT5NeKmr9J3_BVQdqezrp7q8-25a4iQLxZldQVCo")
    hojas = {
        "postulantes": spreadsheet.worksheet("postulantes"),
        "empresas": spreadsheet.worksheet("empresas"),
        "estudios": spreadsheet.worksheet("estudios"),
        "resultados": spreadsheet.worksheet("resultados"),
        "empresaestudios": spreadsheet.worksheet("empresaestudios"),
    }

    # Funciones auxiliares para interactuar con Google Sheets
    def agregar_fila(hoja, valores):
        valores = [convertir_a_tipo_basico(v) for v in valores]
        hoja.append_row(valores)

    def convertir_a_tipo_basico(valor):
        """ Convierte el valor a un tipo básico de Python (int, str, float) """
        if isinstance(valor, (int, float)):
            return valor
        return str(valor)

    def obtener_todos_los_datos(hoja):
        datos = hoja.get_all_records()
        return pd.DataFrame(datos)

    # Interfaz en Streamlit
    st.title("Sistema de Gestión de Pedidos Prelaborales")

    # Menú lateral con opciones
    menu = st.sidebar.radio(
        "Navegación",
        options=["Inicio", "Postulantes", "Empresas", "Estudios", "Resultados", "Pedidos", "Relacionar Empresa con Estudio"],
    )

    # Contenido dinámico según la selección del menú
    if menu == "Inicio":
        st.header("Bienvenido al Sistema de Gestión de Pedidos Prelaborales")
        st.write("Selecciona una opción del menú para comenzar.")

    elif menu == "Postulantes":
        st.header("Gestión de Postulantes")

        # Obtener la lista de empresas
        empresas_df = obtener_todos_los_datos(hojas["empresas"])
        empresas_opciones = empresas_df["Nombre"].tolist() if not empresas_df.empty else []

        with st.form("form_postulantes"):
            tipo_documento = st.selectbox("Tipo de Documento", options=["DNI", "Pasaporte", "Otro"])
            numero_dni = st.text_input("Número de Documento")
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            estado_civil = st.selectbox("Estado Civil", options=["Soltero", "Casado", "Divorciado", "Viudo", "Otro"])
            sexo = st.selectbox("Sexo", options=["Masculino", "Femenino", "Otro"])
            edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
            fecha_nacimiento = st.date_input("Fecha de Nacimiento")
            observaciones = st.text_area("Observaciones")

            calle = st.text_input("Calle")
            numero = st.text_input("Número")
            departamento = st.text_input("Departamento")
            localidad = st.text_input("Localidad")
            telefono = st.text_input("Teléfono")

            empresa_seleccionada = st.selectbox(
                "Empresa Relacionada",
                options=[f"{row['Codigo']} - {row['Nombre']}" for _, row in empresas_df.iterrows()]
            )
            
            submitted = st.form_submit_button("Agregar Postulante")

            if submitted:
                empresa_codigo = empresa_seleccionada.split(" - ")[0]
                empresa_id = empresas_df.loc[empresas_df["Codigo"] == int(empresa_codigo), "Codigo"].values[0]

                nueva_fila = [
                    len(obtener_todos_los_datos(hojas["postulantes"])) + 1,  # ID autoincremental
                    tipo_documento,
                    numero_dni,
                    nombre,
                    apellido,
                    estado_civil,
                    sexo,
                    edad,
                    fecha_nacimiento.strftime("%Y-%m-%d"),
                    observaciones,
                    calle,
                    numero,
                    departamento,
                    localidad,
                    telefono,
                    empresa_id,
                ]
                agregar_fila(hojas["postulantes"], nueva_fila)
                st.success("Postulante agregado exitosamente.")

        st.subheader("Listado de Postulantes")
        postulantes_df = obtener_todos_los_datos(hojas["postulantes"])
        st.dataframe(postulantes_df)

    elif menu == "Empresas":
        st.header("Gestión de Empresas")

        with st.form("form_empresas"):
            nombre = st.text_input("Nombre de la Empresa")
            domicilio = st.text_input("Domicilio")
            codigo_provincia = st.text_input("Código de Provincia")
            provincia = st.number_input("Provincia", min_value=0, step=1)
            codigo_departamento = st.text_input("Código de Departamento")
            departamento = st.number_input("Departamento", min_value=0, step=1)
            cod_localidad = st.text_input("Código de Localidad")
            cuit = st.number_input("CUIT", min_value=0, step=1)
            privado_publico = st.selectbox("Privado/Publico", options=["Privado", "Público"])
            codigo_tipo_institucion = st.number_input("Código Tipo Institución", min_value=0, step=1)
            porcentaje_ins_tit098 = st.number_input("Porcentaje Inscripción Titular 098", min_value=0, max_value=100, step=1)
            porcentaje_ins_tit099 = st.number_input("Porcentaje Inscripción Titular 099", min_value=0, max_value=100, step=1)
            fecha_registro = st.date_input("Fecha de Registro")
            hora_registro = st.time_input("Hora de Registro")
            submitted = st.form_submit_button("Agregar Empresa")

            if submitted:
                nueva_fila = [
                    len(obtener_todos_los_datos(hojas["empresas"])) + 1,
                    nombre,
                    domicilio,
                    codigo_provincia,
                    provincia,
                    codigo_departamento,
                    departamento,
                    cod_localidad,
                    cuit,
                    privado_publico,
                    codigo_tipo_institucion,
                    porcentaje_ins_tit098,
                    porcentaje_ins_tit099,
                    fecha_registro.strftime("%Y-%m-%d"),
                    hora_registro.strftime("%H:%M:%S"),
                ]
                agregar_fila(hojas["empresas"], nueva_fila)
                st.success("Empresa agregada exitosamente.")

        st.subheader("Listado de Empresas")
        empresas_df = obtener_todos_los_datos(hojas["empresas"])
        st.dataframe(empresas_df)
