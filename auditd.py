#!/usr/bin/env python3
"""
SCRIPT: auditd_report.py
Autor: Paola Medrano
Descripción:
    Compara los registros de logs de auditd con un reporte general de agentes,
    y genera dos archivos:
    - resultado.csv → Coincidencias encontradas
    - sin_coincidencia.csv → Agentes en logs no encontrados en el reporte

Requisitos:
    - pandas
    - Archivos CSV deben estar en la misma carpeta del script
"""

import pandas as pd
import os

def leer_csv_limpio(ruta):
    try:
        df = pd.read_csv(ruta)
        df.columns = df.columns.str.strip()  # Eliminar espacios en encabezados
        return df
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return None
    except pd.errors.ParserError:
        print(f"Error al analizar el archivo CSV: {ruta}")
        return None
    except Exception as e:
        print(f"Error desconocido al leer {ruta}: {e}")
        return None

def procesar_datos(auditd_csv, datos_idr_csv):
    auditd_df = leer_csv_limpio(auditd_csv)
    datos_idr_df = leer_csv_limpio(datos_idr_csv)

    # Verificar si se cargaron correctamente
    if auditd_df is None or datos_idr_df is None:
        return

    # Verificar que exista la columna 'Agent ID'
    if 'Agent ID' not in auditd_df.columns or 'Agent ID' not in datos_idr_df.columns:
        print("Una o ambas columnas 'Agent ID' no están presentes en los archivos.")
        print("Columnas en auditd.csv:", auditd_df.columns.tolist())
        print("Columnas en datos_idr.csv:", datos_idr_df.columns.tolist())
        return

    try:
        # Merge de coincidencias
        resultado_df = pd.merge(auditd_df, datos_idr_df, on='Agent ID')
        resultado_df = resultado_df[['Hostname', 'IP Adress', "Operating System", "Last Seen", 'Log']]
        resultado_df.to_csv('resultado.csv', index=False)
        print("Archivo 'resultado.csv' creado con éxito.")

        # IDs de auditd que no están en datos_idr
        no_encontrados_df = auditd_df[~auditd_df['Agent ID'].isin(datos_idr_df['Agent ID'])]
        if not no_encontrados_df.empty:
            no_encontrados_df.to_csv('sin_coincidencia.csv', index=False)
            print("Archivo 'sin_coincidencia.csv' creado con los ID_Agent sin coincidencia.")
        else:

            
            print("Todos los ID_Agent de auditd.csv tienen coincidencia.")
    except Exception as e:
        print(f"Error al procesar datos: {e}")

def leer_datos():
    while True:
        archivo1 = input("Ingresa el nombre del primer archivo CSV de logs de auditd sacados de la plataforma de InsightIDR: ")
        archivo2 = input("Ingresa el nombre del segundo archivo CSV sacado del reporte de InsightIDR: ")

        # Validación de extensión .csv
        if not archivo1.endswith(".csv") or not archivo2.endswith(".csv"):
            print("Por favor, asegúrate de ingresar archivos con extensión .csv")
            continue

        # Validación de existencia de los archivos
        if not os.path.isfile(archivo1) or not os.path.isfile(archivo2):
            print("Uno o ambos archivos no se encuentran en el directorio actual. Verifica los nombres e intenta de nuevo.")
            continue

        try:
            procesar_datos(archivo1, archivo2)
            break
        except FileNotFoundError:
            print("Error: Uno de los archivos no se encontró. Verifica los nombres e intenta de nuevo.")

# llamar a la funcion
if __name__ == "__main__":
    leer_datos()
