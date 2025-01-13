import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from statsbombpy import sb

# Ruta para guardar archivos
OUTPUT_PATH = r"C:\Users\anavarro\OneDrive - INDEPORTES ANTIOQUIA\AI\2024\METODOLOGO\PYTHON\MODULO 8\M-8 TAREA_4\data"

# Página de análisis de equipos
def main():
    st.title("Análisis de Partidos (Equipos)")

    # Cargar datos de partidos
    C_Am = sb.matches(competition_id=223, season_id=282)
    matches_df = C_Am[["home_team", "away_team", "match_id"]].copy()
    matches_df["Plays"] = matches_df["home_team"] + " vs " + matches_df["away_team"]

    # Selección de partido
    selected_play = st.sidebar.selectbox("Selecciona un partido:", matches_df["Plays"])
    match_id = matches_df[matches_df["Plays"] == selected_play]["match_id"].values[0]

    # Extraer eventos del partido seleccionado
    events = sb.events(match_id=match_id)

    # Estadística gráfica de equipos
    st.subheader("Estadísticas del Partido")
    action_counts = events["type"].value_counts().head(5)  # Principales acciones
    fig, ax = plt.subplots(figsize=(8, 5))
    action_counts.plot(kind="bar", color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"], ax=ax)
    ax.set_title("Principales Acciones del Partido")
    ax.set_xlabel("Acción")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)

    # Tabla Local vs Visitante con acciones principales
    st.subheader("Comparación de Equipos")
    home_team = matches_df[matches_df["match_id"] == match_id]["home_team"].values[0]
    away_team = matches_df[matches_df["match_id"] == match_id]["away_team"].values[0]

    # Filtrar acciones principales
    principales_acciones = events[["team", "type"]].value_counts().reset_index(name="count")
    principales_acciones = principales_acciones.pivot(index="type", columns="team", values="count").fillna(0)

    st.table(principales_acciones)



if __name__ == "__main__":
    main()
