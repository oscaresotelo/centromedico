import sqlite3
import csv
import os

# Establecer la conexión con la base de datos SQLite
db_file = 'sistema_pedidos.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Eliminar la tabla 'empresas' si ya existe, para asegurarnos de que tenga la estructura correcta
cursor.execute('DROP TABLE IF EXISTS empresas;')

# Crear la tabla 'empresas' con la estructura correcta
cursor.execute('''
CREATE TABLE empresas (
    Codigo TEXT PRIMARY KEY,
    Nombre TEXT,
    Domicilio TEXT,
    Codigo_Provincia TEXT,
    Provincia TEXT,
    Codigo_Departamento TEXT,
    Departamento TEXT,
    Codigo_Localidad TEXT,
    CUIT TEXT,
    Privado_Publico TEXT,
    Codigo_TipoInstitucion TEXT,
    Porcentaje_Ins_Tit098 REAL,
    Porcentaje_Ins_Tit099 REAL,
    Fecha_Registro TEXT,
    Hora_Registro TEXT
);
''')

# Ruta del archivo CSV
csv_file = 'empresas.csv'

# Verificar si el archivo CSV existe
if os.path.exists(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        # Especificar el delimitador como punto y coma
        reader = csv.reader(file, delimiter=';')  # Leer el archivo CSV como una lista de listas

        # Saltar la primera fila de encabezado
        next(reader)  # Omitir el encabezado

        # Insertar cada fila del archivo CSV en la tabla 'empresas'
        for row_number, row in enumerate(reader, start=1):
            # Mostrar la cantidad de columnas por fila para depurar
            print(f"Fila {row_number} tiene {len(row)} columnas: {row}")

            # Limpiar los espacios al principio y al final de cada valor
            row = [value.strip() if value else None for value in row]

            # Si la fila tiene más de 15 columnas, recortamos a 15 columnas
            if len(row) > 15:
                print(f"Fila {row_number} tiene más de 15 columnas, recortando el exceso.")
                row = row[:15]  # Recortamos a 15 columnas si hay más

            # Si la fila tiene menos de 15 columnas, completamos con None (NULL) para que coincidan las columnas
            if len(row) < 15:
                print(f"Fila {row_number} tiene menos de 15 columnas, completando con None")
                # Completar con None hasta completar las 15 columnas
                row.extend([None] * (15 - len(row)))

            # Asegurarnos de que la fila tiene exactamente 15 columnas
            if len(row) == 15:
                # Depuración para verificar el contenido de la fila antes de insertar
                print(f"Fila {row_number} después de limpieza: {row}")

                # Insertar la fila en la base de datos
                try:
                    cursor.execute('''
                    INSERT OR IGNORE INTO empresas (
                        Codigo, Nombre, Domicilio, Codigo_Provincia, Provincia,
                        Codigo_Departamento, Departamento, Codigo_Localidad, CUIT,
                        Privado_Publico, Codigo_TipoInstitucion, Porcentaje_Ins_Tit098,
                        Porcentaje_Ins_Tit099, Fecha_Registro, Hora_Registro
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', tuple(row))  # Convertimos la fila a una tupla para insertarla
                    print(f"Fila {row_number} insertada correctamente.")
                except Exception as e:
                    print(f"Error al insertar la fila {row_number}: {e}")

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print("Datos cargados correctamente desde el archivo CSV.")
else:
    print(f"El archivo {csv_file} no existe.")

# Verificar si se insertaron datos
cursor.execute("SELECT COUNT(*) FROM empresas;")
count = cursor.fetchone()[0]
print(f"Número de registros en la base de datos: {count}")

# Cerrar la conexión con la base de datos
conn.close()
