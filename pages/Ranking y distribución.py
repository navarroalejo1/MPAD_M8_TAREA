import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from statsbombpy import sb


# Función para cargar datos de partidos
def cargar_datos_partidos():
    try:
        partidos = sb.matches(competition_id=223, season_id=282)
        partidos["Plays"] = partidos["home_team"] + " vs " + partidos["away_team"]
        return partidos[["home_team", "away_team", "match_id", "Plays"]]
    except Exception as e:
        st.error(f"Error al cargar datos de partidos: {e}")
        return pd.DataFrame()


# Función para cargar eventos de todos los partidos
def cargar_eventos_partidos(matches_df):
    all_events = []
    for match_id in matches_df["match_id"]:
        try:
            events = sb.events(match_id=match_id)
            all_events.append(events)
        except Exception as e:
            st.warning(f"Error al cargar eventos para el partido {match_id}: {e}")
    if all_events:
        return pd.concat(all_events, ignore_index=True)
    return pd.DataFrame()


# Función para calcular rankings por tipo de acción
def calcular_rankings(events_df, tipos_incluidos):
    filtered_events = events_df[events_df["type"].isin(tipos_incluidos)]
    team_stats = filtered_events.groupby(["team", "type"]).size().reset_index(name="count")
    rankings = {}
    for tipo in tipos_incluidos:
        top_teams = team_stats[team_stats["type"] == tipo].sort_values(by="count", ascending=False).head(3)
        rankings[tipo] = top_teams
    return rankings


# Función para generar gráficos comparativos
def generar_grafico_comparativo(data, home_team, away_team, tipo_accion, ax=None):
    accion_home = data[(data["team"] == home_team) & (data["type"] == tipo_accion)]["count"].sum()
    accion_away = data[(data["team"] == away_team) & (data["type"] == tipo_accion)]["count"].sum()
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([home_team, away_team], [accion_home, accion_away], color=["#1f77b4", "#ff7f0e"])
    ax.set_title(f"Comparación: {tipo_accion}")
    ax.set_xlabel("Equipo")
    ax.set_ylabel("Cantidad")
    return ax


# Función principal
def main():
    st.title("Ranking Avanzado de Equipos")

    # Cargar datos de partidos
    matches_df = cargar_datos_partidos()
    if matches_df.empty:
        st.stop()

    # Cargar eventos de todos los partidos
    tipos_incluidos = ["Pass", "Shot", "Carry", "Duel", "Ball Recovery"]
    events_df = cargar_eventos_partidos(matches_df)
    if events_df.empty:
        st.warning("No se pudieron cargar los eventos de los partidos.")
        st.stop()

    # Calcular rankings iniciales
    rankings = calcular_rankings(events_df, tipos_incluidos)

    # Mostrar rankings
    st.subheader("Ranking de Equipos por Tipo de Acción")
    for tipo, data in rankings.items():
        st.write(f"**Top 3 en {tipo}:**")
        st.table(data)

    # Selección de partido para análisis detallado
    st.subheader("Análisis Detallado del Partido")
    selected_play = st.sidebar.selectbox("Selecciona un partido:", matches_df["Plays"])
    match_id = matches_df[matches_df["Plays"] == selected_play]["match_id"].values[0]
    home_team = matches_df[matches_df["match_id"] == match_id]["home_team"].values[0]
    away_team = matches_df[matches_df["match_id"] == match_id]["away_team"].values[0]

    # Filtrar eventos para el partido seleccionado
    filtered_events = events_df[events_df["match_id"] == match_id]

    if filtered_events.empty:
        st.warning(f"No se encontraron datos de eventos para el partido: {selected_play}")
        st.stop()

    # Comparación general de acciones por equipo
    st.subheader("Distribución General de Acciones por Equipo")

    # Agrupar datos por equipo
    team_totals = (
        filtered_events.groupby("team")["type"]
        .count()
        .reset_index(name="count")
    )

    if team_totals.empty:
        st.warning("No hay datos suficientes para mostrar la distribución de acciones.")
    else:
        # Crear gráfico de comparación
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(team_totals["team"], team_totals["count"], color=["#1f77b4", "#ff7f0e"])
        ax.set_title("Comparación de Acciones Totales")
        ax.set_xlabel("Equipo")
        ax.set_ylabel("Cantidad de Acciones")
        st.pyplot(fig)

    # Comparación detallada por tipo de acción
    st.subheader("Comparación Detallada por Tipo de Acción")
    for tipo_accion in tipos_incluidos:
        # Agrupar datos por equipo y tipo de acción
        tipo_data = filtered_events[filtered_events["type"] == tipo_accion]
        tipo_totals = tipo_data.groupby("team").size().reset_index(name="count")

        if tipo_totals.empty:
            st.warning(f"No hay datos para la acción: {tipo_accion}")
            continue

        # Crear gráfico para cada tipo de acción
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(tipo_totals["team"], tipo_totals["count"], color=["#1f77b4", "#ff7f0e"])
        ax.set_title(f"Comparación: {tipo_accion}")
        ax.set_xlabel("Equipo")
        ax.set_ylabel("Cantidad")
        st.pyplot(fig)


if __name__ == "__main__":
    main()
